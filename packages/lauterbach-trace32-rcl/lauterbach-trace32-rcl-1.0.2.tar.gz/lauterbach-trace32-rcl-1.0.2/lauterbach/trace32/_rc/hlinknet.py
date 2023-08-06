import queue
import socket
import struct

import lauterbach.trace32._rc._error as err
from lauterbach.trace32._rc.common import align_eight


class CommunicationInterface:
    def connect(self, node, port):
        pass

    def getHeadersize(self):
        pass

    def sync(self, maxTries=20):
        pass

    def transmit(self, data):
        pass

    def receive(self):
        pass

    def receive_notify_message(self):
        pass

    def notificationpending(self):
        pass

    def exit(self):
        pass


class NotificationQueue(queue.Queue):
    pass


# UDP specific constant definitions:
T32_API_RECEIVE = 0x01
T32_API_SYNCREQUEST = 0x02
T32_API_CONNECTREQUEST = 0x03
T32_API_DISCONNECT = 0x04
T32_API_SYNCBACKREQ = 0x05
T32_API_NOTIFICATION = 0x06
T32_API_NORMAL_TRANSMIT = 0x11
T32_API_SYNCACKN = 0x12
T32_API_SYNCACKN_BACK = 0x13
T32_API_SYNCBACK = 0x22

T32_API_KEEPALIVE = 0xFE

T32_MSG_LRETRY = 0x08

PCKLEN_MAX = 0x4000  # maximum size of UDP-packet
MAXRETRY = 5
MAGIC_PATTERN = b"TRACE32\0"
MAGIC_PATTERN_LENGTH = len(MAGIC_PATTERN)


class CommunicationBase(CommunicationInterface):
    """Implements common CommunicationInterface methods to TCP and UDP

    RCL configuration according to NETASSIST.
    """

    def __init__(self, packlen, timeout):
        self._socket = None

        self._message_id = 0
        self._transmit_block_id = 0
        self._receive_block_id = 0

        self._packlen = packlen
        self._timeout = timeout

        self._notify_queue = NotificationQueue()

    def __del__(self):
        self.exit()

    def notificationpending(self):
        """Return True if notifications remain in queue"""
        return not self._notify_queue.empty()


class CommunicationUdp(CommunicationBase):
    """Implements CommunicationInterface methods specific to UDP transfers"""

    def connect(self, node, port):
        """Bind socket and send connect request sequence"""

        if self._socket is not None:
            # connection already exists
            return

        try:

            self._hostname = node
            self._port = port
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # use UDP
            self._socket.settimeout(self._timeout)
            self._socket.bind(("", 0))

            socket_address, receive_port = self._socket.getsockname()

            # negotiate send/receive packet size
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, PCKLEN_MAX)
            val = self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

            self._packlen = min(val, self._packlen)

            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, PCKLEN_MAX)
            val = self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

        except Exception as e:
            raise err.ApiConnectionInitError(e)

        else:
            # Connection
            self._transmit_block_id = 1

            padding_length = self._packlen - (1 + 1 + 2 + 2 + 2 + MAGIC_PATTERN_LENGTH)
            magic_sequence = struct.pack(
                "BBHHH{}s{}x".format(MAGIC_PATTERN_LENGTH, padding_length),
                T32_API_CONNECTREQUEST,
                0x01,
                self._transmit_block_id,
                self._port,
                receive_port,
                MAGIC_PATTERN,
            )

            try:
                self._socket.sendto(magic_sequence, 0, (self._hostname, self._port))

                data = self._socket.recv(self._packlen)
            except Exception as e:
                raise err.ApiConnectionInitError(e) from None

            if not data[0] == T32_API_SYNCACKN_BACK:
                raise err.ApiConnectionInitError("received invalid sync acknowledge back")

            if not data[1:] == magic_sequence[1:]:
                raise err.ApiConnectionInitError("received wrong magic pattern")

            self._receive_block_id = int.from_bytes(data[2:4], byteorder="little")

    def getHeadersize(self):
        """Return protocol specific length of header bytes per packet"""
        return 5 + 4

    # == LINE_CommunicationSync() in hlinknet.c
    def sync(self, maxTries=20):
        """Send synchronisation request"""

        success = False

        send_data = struct.pack(
            "BBHI{}s".format(MAGIC_PATTERN_LENGTH),
            T32_API_SYNCREQUEST,
            0x00,
            self._transmit_block_id,
            0x00,
            MAGIC_PATTERN,
        )

        try:
            self._socket.sendto(send_data, 0, (self._hostname, self._port))
            for attempt in range(maxTries):

                recv_data, sender_info = self._socket.recvfrom(self._packlen)
                if recv_data[0] == T32_API_SYNCBACKREQ and len(recv_data) == 16:
                    success = self.sync(maxTries - attempt)  # initiate retry with remaining attempts
                    break
                # wait for sync ackn
                if (
                    recv_data[0] == T32_API_SYNCACKN
                    and len(recv_data) == 16
                    and str(recv_data[8:]).startswith(str(MAGIC_PATTERN))
                ):
                    self._receive_block_id = int.from_bytes(recv_data[2:4], byteorder="little")
                    break

            else:  # nobreak
                raise err.ApiConnectionSyncError("max number of attempts reaced")

            if not success:

                send_data = struct.pack(
                    "BBHI{}s".format(MAGIC_PATTERN_LENGTH),
                    T32_API_SYNCBACK,
                    0x00,
                    self._transmit_block_id,
                    0x00,
                    MAGIC_PATTERN,
                )
                self._socket.sendto(send_data, 0, (self._hostname, self._port))

                success = True

        except Exception as e:
            success = False
            raise err.ApiConnectionSyncError(e)

        return success

    # == LINE_Transmit() in hremote.c
    def transmit(self, data):
        """Write send data to send socket"""

        if data is None:
            raise err.ApiConnectionTransmitError("called transmit on None data")

        assert isinstance(data, bytes) or isinstance(data, bytearray), "Transmit data are not bytes format"

        try:
            # prepend header
            data = b"\x00" * 5 + data

            chunk_size = self._packlen - 4
            chunk = data[:chunk_size]
            chunk_count = 1

            while chunk:
                if data[(chunk_size * chunk_count) :]:
                    followingPacketFlag = 1
                else:
                    followingPacketFlag = 0

                send_data = struct.pack(
                    "BBH{}s".format(len(chunk)),
                    T32_API_NORMAL_TRANSMIT,
                    followingPacketFlag,
                    self._transmit_block_id,
                    chunk,
                )

                self._socket.sendto(send_data, 0, (self._hostname, self._port))
                self._transmit_block_id = (self._transmit_block_id + 1) % (1 << 16)

                # prepare next chunk:
                chunk_from = chunk_size * chunk_count
                chunk_to = chunk_size * (chunk_count + 1)
                chunk = data[chunk_from:chunk_to]
                chunk_count += 1

        except Exception as e:
            raise err.ApiConnectionTransmitError(e)

    def receive(self, message_id):
        """Polls receive data for incoming responses"""

        HEADER = 9
        for retry in range(MAXRETRY):

            inbuffer = self.line_receive()

            if inbuffer is None:
                raise err.ApiConnectionReceiveError("receiving UDP packet failed")

            elif inbuffer[HEADER - 2] == T32_API_KEEPALIVE:
                # not sure what this is supposed to do
                # self.setreceivetogglebit(-1)
                continue

            elif not inbuffer[HEADER - 1] == message_id:
                continue

            # elif inbuffer[HEADER-5] & T32_MSG_LRETRY:
            #    if False: #TODO T32_MSG_LHANDLE and getreceivetogglebit ???
            #        self.transmit(data=bytes(1)) #transmit 0 ???
            #        self.sync()
            #        continue

            else:
                # self.setreceivetogglebit(blabla)
                break

        else:  # nobreak
            raise err.ApiHeaderError("UDP packet contains invalid message header")

        return inbuffer[HEADER - 2 :]

    # == LINE_CommunicationReceive() in hlinknet.c
    def line_receive(self):
        """Read data from receive socket"""

        data = None
        header_length = 0  # keep header of first arriving packet, omit subsequent
        remainingPackets = True
        received_data = bytearray(0)

        while remainingPackets:

            packet_received, sender_info = self._socket.recvfrom(self._packlen)
            i = len(packet_received)

            if i == 1 and packet_received[0] == b"+":
                # got a handshakepackage, ignore it
                continue

            elif i < 5:
                # requires 5 byte header
                raise err.ApiHeaderError("UDP message header too short")

            # Detect and enqeue async notification that slipped into a request/reply pair
            elif packet_received[0] == T32_API_NOTIFICATION:
                self._notify_queue.put(packet_received)
                continue

            elif packet_received[0] == T32_API_RECEIVE:
                received_data += packet_received[header_length:]
                header_length = 4  # omit header of subsequent messages delivering chunks
                if packet_received[1] == 0:
                    remainingPackets = False
                self._receive_block_id += 1
                if packet_received[1] == 2:
                    handshake = b"\x07\x00\x00\x00\x00\x00\x00\x00TRACE32\x00"
                    self._socket.sendto(handshake, 0, (self._hostname, self._port))

            else:
                raise err.ApiHeaderError("unkown UDP message header received")

            data = received_data

        return data

    def receive_notify_message(self):
        """Poll for notification messages, queue them"""

        try:
            msg_data = self._notify_queue.get(block=False)

        except queue.Empty:
            try:
                packet_received, sender_info = self._socket.recvfrom(self._packlen)
                msg_type = packet_received[0]
                msg_data = packet_received
            except Exception:
                # aparently there is no notification
                return None

            else:
                if not msg_type == T32_API_NOTIFICATION:
                    raise err.ApiHeaderError("UDP packet does not contain Notification")

        return msg_data

    def exit(self):
        """Send termination sequence to remote server"""

        if self._socket is not None:

            send_data = struct.pack("Q{}s".format(MAGIC_PATTERN_LENGTH), T32_API_DISCONNECT, MAGIC_PATTERN)
            try:
                for i in range(5):
                    self._socket.sendto(send_data, 0, (self._hostname, self._port))
            except Exception:
                pass

            try:
                self._socket.close()
            except Exception:
                pass
            finally:
                self._socket = None


# TCP specific constant definitions:
T32_NETTCP_RCL_REQ = 0x0010
T32_NETTCP_RCL_RESP = 0x0011
T32_NETTCP_RCL_NOTIFY = 0x0012


class CommunicationTcp(CommunicationBase):
    """Implements CommunicationInterface methods specific to TCP transfers.

    RCL client according to NETTCP configuration
    """

    def connect(self, node, port):
        """Connect socket to remote node"""
        if self._socket is not None:
            # connection already exists
            return

        self._hostname = node
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(self._timeout)
        self._socket.connect((self._hostname, self._port))

    def getHeadersize(self):
        """Get protocol specific header length"""
        return 8 + 2

    def sync(self, maxTries=20):
        """Dummy stub, there is no sync mechanism with TCP packets"""
        return True

    def transmit(self, data):
        """Assemble and write message data to send socket"""

        if data is None:
            raise err.ApiConnectionTransmitError("called transmit on None data")

        assert isinstance(data, bytes) or isinstance(data, bytearray), "Transmit data are not bytes format"

        try:
            size = len(data)

            padding_length = align_eight(size + 4 + 4)
            send_data = struct.pack("II{}s{}x".format(size, padding_length), size, T32_NETTCP_RCL_REQ, data)

            self._socket.sendto(send_data, 0, (self._hostname, self._port))
        except Exception as e:
            raise err.ApiConnectionTransmitError(e)

    def receive(self, message_id):
        """Read receive data, evaluate for errors"""

        while True:

            packet_received, sender_info = self._socket.recvfrom(self._packlen)
            msg_len = int.from_bytes(packet_received[:4], byteorder="little")
            msg_type = int.from_bytes(packet_received[4:8], byteorder="little")
            msg_data = packet_received[8 : 8 + msg_len]

            if msg_type == T32_NETTCP_RCL_NOTIFY:
                # potential bug, if notification is longer than one packet!
                self._notify_queue.put(msg_data)
                continue

            elif msg_type == T32_NETTCP_RCL_RESP:
                msg_id_received = int.from_bytes(packet_received[9:10], byteorder="little")
                if msg_id_received == message_id:
                    if msg_data[0] == T32_API_KEEPALIVE:
                        # keep on polling as rcl host will send empty keepalive packets
                        # in case the processing takes longer
                        continue
                    break
                elif msg_id_received < message_id:
                    continue
                else:
                    raise err.ApiConnectionReceiveError("Messages out of sync")

            else:
                raise err.ApiHeaderError("TCP packet contains invalid messagetype")

        # if not msg_data[0] == 0:
        #    raise err.ResponseErrorCode(msg_data[0])

        if len(msg_data) < msg_len:
            # need to receive more packets with remaining payload
            result = msg_data
            while len(result) < msg_len:
                msg_data, sender_info = self._socket.recvfrom(self._packlen)
                result += msg_data

            return result[:msg_len]
        else:
            return msg_data[:msg_len]

    def receive_notify_message(self):
        """Poll and queue notification messages from socket"""

        try:
            msg_data = self._notify_queue.get(block=False)

        except queue.Empty:
            try:
                packet_received, sender_info = self._socket.recvfrom(self._packlen)
                msg_len = int.from_bytes(packet_received[:4], byteorder="little")
                msg_type = int.from_bytes(packet_received[4:8], byteorder="little")
                msg_data = packet_received[8 : 8 + msg_len]
            except Exception:
                # aparently there is no notification
                return None

            else:
                if not msg_type == T32_NETTCP_RCL_NOTIFY:
                    raise err.ApiHeaderError("TCP packet does not contain Notification")

        return msg_data

    def exit(self):
        """Close socket"""

        if self._socket is not None:
            try:
                self._socket.close()
            except Exception:
                pass
            finally:
                self._socket = None


class Link:
    """Provides communication for remote API according to set configuration

        Args:
            configuration (str,dict): Parameters for client connection to remote API such as node, protocol, port etc.

    """

    def __init__(self, node, port, packlen, protocol, timeout):

        self._message_id = 0
        self._transmit_block_id = 0
        self._receive_block_id = 0

        self.node = node
        self.port = port
        self.packlen = packlen
        self.protocol = protocol
        self.timeout = timeout

        if protocol == "TCP":
            # ignore packlen parameter for TCP, always use 16384
            self._line = CommunicationTcp(0x4000, self.timeout)
            # self._line = CommunicationTcp(self.packlen, self.timeout)
        elif protocol == "UDP":
            self._line = CommunicationUdp(self.packlen, self.timeout)
        else:
            raise NotImplementedError('protocol other than "UDP","TCP"')

        self.connect()

    @property
    def node(self):
        return self.__node

    @node.setter
    def node(self, val):
        self.__node = str(val)

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, val):
        self.__port = int(val)

    @property
    def packlen(self):
        return self.__packlen

    @packlen.setter
    def packlen(self, val):
        self.__packlen = int(val)

    @property
    def protocol(self):
        return self.__protocol

    @protocol.setter
    def protocol(self, val):
        if val not in ("TCP", "UDP"):
            raise err.ApiConnectionConfigError("invalid protocol {}".format(val))
        else:
            self.__protocol = val

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, val):
        if val is None:
            self.__timeout = None
        else:
            self.__timeout = float(val)

    def connect(self, node=None, port=None):
        if node is not None and port is not None:
            return self._line.connect(node, port)
        else:
            return self._line.connect(self.node, self.port)

    def sync(self, *a, **kw):
        return self._line.sync(*a, **kw)

    def transmit(self, *a, **kw):
        return self._line.transmit(*a, **kw)

    def receive(self, *a, **kw):
        msg_id = self.get_message_id()
        try:
            return self._line.receive(message_id=msg_id, *a, **kw)
        except socket.timeout as e:
            raise err.ApiConnectionTimeoutError(str(e)) from None

    def receive_notify_message(self, *a, **kw):
        return self._line.receive_notify_message(*a, **kw)

    def getHeadersize(self, *a, **kw):
        return self._line.getHeadersize(*a, **kw)

    def exit(self, *a, **kw):
        return self._line.exit(*a, **kw)

    def get_message_id(self):
        return self._message_id % 255

    def increment_message_id(self, n=1):
        self._message_id += n
        return self._message_id % 255
