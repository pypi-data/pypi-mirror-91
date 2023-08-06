import lauterbach.trace32._rc._error as err
from lauterbach.trace32._rc.common import int2bytearray, up_align

from ._address import Address


class Symbol:
    def __init__(self, conn, *, address=None, name=None):
        self.__conn = conn
        self.address = address
        self.name = name
        self.path = None
        self.size = None

    def __str__(self):
        return "{}{} {} {}".format(
            self.__path if self.__path is not None else "", self.__name, str(self.address), self.size,
        )

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        if address is None:
            self.__address = None
        elif isinstance(address, Address):
            self.__address = address
        else:
            raise err.SymbolAddressError("Invalid address type: {} expects Address object".format(type(address)))

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    def query(self):
        """Queries symbol

        Returns:
            Symbol: Result
        """
        recv_buffer = self.__conn.library.t32_querysymbolobj(self)
        return self.deserialize(recv_buffer)

    def serialize(self):

        result = b""
        if self.address is not None:
            result += b"AD"
            addr_params_size, addr_params = self.address.serialize()
            result += addr_params

        if self.name is not None:
            name = self.name.encode()
            namelen = up_align(len(name) + 1, 2)
            result += b"NM"
            result += int2bytearray(namelen, 2)
            result += name
            result += int2bytearray(0x00, namelen - len(name))

        if self.path is not None:
            path = self.path.encode()
            pathlen = up_align(len(path) + 1, 2)
            result += b"PR"
            result += int2bytearray(pathlen, 2)
            result += path
            result += int2bytearray(0x00, pathlen - len(path))

        result += b"XX"  # = end marker
        return len(result), result

    def deserialize(self, recv_buffer):
        read_ptr = 0
        parameter_id_len = 2

        while read_ptr < len(recv_buffer):

            parameter_id = recv_buffer[read_ptr : read_ptr + parameter_id_len]

            if parameter_id == b"AD":
                read_ptr += parameter_id_len
                addr_params_size, address = Address.deserialize(self.__conn, recv_buffer[read_ptr:])
                next_read_ptr = read_ptr + addr_params_size
                self.address = address

            elif parameter_id == b"NM":
                read_ptr += parameter_id_len

                field_len = int.from_bytes(recv_buffer[read_ptr : read_ptr + 2], byteorder="little")
                read_ptr += 2

                next_read_ptr = read_ptr + field_len
                name = recv_buffer[read_ptr:next_read_ptr].decode()

                if len(name) > field_len:
                    raise ValueError()

                self.name = name

            elif parameter_id == b"SZ":
                read_ptr += parameter_id_len
                next_read_ptr = read_ptr + 8
                self.size = int.from_bytes(recv_buffer[read_ptr:next_read_ptr], byteorder="little")

            elif parameter_id == b"NE":  # name extension
                read_ptr += parameter_id_len
                field_len = int.from_bytes(recv_buffer[read_ptr : read_ptr + 2], byteorder="little")
                read_ptr += 2

                next_read_ptr = read_ptr + field_len
                name_extension = recv_buffer[read_ptr:next_read_ptr].decode()

                if len(name_extension) > field_len:
                    raise ValueError()

                # name_extension not implemented yet
                # self.name_extension = name_extension

            elif parameter_id == b"PR":
                read_ptr += parameter_id_len

                field_len = int.from_bytes(recv_buffer[read_ptr : read_ptr + 2], byteorder="little")
                read_ptr += 2

                next_read_ptr = read_ptr + field_len
                path = recv_buffer[read_ptr:next_read_ptr].decode()

                if len(path) > field_len:
                    raise ValueError()

                self.path = path

            elif parameter_id == b"XX":
                read_ptr += parameter_id_len
                break

            else:
                raise ValueError()

            read_ptr = next_read_ptr

        return self


class SymbolService:
    def __init__(self, conn):
        self.__conn = conn

    def __call__(self, *args, **kwargs):
        return Symbol(self.__conn, *args, **kwargs)

    def _symbol_query(self, address=None, name=None) -> Symbol:
        if address is None and name is None:
            raise err.SymbolQueryError("Either address or name must be set to query, but not both.")
        elif address is not None and name is not None:
            raise err.SymbolQueryError("Either address or name must be set to query, but not both.")
        sym = Symbol(self.__conn, address=address, name=name)
        if name is not None:
            sym.name = name
        elif address is not None:
            sym.address = address

        return sym.query()

    def query_by_address(self, address) -> Symbol:
        """Search symbol by address.

        Args:
            address (Address): Name with which the symbol is searched.

        Returns:
            Symbol: Result
        """
        return self._symbol_query(address=address)

    def query_by_name(self, name) -> Symbol:
        """Search symbol by name.

        Args:
            name (str): Address at which the symbol is searched.

        Returns:
            Symbol: Result
        """
        return self._symbol_query(name=name)
