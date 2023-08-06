from lauterbach.trace32._rc._error import BaseError


class FunctionError(BaseError):
    pass


class FunctionService:
    """
    Executes function on call.
    """
    def __init__(self, conn):
        self.__conn = conn

    def __call__(self, command: str):
        return self.__conn._fnc(command)

    def iobase_address(self) -> object:
        return self.__conn._fnc("IOBASE.ADDRESS()")

    def iobase2(self) -> int:
        return self.__conn._fnc("IOBASE2()")

    def tpubase_address(self) -> object:
        return self.__conn._fnc("TPUBASE.ADDRESS()")

    def fasbase_address(self) -> object:
        return self.__conn._fnc("FASBASE.ADDRESS()")

    def per_arg_address(self, addr: int) -> object:
        return self.__conn._fnc("PER.ARG.ADDRESS(" + str(addr) + ")")

    def per_address_isnonsecure(self, pAddrIn: int) -> bool:
        return self.__conn._fnc("PER.ADDRESS.isNONSECURE(" + str(pAddrIn) + ")")

    def per_address_isnonsecureex(self, pAddrIn: int) -> bool:
        return self.__conn._fnc("PER.ADDRESS.isNONSECUREEX(" + str(pAddrIn) + ")")

    def per_address_issecure(self, pAddrIn: int) -> bool:
        return self.__conn._fnc("PER.ADDRESS.isSECURE(" + str(pAddrIn) + ")")

    def per_address_issecureex(self, pAddrIn: int) -> bool:
        return self.__conn._fnc("PER.ADDRESS.isSECUREEX(" + str(pAddrIn) + ")")

    def per_eval(self, integer: int) -> object:
        return self.__conn._fnc("PER.EVAL(" + str(integer) + ")")

    def per_filename(self) -> str:
        return self.__conn._fnc("PER.FILENAME()")

    def per_byte(self, address: int) -> int:
        return self.__conn._fnc("PER.Byte(" + str(address) + ")")

    def per_word_littleendian(self, address: int) -> int:
        return self.__conn._fnc("PER.Word.LittleEndian(" + str(address) + ")")

    def per_word_bigendian(self, address: int) -> int:
        return self.__conn._fnc("PER.Word.BigEndian(" + str(address) + ")")

    def per_short_littleendian(self, address: int) -> int:
        return self.__conn._fnc("PER.Short.LittleEndian(" + str(address) + ")")

    def per_short_bigendian(self, address: int) -> int:
        return self.__conn._fnc("PER.Short.BigEndian(" + str(address) + ")")

    def per_long_littleendian(self, address: int) -> int:
        return self.__conn._fnc("PER.Long.LittleEndian(" + str(address) + ")")

    def per_long_bigendian(self, address: int) -> int:
        return self.__conn._fnc("PER.Long.BigEndian(" + str(address) + ")")

    def per_slong(self, address: int) -> int:
        return self.__conn._fnc("PER.SLong(" + str(address) + ")")

    def per_quad_littleendian(self, address: int) -> int:
        return self.__conn._fnc("PER.Quad.LittleEndian(" + str(address) + ")")

    def per_quad_bigendian(self, address: int) -> int:
        return self.__conn._fnc("PER.Quad.BigEndian(" + str(address) + ")")

    def per_longlong_littleendian(self, address: int) -> int:
        return self.__conn._fnc("PER.LongLong.LittleEndian(" + str(address) + ")")

    def per_longlong_bigendian(self, address: int) -> int:
        return self.__conn._fnc("PER.LongLong.BigEndian(" + str(address) + ")")

    def per_tbyte(self, address: int) -> int:
        return self.__conn._fnc("PER.TByte(" + str(address) + ")")

    def per_pbyte(self, address: int) -> int:
        return self.__conn._fnc("PER.PByte(" + str(address) + ")")

    def per_hbyte(self, address: int) -> int:
        return self.__conn._fnc("PER.HByte(" + str(address) + ")")

    def per_sbyte(self, address: int) -> int:
        return self.__conn._fnc("PER.SByte(" + str(address) + ")")

    def per_buffer_byte(self, index: int) -> int:
        return self.__conn._fnc("PER.Buffer.Byte(" + str(index) + ")")

    def per_buffer_word(self, index: int) -> int:
        return self.__conn._fnc("PER.Buffer.Word(" + str(index) + ")")

    def per_buffer_short(self, index: int) -> int:
        return self.__conn._fnc("PER.Buffer.Short(" + str(index) + ")")

    def per_buffer_long(self, index: int) -> int:
        return self.__conn._fnc("PER.Buffer.Long(" + str(index) + ")")

    def per_buffer_quad(self, index: int) -> int:
        return self.__conn._fnc("PER.Buffer.Quad(" + str(index) + ")")

    def per_buffer_longlong(self, index: int) -> int:
        return self.__conn._fnc("PER.Buffer.LongLong(" + str(index) + ")")

    def register_list(self, register_name: int) -> str:
        return self.__conn._fnc("Register.LIST(" + str(register_name) + ")")

    def pp(self) -> object:
        return self.__conn._fnc("PP()")

    def fpu_raw(self, name: int) -> int:
        return self.__conn._fnc("FPU.RAW(" + str(name) + ")")

    def fpucr(self, name: int) -> int:
        return self.__conn._fnc("FPUCR(" + str(name) + ")")

    def mmu_format_detected_zone(self, address: int) -> str:
        return self.__conn._fnc("MMU.FORMAT.DETECTED.ZONE(" + str(address) + ")")

    def mmu_format_zone(self, address: int) -> str:
        return self.__conn._fnc("MMU.FORMAT.ZONE(" + str(address) + ")")

    def mmu_defaultpt_zone(self, address: int) -> object:
        return self.__conn._fnc("MMU.DEFAULTPT.ZONE(" + str(address) + ")")

    def mmu_defaultpt2(self) -> object:
        return self.__conn._fnc("MMU.DEFAULTPT2()")

    def mmu_defaulttrans_logrange_zone(self, address: int) -> object:
        return self.__conn._fnc(
            "MMU.DEFAULTTRANS.LOGRANGE.ZONE(" + str(address) + ")"
        )

    def mmu_defaulttrans_physaddr_zone(self, address: int) -> object:
        return self.__conn._fnc(
            "MMU.DEFAULTTRANS.PHYSADDR.ZONE(" + str(address) + ")"
        )

    def mmu_logical_valid(self, physical_address: int) -> bool:
        return self.__conn._fnc("MMU.LOGICAL.VALID(" + str(physical_address) + ")")

    def mmu_physical_valid(self, addrin: int) -> bool:
        return self.__conn._fnc("MMU.PHYSICAL.VALID(" + str(addrin) + ")")

    def mmu_physicalex_valid(self, addrin: int) -> bool:
        return self.__conn._fnc("MMU.PHYSICALEX.VALID(" + str(addrin) + ")")

    def mmu_intermediate_valid(self, address: int) -> bool:
        return self.__conn._fnc("MMU.INTERMEDIATE.VALID(" + str(address) + ")")

    def mmu_intermediateex_valid(self, addrin: int) -> bool:
        return self.__conn._fnc("MMU.INTERMEDIATEEX.VALID(" + str(addrin) + ")")

    def mmu_linear_valid(self, address: int) -> bool:
        return self.__conn._fnc("MMU.LINEAR.VALID(" + str(address) + ")")

    def mmu_linearex_valid(self, addrin: int) -> bool:
        return self.__conn._fnc("MMU.LINEAREX.VALID(" + str(addrin) + ")")

    def data_byte(self, address: int) -> int:
        return self.__conn._fnc("Data.Byte(" + str(address) + ")")

    def data_word_littleendian(self, address: int) -> int:
        return self.__conn._fnc("Data.Word.LittleEndian(" + str(address) + ")")

    def data_word_bigendian(self, address: int) -> int:
        return self.__conn._fnc("Data.Word.BigEndian(" + str(address) + ")")

    def data_word_byte(self, address: int) -> int:
        return self.__conn._fnc("Data.Word.Byte(" + str(address) + ")")

    def data_word_word(self, address: int) -> int:
        return self.__conn._fnc("Data.Word.Word(" + str(address) + ")")

    def data_short_littleendian(self, address: int) -> int:
        return self.__conn._fnc("Data.Short.LittleEndian(" + str(address) + ")")

    def data_short_bigendian(self, address: int) -> int:
        return self.__conn._fnc("Data.Short.BigEndian(" + str(address) + ")")

    def data_long_littleendian(self, address: int) -> int:
        return self.__conn._fnc("Data.Long.LittleEndian(" + str(address) + ")")

    def data_long_bigendian(self, address: int) -> int:
        return self.__conn._fnc("Data.Long.BigEndian(" + str(address) + ")")

    def data_long_byte(self, address: int) -> int:
        return self.__conn._fnc("Data.Long.Byte(" + str(address) + ")")

    def data_long_word(self, address: int) -> int:
        return self.__conn._fnc("Data.Long.Word(" + str(address) + ")")

    def data_long_long(self, address: int) -> int:
        return self.__conn._fnc("Data.Long.Long(" + str(address) + ")")

    def data_slong(self, address: int) -> int:
        return self.__conn._fnc("Data.SLong(" + str(address) + ")")

    def data_quad_littleendian(self, address: int) -> int:
        return self.__conn._fnc("Data.Quad.LittleEndian(" + str(address) + ")")

    def data_quad_bigendian(self, address: int) -> int:
        return self.__conn._fnc("Data.Quad.BigEndian(" + str(address) + ")")

    def data_quad_byte(self, address: int) -> int:
        return self.__conn._fnc("Data.Quad.Byte(" + str(address) + ")")

    def data_quad_word(self, address: int) -> int:
        return self.__conn._fnc("Data.Quad.Word(" + str(address) + ")")

    def data_quad_long(self, address: int) -> int:
        return self.__conn._fnc("Data.Quad.Long(" + str(address) + ")")

    def data_quad_quad(self, address: int) -> int:
        return self.__conn._fnc("Data.Quad.Quad(" + str(address) + ")")

    def data_longlong_littleendian(self, address: int) -> int:
        return self.__conn._fnc("Data.LongLong.LittleEndian(" + str(address) + ")")

    def data_longlong_bigendian(self, address: int) -> int:
        return self.__conn._fnc("Data.LongLong.BigEndian(" + str(address) + ")")

    def data_tbyte(self, address: int) -> int:
        return self.__conn._fnc("Data.TByte(" + str(address) + ")")

    def data_pbyte(self, address: int) -> int:
        return self.__conn._fnc("Data.PByte(" + str(address) + ")")

    def data_hbyte(self, address: int) -> int:
        return self.__conn._fnc("Data.HByte(" + str(address) + ")")

    def data_sbyte(self, address: int) -> int:
        return self.__conn._fnc("Data.SByte(" + str(address) + ")")

    def data_string_byte(self, paddr: int) -> str:
        return self.__conn._fnc("Data.STRing.Byte(" + str(paddr) + ")")

    def data_stringn(self, length: int, address: int) -> str:
        return self.__conn._fnc(
            "Data.STRingN(" + str(length) + ", " + str(address) + ")"
        )

    def data_wstring_bigendian(self, address: int) -> str:
        return self.__conn._fnc("Data.WSTRING.BigEndian(" + str(address) + ")")

    def data_wstring_littleendian(self, address: int) -> str:
        return self.__conn._fnc("Data.WSTRING.LittleEndian(" + str(address) + ")")

    def data_float(self, address: int, format: int) -> float:
        return self.__conn._fnc(
            "Data.Float(" + str(address) + ", " + str(format) + ")"
        )

    def data_sum(self) -> int:
        return self.__conn._fnc("Data.SUM()")

    def data_jumptarget(self, paddr: int) -> int:
        return self.__conn._fnc("Data.JUMPTARGET(" + str(paddr) + ")")

    def data_al_errors(self) -> int:
        return self.__conn._fnc("Data.AL.ERRORS()")

    def eval_address(self) -> object:
        return self.__conn._fnc("EVAL.ADDRESS()")

    def eval_addressrange(self) -> object:
        return self.__conn._fnc("EVAL.ADDRESSRANGE()")

    def eval_string(self) -> str:
        return self.__conn._fnc("EVAL.STRing()")

    def eval_type(self) -> int:
        return self.__conn._fnc("EVAL.TYPE()")

    def cache_ic_valid(self, way: int, set: int) -> bool:
        return self.__conn._fnc("CACHE.IC.VALID(" + str(way) + ", " + str(set) + ")")

    def cache_ic_validmask(self, way: int, set: int) -> int:
        return self.__conn._fnc(
            "CACHE.IC.VALIDMASK(" + str(way) + ", " + str(set) + ")"
        )

    def cache_ic_dirty(self, way: int, set: int) -> bool:
        return self.__conn._fnc("CACHE.IC.DIRTY(" + str(way) + ", " + str(set) + ")")

    def cache_ic_dirtymask(self, way: int, set: int) -> int:
        return self.__conn._fnc(
            "CACHE.IC.DIRTYMASK(" + str(way) + ", " + str(set) + ")"
        )

    def cache_ic_tag(self, way: int, set: int) -> int:
        return self.__conn._fnc("CACHE.IC.TAG(" + str(way) + ", " + str(set) + ")")

    def cache_ic_lru(self, set: int) -> int:
        return self.__conn._fnc("CACHE.IC.LRU(" + str(set) + ")")

    def cache_dc_valid(self, way: int, set: int) -> bool:
        return self.__conn._fnc("CACHE.DC.VALID(" + str(way) + ", " + str(set) + ")")

    def cache_dc_validmask(self, way: int, set: int) -> int:
        return self.__conn._fnc(
            "CACHE.DC.VALIDMASK(" + str(way) + ", " + str(set) + ")"
        )

    def cache_dc_dirty(self, way: int, set: int) -> bool:
        return self.__conn._fnc("CACHE.DC.DIRTY(" + str(way) + ", " + str(set) + ")")

    def cache_dc_dirtymask(self, way: int, set: int) -> int:
        return self.__conn._fnc(
            "CACHE.DC.DIRTYMASK(" + str(way) + ", " + str(set) + ")"
        )

    def cache_dc_tag(self, way: int, set: int) -> int:
        return self.__conn._fnc("CACHE.DC.TAG(" + str(way) + ", " + str(set) + ")")

    def cache_dc_lru(self, set: int) -> int:
        return self.__conn._fnc("CACHE.DC.LRU(" + str(set) + ")")

    def cache_l2_valid(self, way: int, set: int) -> bool:
        return self.__conn._fnc("CACHE.L2.VALID(" + str(way) + ", " + str(set) + ")")

    def cache_l2_validmask(self, way: int, set: int) -> int:
        return self.__conn._fnc(
            "CACHE.L2.VALIDMASK(" + str(way) + ", " + str(set) + ")"
        )

    def cache_l2_dirty(self, way: int, set: int) -> bool:
        return self.__conn._fnc("CACHE.L2.DIRTY(" + str(way) + ", " + str(set) + ")")

    def cache_l2_dirtymask(self, way: int, set: int) -> int:
        return self.__conn._fnc(
            "CACHE.L2.DIRTYMASK(" + str(way) + ", " + str(set) + ")"
        )

    def cache_l2_shared(self, way: int, set: int) -> bool:
        return self.__conn._fnc("CACHE.L2.SHARED(" + str(way) + ", " + str(set) + ")")

    def cache_l2_sharedmask(self, way: int, set: int) -> int:
        return self.__conn._fnc(
            "CACHE.L2.SHAREDMASK(" + str(way) + ", " + str(set) + ")"
        )

    def cache_l2_tag(self, way: int, set: int) -> int:
        return self.__conn._fnc("CACHE.L2.TAG(" + str(way) + ", " + str(set) + ")")

    def cache_l2_lru(self, set: int) -> int:
        return self.__conn._fnc("CACHE.L2.LRU(" + str(set) + ")")

    def cache_l3_valid(self, way: int, set: int) -> bool:
        return self.__conn._fnc("CACHE.L3.VALID(" + str(way) + ", " + str(set) + ")")

    def cache_l3_validmask(self, way: int, set: int) -> int:
        return self.__conn._fnc(
            "CACHE.L3.VALIDMASK(" + str(way) + ", " + str(set) + ")"
        )

    def cache_l3_dirty(self, way: int, set: int) -> bool:
        return self.__conn._fnc("CACHE.L3.DIRTY(" + str(way) + ", " + str(set) + ")")

    def cache_l3_dirtymask(self, way: int, set: int) -> int:
        return self.__conn._fnc(
            "CACHE.L3.DIRTYMASK(" + str(way) + ", " + str(set) + ")"
        )

    def cache_l3_tag(self, way: int, set: int) -> int:
        return self.__conn._fnc("CACHE.L3.TAG(" + str(way) + ", " + str(set) + ")")

    def cache_l3_lru(self, set: int) -> int:
        return self.__conn._fnc("CACHE.L3.LRU(" + str(set) + ")")

    def task_back(self) -> int:
        return self.__conn._fnc("TASK.BACK()")

    def task_fore(self) -> int:
        return self.__conn._fnc("TASK.FORE()")

    def task_spaceid(self, task_name: int) -> int:
        return self.__conn._fnc("TASK.SPACEID(" + str(task_name) + ")")

    def task_id(self, task_name: int) -> int:
        return self.__conn._fnc("TASK.ID(" + str(task_name) + ")")

    def task_magic(self, task_name: int) -> int:
        return self.__conn._fnc("TASK.MAGIC(" + str(task_name) + ")")

    def task_name(self, task_magic: int) -> str:
        return self.__conn._fnc("TASK.NAME(" + str(task_magic) + ")")

    def task_access_zone(self) -> str:
        return self.__conn._fnc("TASK.ACCESS.ZONE()")

    def task_configfile(self) -> str:
        return self.__conn._fnc("TASK.CONFIGFILE()")

    def task_machineid(self, name: int) -> int:
        return self.__conn._fnc("TASK.MACHINEID(" + str(name) + ")")

    def task_machine_name(self, machine_id: int) -> str:
        return self.__conn._fnc("TASK.MACHINE.NAME(" + str(machine_id) + ")")

    def task_machine_access(self, machine_id: int) -> str:
        return self.__conn._fnc("TASK.MACHINE.ACCESS(" + str(machine_id) + ")")

    def track_address_data(self) -> object:
        return self.__conn._fnc("TRACK.ADDRESS.DATA()")

    def track_address_prog(self) -> object:
        return self.__conn._fnc("TRACK.ADDRESS.PROG()")

    def track_string(self) -> str:
        return self.__conn._fnc("TRACK.STRing()")

    def track_record(self) -> int:
        return self.__conn._fnc("TRACK.RECORD()")

    def track_column(self) -> int:
        return self.__conn._fnc("TRACK.COLUMN()")

    def track_line(self) -> int:
        return self.__conn._fnc("TRACK.LINE()")

    def track_time(self) -> object:
        return self.__conn._fnc("TRACK.TIME()")

    def error_address(self) -> object:
        return self.__conn._fnc("ERROR.ADDRESS()")

    def error_cmdline(self) -> str:
        return self.__conn._fnc("ERROR.CMDLINE()")

    def error_fileline(self) -> int:
        return self.__conn._fnc("ERROR.FILELINE()")

    def error_filename(self) -> str:
        return self.__conn._fnc("ERROR.FILENAME()")

    def error_id(self) -> str:
        return self.__conn._fnc("ERROR.ID()")

    def error_firstid(self) -> str:
        return self.__conn._fnc("ERROR.FIRSTID()")

    def error_message(self) -> str:
        return self.__conn._fnc("ERROR.MESSAGE()")

    def error_occurred(self) -> bool:
        return self.__conn._fnc("ERROR.OCCURRED()")

    def error_position(self) -> int:
        return self.__conn._fnc("ERROR.POSITION()")

    def address_access(self, address: int) -> int:
        return self.__conn._fnc("ADDRESS.ACCESS(" + str(address) + ")")

    def address_isdata(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isDATA(" + str(address) + ")")

    def address_expandaccess(self, address: int) -> object:
        return self.__conn._fnc("ADDRESS.EXPANDACCESS(" + str(address) + ")")

    def address_expandaccessp(self, pAddrIn: int) -> object:
        return self.__conn._fnc("ADDRESS.EXPANDACCESSP(" + str(pAddrIn) + ")")

    def address_isintermediate(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isINTERMEDIATE(" + str(address) + ")")

    def address_isnonsecure(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isNONSECURE(" + str(address) + ")")

    def address_isnonsecureex(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isNONSECUREEX(" + str(address) + ")")

    def address_offset(self, address: int) -> int:
        return self.__conn._fnc("ADDRESS.OFFSET(" + str(address) + ")")

    def address_isonchip(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isONCHIP(" + str(address) + ")")

    def address_isphysical(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isPHYSICAL(" + str(address) + ")")

    def address_isprogram(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isPROGRAM(" + str(address) + ")")

    def address_range_begin(self, addressrange: int) -> object:
        return self.__conn._fnc("ADDRESS.RANGE.BEGIN(" + str(addressrange) + ")")

    def address_range_end(self, addressrange: int) -> object:
        return self.__conn._fnc("ADDRESS.RANGE.END(" + str(addressrange) + ")")

    def address_range_size(self, addressrange: int) -> int:
        return self.__conn._fnc("ADDRESS.RANGE.SIZE(" + str(addressrange) + ")")

    def address_issecure(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isSECURE(" + str(address) + ")")

    def address_issecureex(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isSECUREEX(" + str(address) + ")")

    def address_ishypervisor(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isHYPERVISOR(" + str(address) + ")")

    def address_ishypervisorex(self, pAddrIn: int) -> bool:
        return self.__conn._fnc("ADDRESS.isHYPERVISOREX(" + str(pAddrIn) + ")")

    def address_isguest(self, address: int) -> bool:
        return self.__conn._fnc("ADDRESS.isGUEST(" + str(address) + ")")

    def address_isguestex(self, pAddrIn: int) -> bool:
        return self.__conn._fnc("ADDRESS.isGUESTEX(" + str(pAddrIn) + ")")

    def address_machineid(self, address: int) -> int:
        return self.__conn._fnc("ADDRESS.MACHINEID(" + str(address) + ")")

    def address_segment(self, address: int) -> int:
        return self.__conn._fnc("ADDRESS.SEGMENT(" + str(address) + ")")

    def address_straccess(self, address: int) -> str:
        return self.__conn._fnc("ADDRESS.STRACCESS(" + str(address) + ")")

    def address_track_data(self) -> object:
        return self.__conn._fnc("ADDRESS.TRACK.DATA()")

    def address_track_program(self) -> object:
        return self.__conn._fnc("ADDRESS.TRACK.PROGram()")

    def address_instr_len(self, address: int) -> int:
        return self.__conn._fnc("ADDRESS.INSTR.LEN(" + str(address) + ")")

    def address_mau(self, address: int) -> int:
        return self.__conn._fnc("ADDRESS.MAU(" + str(address) + ")")

    def access_ishypervisor(self, address: int) -> bool:
        return self.__conn._fnc("ACCESS.isHYPERVISOR(" + str(address) + ")")

    def access_ishypervisorex(self, pAddrIn: int) -> bool:
        return self.__conn._fnc("ACCESS.isHYPERVISOREX(" + str(pAddrIn) + ")")

    def access_isguest(self, address: int) -> bool:
        return self.__conn._fnc("ACCESS.isGUEST(" + str(address) + ")")

    def access_isguestex(self, pAddrIn: int) -> bool:
        return self.__conn._fnc("ACCESS.isGUESTEX(" + str(pAddrIn) + ")")

    def disassemble_address(self, address: int) -> str:
        return self.__conn._fnc("DISASSEMBLE.ADDRESS(" + str(address) + ")")

    def convert_addresstodualport(self, address: int) -> object:
        return self.__conn._fnc("CONVert.ADDRESSTODUALPORT(" + str(address) + ")")

    def convert_addresstononsecure(self, address: int) -> object:
        return self.__conn._fnc("CONVert.ADDRESSTONONSECURE(" + str(address) + ")")

    def convert_addresstosecure(self, address: int) -> object:
        return self.__conn._fnc("CONVert.ADDRESSTOSECURE(" + str(address) + ")")

    def convert_inttoaddress(self, poffset: int, psegment: int) -> object:
        return self.__conn._fnc(
            "CONVert.INTTOADDRESS(" + str(poffset) + ", " + str(psegment) + ")"
        )

    def convert_booltoint(self, bool: int) -> int:
        return self.__conn._fnc("CONVert.BOOLTOINT(" + str(bool) + ")")

    def convert_char(self, integer: int) -> int:
        return self.__conn._fnc("CONVert.CHAR(" + str(integer) + ")")

    def convert_floattoint(self, float: int) -> int:
        return self.__conn._fnc("CONVert.FLOATTOINT(" + str(float) + ")")

    def convert_hextoint(self, hex: int) -> int:
        return self.__conn._fnc("CONVert.HEXTOINT(" + str(hex) + ")")

    def convert_inttobool(self, bool: int) -> bool:
        return self.__conn._fnc("CONVert.INTTOBOOL(" + str(bool) + ")")

    def convert_inttofloat(self, integer: int) -> float:
        return self.__conn._fnc("CONVert.INTTOFLOAT(" + str(integer) + ")")

    def convert_inttohex(self, integer: int) -> int:
        return self.__conn._fnc("CONVert.INTTOHEX(" + str(integer) + ")")

    def convert_inttomask(self, mask: int, value: int) -> int:
        return self.__conn._fnc(
            "CONVert.INTTOMASK(" + str(mask) + ", " + str(value) + ")"
        )

    def convert_maskmtoint(self, mask_value: int) -> int:
        return self.__conn._fnc("CONVert.MASKMTOINT(" + str(mask_value) + ")")

    def convert_masktoint(self, value: int) -> int:
        return self.__conn._fnc("CONVert.MASKTOINT(" + str(value) + ")")

    def convert_octaltoint(self, string: int) -> int:
        return self.__conn._fnc("CONVert.OCTaltoint(" + str(string) + ")")

    def convert_signedbyte(self, value: int) -> int:
        return self.__conn._fnc("CONVert.SignedByte(" + str(value) + ")")

    def convert_signedlong(self, value: int) -> int:
        return self.__conn._fnc("CONVert.SignedLong(" + str(value) + ")")

    def convert_signedword(self, value: int) -> int:
        return self.__conn._fnc("CONVert.SignedWord(" + str(value) + ")")

    def convert_timemstoint(self, timevalue: int) -> int:
        return self.__conn._fnc("CONVert.TIMEMSTOINT(" + str(timevalue) + ")")

    def convert_timestoint(self, timevalue: int) -> int:
        return self.__conn._fnc("CONVert.TIMESTOINT(" + str(timevalue) + ")")

    def convert_timeustoint(self, timevalue: int) -> int:
        return self.__conn._fnc("CONVert.TIMEUSTOINT(" + str(timevalue) + ")")

    def convert_timenstoint(self, timevalue: int) -> int:
        return self.__conn._fnc("CONVert.TIMENSTOINT(" + str(timevalue) + ")")

    def convert_tolower(self, string: int) -> str:
        return self.__conn._fnc("CONVert.TOLOWER(" + str(string) + ")")

    def convert_toupper(self, string: int) -> str:
        return self.__conn._fnc("CONVert.TOUPPER(" + str(string) + ")")

    def selection_address(self) -> object:
        return self.__conn._fnc("SELECTION.ADDRESS()")

    def selection_string(self) -> str:
        return self.__conn._fnc("SELECTION.STRing()")

    def trans_logical_valid(self, physical_address: int) -> bool:
        return self.__conn._fnc("TRANS.LOGICAL.VALID(" + str(physical_address) + ")")

    def trans_physical(self, address: int) -> object:
        return self.__conn._fnc("TRANS.PHYSICAL(" + str(address) + ")")

    def trans_physicalex_valid(self, address: int) -> bool:
        return self.__conn._fnc("TRANS.PHYSICALEX.VALID(" + str(address) + ")")

    def trans_intermediate_valid(self, address: int) -> bool:
        return self.__conn._fnc("TRANS.INTERMEDIATE.VALID(" + str(address) + ")")

    def trans_intermediateex_valid(self, address: int) -> bool:
        return self.__conn._fnc("TRANS.INTERMEDIATEEX.VALID(" + str(address) + ")")

    def trans_linear_valid(self, address: int) -> bool:
        return self.__conn._fnc("TRANS.LINEAR.VALID(" + str(address) + ")")

    def trans_linearex_valid(self, address: int) -> bool:
        return self.__conn._fnc("TRANS.LINEAREX.VALID(" + str(address) + ")")

    def trans_enable(self) -> bool:
        return self.__conn._fnc("TRANS.ENABLE()")

    def trans_tablewalk(self) -> bool:
        return self.__conn._fnc("TRANS.TABLEWALK()")

    def file_type(self, file: int) -> str:
        return self.__conn._fnc("FILE.TYPE(" + str(file) + ")")

    def file_eof(self, file_number: int) -> bool:
        return self.__conn._fnc("FILE.EOF(" + str(file_number) + ")")

    def file_eoflastread(self) -> bool:
        return self.__conn._fnc("FILE.EOFLASTREAD()")

    def file_exist(self, file: int) -> bool:
        return self.__conn._fnc("FILE.EXIST(" + str(file) + ")")

    def file_open(self, file_number: int) -> bool:
        return self.__conn._fnc("FILE.OPEN(" + str(file_number) + ")")

    def file_sum(self) -> str:
        return self.__conn._fnc("FILE.SUM()")

    def tpu_long(self, paddr: int) -> int:
        return self.__conn._fnc("TPU.Long(" + str(paddr) + ")")

    def tpu_run(self) -> bool:
        return self.__conn._fnc("TPU.RUN()")

    def tpu_idle(self) -> bool:
        return self.__conn._fnc("TPU.IDLE()")

    def spe(self, register_name: int) -> int:
        return self.__conn._fnc("SPE(" + str(register_name) + ")")

    def vpu(self, register_name: int) -> int:
        return self.__conn._fnc("VPU(" + str(register_name) + ")")

    def vpucr(self, register: int) -> int:
        return self.__conn._fnc("VPUCR(" + str(register) + ")")

    def system_option_fastaccess(self) -> bool:
        return self.__conn._fnc("SYStem.Option.FASTACCESS()")

    def system_option_memorymodel(self) -> str:
        return self.__conn._fnc("SYStem.Option.MEMoryMODEL()")

    def system_option_swdcontrolstatus(self) -> int:
        return self.__conn._fnc("SYStem.Option.SWDCONTROLSTATUS()")

    def system_option_swdread(self, offset: int, apndp: int) -> int:
        return self.__conn._fnc(
            "SYStem.Option.SWDREAD(" + str(offset) + ", " + str(apndp) + ")"
        )

    def system_option_topology_sockets(self) -> int:
        return self.__conn._fnc("SYStem.Option.TOPOlogy.SOCKETS()")

    def system_option_mmuspaces(self) -> bool:
        return self.__conn._fnc("SYStem.Option.MMUSPACES()")

    def system_option_zonespaces(self) -> bool:
        return self.__conn._fnc("SYStem.Option.ZoneSPACES()")

    def system_option_machinespaces(self) -> bool:
        return self.__conn._fnc("SYStem.Option.MACHINESPACES()")

    def system_option_dualport(self) -> bool:
        return self.__conn._fnc("SYStem.Option.DUALPORT()")

    def system_detect_cltapchain(self) -> str:
        return self.__conn._fnc("SYStem.DETECT.CLTapchain()")

    def system_detect_stepping(self) -> int:
        return self.__conn._fnc("SYStem.DETECT.STEPping()")

    def system_readpdrl(self) -> int:
        return self.__conn._fnc("SYStem.ReadPDRL()")

    def system_readpdrh(self) -> int:
        return self.__conn._fnc("SYStem.ReadPDRH()")

    def system_corestates_phys(self, core: int) -> int:
        return self.__conn._fnc("SYStem.CoreStates.PHYS(" + str(core) + ")")

    def system_corestates_hyper(self, core: int) -> int:
        return self.__conn._fnc("SYStem.CoreStates.HYPER(" + str(core) + ")")

    def system_corestates_apic(self, core: int) -> int:
        return self.__conn._fnc("SYStem.CoreStates.APIC(" + str(core) + ")")

    def system_corestates_mode(self, core: int) -> str:
        return self.__conn._fnc("SYStem.CoreStates.MODE(" + str(core) + ")")

    def system_corestates_prior(self, core: int) -> str:
        return self.__conn._fnc("SYStem.CoreStates.PRIOR(" + str(core) + ")")

    def system_corestates_smm(self, core: int) -> str:
        return self.__conn._fnc("SYStem.CoreStates.SMM(" + str(core) + ")")

    def system_corestates_vmx(self, core: int) -> str:
        return self.__conn._fnc("SYStem.CoreStates.VMX(" + str(core) + ")")

    def system_config_pch(self) -> str:
        return self.__conn._fnc("SYStem.CONFIG.PCH()")

    def system_config_drpre(self, core_index: int) -> int:
        return self.__conn._fnc("SYStem.CONFIG.DRPRE(" + str(core_index) + ")")

    def system_config_drpost(self, core_index: int) -> int:
        return self.__conn._fnc("SYStem.CONFIG.DRPOST(" + str(core_index) + ")")

    def system_config_listcore(self, column_string: int, line_number: int) -> str:
        return self.__conn._fnc(
            "SYStem.CONFIG.ListCORE("
            + str(column_string)
            + ", "
            + str(line_number)
            + ")"
        )

    def system_config_listsim(self, column_string: int, line_number: int) -> str:
        return self.__conn._fnc(
            "SYStem.CONFIG.ListSIM("
            + str(column_string)
            + ", "
            + str(line_number)
            + ")"
        )

    def system_config_irpre(self, core_index: int) -> int:
        return self.__conn._fnc("SYStem.CONFIG.IRPRE(" + str(core_index) + ")")

    def system_config_irpost(self, core_index: int) -> int:
        return self.__conn._fnc("SYStem.CONFIG.IRPOST(" + str(core_index) + ")")

    def system_config_jtagtap(self, config_index: int, item: int) -> int:
        return self.__conn._fnc(
            "SYStem.CONFIG.JTAGTAP(" + str(config_index) + ", " + str(item) + ")"
        )

    def system_config_slave(self) -> bool:
        return self.__conn._fnc("SYStem.CONFIG.Slave()")

    def system_config_swdp(self) -> bool:
        return self.__conn._fnc("SYStem.CONFIG.SWDP()")

    def system_config_swdptargetid(self) -> int:
        return self.__conn._fnc("SYStem.CONFIG.SWDPTargetId()")

    def system_config_swdptargetsel(self) -> int:
        return self.__conn._fnc("SYStem.CONFIG.SWDPTargetSel()")

    def system_config_tapstate(self) -> int:
        return self.__conn._fnc("SYStem.CONFIG.TAPState()")

    def system_config_xcp_info_str(self, property: int) -> str:
        return self.__conn._fnc("SYStem.CONFIG.XCP.INFO.STR(" + str(property) + ")")

    def system_config_xcp_connectmode(self) -> str:
        return self.__conn._fnc("SYStem.CONFIG.XCP.ConnectMode()")

    def system_config_xcp_connected(self) -> bool:
        return self.__conn._fnc("SYStem.CONFIG.XCP.Connected()")

    def system_config_debugport(self) -> str:
        return self.__conn._fnc("SYStem.CONFIG.DEBUGPORT()")

    def system_config_debugporttype(self) -> str:
        return self.__conn._fnc("SYStem.CONFIG.DEBUGPORTTYPE()")

    def system_mmu(self) -> bool:
        return self.__conn._fnc("SYStem.MMU()")

    def system_cpu(self) -> str:
        return self.__conn._fnc("SYStem.CPU()")

    def system_access_denied(self) -> bool:
        return self.__conn._fnc("SYStem.ACCESS.DENIED()")

    def system_jtagclock(self) -> int:
        return self.__conn._fnc("SYStem.JtagClock()")

    def system_up_islocked(self) -> bool:
        return self.__conn._fnc("SYStem.Up.isLOCKED()")

    def system_traceext(self) -> bool:
        return self.__conn._fnc("SYStem.TRACEEXT()")

    def system_traceint(self) -> bool:
        return self.__conn._fnc("SYStem.TRACEINT()")

    def system_imaskasm(self) -> bool:
        return self.__conn._fnc("SYStem.IMASKASM()")

    def system_imaskhll(self) -> bool:
        return self.__conn._fnc("SYStem.IMASKHLL()")

    def system_bigendian(self) -> bool:
        return self.__conn._fnc("SYStem.BigEndian()")

    def system_littleendian(self) -> bool:
        return self.__conn._fnc("SYStem.LittleEndian()")

    def system_memaccess(self) -> str:
        return self.__conn._fnc("SYStem.MEMACCESS()")

    def system_mode(self) -> int:
        return self.__conn._fnc("SYStem.Mode()")

    def system_cadiconfig_remoteserver(self, key: int) -> str:
        return self.__conn._fnc("SYStem.CADIconfig.RemoteServer(" + str(key) + ")")

    def system_cadiconfig_traceconfig(self, pnumber: int) -> str:
        return self.__conn._fnc("SYStem.CADIconfig.Traceconfig(" + str(pnumber) + ")")

    def system_mcdconfig_library(self, key: int) -> str:
        return self.__conn._fnc("SYStem.MCDconfig.LIBrary(" + str(key) + ")")

    def system_dci_bssbclock(self, clock: int) -> int:
        return self.__conn._fnc("SYStem.DCI.BssbClock(" + str(clock) + ")")

    def system_dci_bridge(self) -> str:
        return self.__conn._fnc("SYStem.DCI.Bridge()")

    def system_dci_timeout(self, strParam: int) -> object:
        return self.__conn._fnc("SYStem.DCI.TimeOut(" + str(strParam) + ")")

    def system_usemask(self) -> int:
        return self.__conn._fnc("SYStem.USEMASK()")

    def system_usecore(self) -> int:
        return self.__conn._fnc("SYStem.USECORE()")

    def system_instance(self) -> int:
        return self.__conn._fnc("SYStem.INSTANCE()")

    def system_gtl_connected(self) -> bool:
        return self.__conn._fnc("SYStem.GTL.CONNECTED()")

    def system_gtl_libname(self) -> str:
        return self.__conn._fnc("SYStem.GTL.LIBname()")

    def system_gtl_vendorid(self) -> str:
        return self.__conn._fnc("SYStem.GTL.VENDORID()")

    def system_gtl_version(self) -> int:
        return self.__conn._fnc("SYStem.GTL.VERSION()")

    def system_gtl_pluginversion(self) -> int:
        return self.__conn._fnc("SYStem.GTL.PLUGINVERSION()")

    def system_gtl_callcounter(self) -> int:
        return self.__conn._fnc("SYStem.GTL.CALLCOUNTER()")

    def system_gtl_modelname(self, index: int) -> str:
        return self.__conn._fnc("SYStem.GTL.ModelNAME(" + str(index) + ")")

    def system_gtl_transactorname(self, index: int) -> str:
        return self.__conn._fnc("SYStem.GTL.TransactorNAME(" + str(index) + ")")

    def system_gtl_transactortype(self, index: int) -> str:
        return self.__conn._fnc("SYStem.GTL.TransactorTYPE(" + str(index) + ")")

    def system_adapter_fw_outdated(self, pNo: int) -> bool:
        return self.__conn._fnc("SYStem.ADAPTER.FW.OUTDATED(" + str(pNo) + ")")

    def system_baudrate(self) -> str:
        return self.__conn._fnc("SYStem.BAUDRATE()")

    def system_coreclock(self) -> int:
        return self.__conn._fnc("SYStem.CORECLOCK()")

    def system_oscclock(self) -> int:
        return self.__conn._fnc("SYStem.OSCCLOCK()")

    def system_opbt(self, pnumber: int) -> int:
        return self.__conn._fnc("SYStem.OPBT(" + str(pnumber) + ")")

    def system_opbt8(self, pnumber: int) -> int:
        return self.__conn._fnc("SYStem.OPBT8(" + str(pnumber) + ")")

    def system_ocdid(self, pnumber: int) -> int:
        return self.__conn._fnc("SYStem.OCDID(" + str(pnumber) + ")")

    def system_cfid(self, pnumber: int) -> int:
        return self.__conn._fnc("SYStem.CFID(" + str(pnumber) + ")")

    def system_dfid(self, pnumber: int) -> int:
        return self.__conn._fnc("SYStem.DFID(" + str(pnumber) + ")")

    def system_hook(self) -> int:
        return self.__conn._fnc("SYStem.HOOK()")

    def system_notrap(self) -> int:
        return self.__conn._fnc("SYStem.NOTRAP()")

    def system_dcfreeze(self) -> bool:
        return self.__conn._fnc("SYStem.DCFreeze()")

    def system_amba(self) -> bool:
        return self.__conn._fnc("SYStem.AMBA()")

    def system_resetbehavior(self) -> str:
        return self.__conn._fnc("SYStem.RESetBehavior()")

    def mmx(self, register_name: int) -> int:
        return self.__conn._fnc("MMX(" + str(register_name) + ")")

    def dpp(self, register: int) -> int:
        return self.__conn._fnc("DPP(" + str(register) + ")")

    def sse(self, register_name: int) -> int:
        return self.__conn._fnc("SSE(" + str(register_name) + ")")

    def avx(self, register_name: int) -> int:
        return self.__conn._fnc("AVX(" + str(register_name) + ")")

    def avx512(self, register_name: int) -> int:
        return self.__conn._fnc("AVX512(" + str(register_name) + ")")

    def idtl(self) -> int:
        return self.__conn._fnc("IDTL()")

    def idtb(self) -> int:
        return self.__conn._fnc("IDTB()")

    def gdtl(self) -> int:
        return self.__conn._fnc("GDTL()")

    def gdtb(self) -> int:
        return self.__conn._fnc("GDTB()")

    def tss(self) -> int:
        return self.__conn._fnc("TSS()")

    def vmx_guest(self) -> bool:
        return self.__conn._fnc("VMX.Guest()")

    def hvx(self, register_name: int) -> str:
        return self.__conn._fnc("HVX(" + str(register_name) + ")")

    def fxu(self, register_name: int) -> str:
        return self.__conn._fnc("FXU(" + str(register_name) + ")")

    def cpuflashtype(self) -> str:
        return self.__conn._fnc("CPUFLASHTYPE()")

    def cpu_basefamily(self) -> str:
        return self.__conn._fnc("CPU.BASEFAMILY()")

    def cpu_subfamily(self) -> str:
        return self.__conn._fnc("CPU.SUBFAMILY()")

    def cpu_pincount(self) -> str:
        return self.__conn._fnc("CPU.PINCOUNT()")

    def cpu_deviceid(self) -> int:
        return self.__conn._fnc("CPU.DEVICEID()")

    def cpu_address(self, section: int) -> object:
        return self.__conn._fnc("CPU.ADDRESS(" + str(section) + ")")

    def cpu_feature(self, feature_string: int) -> bool:
        return self.__conn._fnc("CPU.FEATURE(" + str(feature_string) + ")")

    def epoc_dataaddress(self) -> int:
        return self.__conn._fnc("EPOC.DATAADDRESS()")

    def epoc_entrypoint(self) -> int:
        return self.__conn._fnc("EPOC.ENTRYPOINT()")

    def epoc_textaddress(self) -> int:
        return self.__conn._fnc("EPOC.TEXTADDRESS()")

    def cp15(self, pregno: int) -> int:
        return self.__conn._fnc("CP15(" + str(pregno) + ")")

    def arm64(self) -> bool:
        return self.__conn._fnc("ARM64()")

    def armarchversion(self) -> int:
        return self.__conn._fnc("ARMARCHVERSION()")

    def smmu_baseaddress(self, smmu_name: int) -> object:
        return self.__conn._fnc("SMMU.BaseADDRESS(" + str(smmu_name) + ")")

    def smmu_streamid2smrg(self, streamid: int, smmu_name: int) -> int:
        return self.__conn._fnc(
            "SMMU.Streamid2SMRG(" + str(streamid) + ", " + str(smmu_name) + ")"
        )

    def nmf_isactive(self, instancespec: int) -> bool:
        return self.__conn._fnc("NMF.ISACTIVE(" + str(instancespec) + ")")

    def nmf_this(self, instancespec: int) -> int:
        return self.__conn._fnc("NMF.THIS(" + str(instancespec) + ")")

    def extended(self) -> bool:
        return self.__conn._fnc("EXTENDED()")

    def idcode(self, n: int) -> int:
        return self.__conn._fnc("IDCODE(" + str(n) + ")")

    def idcodenumber(self) -> int:
        return self.__conn._fnc("IDCODENUMBER()")

    def jtag_x7efuse_cntl(self) -> int:
        return self.__conn._fnc("JTAG.X7EFUSE.CNTL()")

    def jtag_x7efuse_dna(self) -> int:
        return self.__conn._fnc("JTAG.X7EFUSE.DNA()")

    def jtag_x7efuse_key(self) -> str:
        return self.__conn._fnc("JTAG.X7EFUSE.KEY()")

    def jtag_x7efuse_result(self) -> int:
        return self.__conn._fnc("JTAG.X7EFUSE.RESULT()")

    def jtag_x7efuse_user(self) -> int:
        return self.__conn._fnc("JTAG.X7EFUSE.USER()")

    def jtag_pin(self, signal_name: int) -> int:
        return self.__conn._fnc("JTAG.PIN(" + str(signal_name) + ")")

    def jtag_shift(self) -> int:
        return self.__conn._fnc("JTAG.SHIFT()")

    def jtag_ontrigger_state(self) -> int:
        return self.__conn._fnc("JTAG.ONTRIGGER.STATE()")

    def jtag_sequence_exist(self, seq_name: int) -> bool:
        return self.__conn._fnc("JTAG.SEQuence.EXIST(" + str(seq_name) + ")")

    def jtag_sequence_locked(self, seq_name: int) -> bool:
        return self.__conn._fnc("JTAG.SEQuence.LOCKED(" + str(seq_name) + ")")

    def jtag_sequence_result(self, global_seq_variable: int) -> int:
        return self.__conn._fnc(
            "JTAG.SEQuence.RESULT(" + str(global_seq_variable) + ")"
        )

    def bsdl_check_bypass(self) -> bool:
        return self.__conn._fnc("BSDL.CHECK.BYPASS()")

    def bsdl_check_flashconf(self) -> bool:
        return self.__conn._fnc("BSDL.CHECK.FLASHCONF()")

    def bsdl_check_idcode(self) -> bool:
        return self.__conn._fnc("BSDL.CHECK.IDCODE()")

    def bsdl_getdrbit(self, bit_number: int, chip_number: int) -> int:
        return self.__conn._fnc(
            "BSDL.GetDRBit(" + str(bit_number) + ", " + str(chip_number) + ")"
        )

    def bsdl_getportlevel(self, port_name: int, chip_number: int) -> int:
        return self.__conn._fnc(
            "BSDL.GetPortLevel(" + str(port_name) + ", " + str(chip_number) + ")"
        )

    def pci_read_b(self, register: int, function: int, device: int, bus: int) -> int:
        return self.__conn._fnc(
            "PCI.Read.B("
            + str(register)
            + ", "
            + str(function)
            + ", "
            + str(device)
            + ", "
            + str(bus)
            + ")"
        )

    def pci_read_l(self, register: int, function: int, device: int, bus: int) -> int:
        return self.__conn._fnc(
            "PCI.Read.L("
            + str(register)
            + ", "
            + str(function)
            + ", "
            + str(device)
            + ", "
            + str(bus)
            + ")"
        )

    def pci_read_w(self, register: int, function: int, device: int, bus: int) -> int:
        return self.__conn._fnc(
            "PCI.Read.W("
            + str(register)
            + ", "
            + str(function)
            + ", "
            + str(device)
            + ", "
            + str(bus)
            + ")"
        )

    def cpubondout(self) -> str:
        return self.__conn._fnc("CPUBONDOUT()")

    def cpucoreversion(self) -> str:
        return self.__conn._fnc("CPUCOREVERSION()")

    def cpufamily(self) -> str:
        return self.__conn._fnc("CPUFAMILY()")

    def coretype(self) -> int:
        return self.__conn._fnc("CORETYPE()")

    def trims08fll(self, frequency_in_KHz: int) -> int:
        return self.__conn._fnc("TRIMS08FLL(" + str(frequency_in_KHz) + ")")

    def cpuis(self, search_string: int) -> bool:
        return self.__conn._fnc("CPUIS(" + str(search_string) + ")")

    def cpuis64bit(self) -> bool:
        return self.__conn._fnc("CPUIS64BIT()")

    def monitor(self) -> bool:
        return self.__conn._fnc("MONITOR()")

    def icefamily(self) -> str:
        return self.__conn._fnc("ICEFAMILY()")

    def state_run(self) -> bool:
        return self.__conn._fnc("STATE.RUN()")

    def state_monitor_run(self) -> bool:
        return self.__conn._fnc("STATE.MONITOR.RUN()")

    def state_reset(self) -> bool:
        return self.__conn._fnc("STATE.RESET()")

    def state_power(self) -> bool:
        return self.__conn._fnc("STATE.POWER()")

    def state_halt(self) -> bool:
        return self.__conn._fnc("STATE.HALT()")

    def state_processor(self) -> str:
        return self.__conn._fnc("STATE.PROCESSOR()")

    def state_target(self) -> str:
        return self.__conn._fnc("STATE.TARGET()")

    def state_oslk(self) -> bool:
        return self.__conn._fnc("STATE.OSLK()")

    def core_isactive(self, core: int) -> bool:
        return self.__conn._fnc("CORE.ISACTIVE(" + str(core) + ")")

    def core_isassigned(self, core_number: int) -> bool:
        return self.__conn._fnc("CORE.ISASSIGNED(" + str(core_number) + ")")

    def core_logicaltophysical(self, core_number: int) -> int:
        return self.__conn._fnc("CORE.LOGICALTOPHYSICAL(" + str(core_number) + ")")

    def core_names(self, index: int) -> str:
        return self.__conn._fnc("CORE.NAMES(" + str(index) + ")")

    def core_number(self) -> int:
        return self.__conn._fnc("CORE.NUMBER()")

    def core_physicaltological(self, core_number: int) -> int:
        return self.__conn._fnc("CORE.PHYSICALTOLOGICAL(" + str(core_number) + ")")

    def confignumber(self) -> int:
        return self.__conn._fnc("CONFIGNUMBER()")

    def corename(self) -> str:
        return self.__conn._fnc("CORENAME()")

    def debugmode(self) -> str:
        return self.__conn._fnc("DEBUGMODE()")

    def interface_cadi(self) -> bool:
        return self.__conn._fnc("INTERFACE.CADI()")

    def interface_gdb(self) -> bool:
        return self.__conn._fnc("INTERFACE.GDB()")

    def interface_host(self) -> bool:
        return self.__conn._fnc("INTERFACE.HOST()")

    def interface_iris(self) -> bool:
        return self.__conn._fnc("INTERFACE.IRIS()")

    def interface_mcd(self) -> bool:
        return self.__conn._fnc("INTERFACE.MCD()")

    def interface_name(self) -> str:
        return self.__conn._fnc("INTERFACE.NAME()")

    def interface_qnx(self) -> bool:
        return self.__conn._fnc("INTERFACE.QNX()")

    def interface_sim(self) -> bool:
        return self.__conn._fnc("INTERFACE.SIM()")

    def interface_vast(self) -> bool:
        return self.__conn._fnc("INTERFACE.VAST()")

    def interface_vdi(self) -> bool:
        return self.__conn._fnc("INTERFACE.VDI()")

    def interface_gdi(self) -> bool:
        return self.__conn._fnc("interface.GDI()")

    def interface_hostmci(self) -> bool:
        return self.__conn._fnc("interface.HOSTMCI()")

    def interface_das(self) -> bool:
        return self.__conn._fnc("interface.DAS()")

    def pbi(self) -> str:
        return self.__conn._fnc("PBI()")

    def flash_list_type(self, address: int) -> str:
        return self.__conn._fnc("FLASH.List.TYPE(" + str(address) + ")")

    def flash_list_state_pending(self) -> int:
        return self.__conn._fnc("FLASH.List.STATE.PENDING()")

    def flash_cfi_size(self, bus_width: int, address: int) -> int:
        return self.__conn._fnc(
            "FLASH.CFI.SIZE(" + str(bus_width) + ", " + str(address) + ")"
        )

    def flash_cfi_width(self, address: int) -> str:
        return self.__conn._fnc("FLASH.CFI.WIDTH(" + str(address) + ")")

    def flash_id(self, id_type: int) -> int:
        return self.__conn._fnc("FLASH.ID(" + str(id_type) + ")")

    def flash_clock_frequency(self) -> int:
        return self.__conn._fnc("FLASH.CLocK.Frequency()")

    def flash_programmode_option(self) -> str:
        return self.__conn._fnc("FLASH.ProgramMODE.OPTION()")

    def flash_sector_begin(self, address: int) -> object:
        return self.__conn._fnc("FLASH.SECTOR.BEGIN(" + str(address) + ")")

    def flash_sector_end(self, address: int) -> object:
        return self.__conn._fnc("FLASH.SECTOR.END(" + str(address) + ")")

    def flash_sector_range(self, address: int) -> object:
        return self.__conn._fnc("FLASH.SECTOR.RANGE(" + str(address) + ")")

    def flash_sector_exist(self, address: int) -> bool:
        return self.__conn._fnc("FLASH.SECTOR.EXIST(" + str(address) + ")")

    def flash_sector_next(self, address: int) -> object:
        return self.__conn._fnc("FLASH.SECTOR.NEXT(" + str(address) + ")")

    def flash_sector_size(self, address: int) -> int:
        return self.__conn._fnc("FLASH.SECTOR.SIZE(" + str(address) + ")")

    def flash_sector_state(self, address: int) -> str:
        return self.__conn._fnc("FLASH.SECTOR.STATE(" + str(address) + ")")

    def flash_sector_type(self, address: int) -> str:
        return self.__conn._fnc("FLASH.SECTOR.TYPE(" + str(address) + ")")

    def flash_sector_width(self, address: int) -> str:
        return self.__conn._fnc("FLASH.SECTOR.WIDTH(" + str(address) + ")")

    def flash_sector_extravalue(self, address: int) -> int:
        return self.__conn._fnc("FLASH.SECTOR.EXTRAvalue(" + str(address) + ")")

    def flash_sector_otp(self, address: int) -> bool:
        return self.__conn._fnc("FLASH.SECTOR.OTP(" + str(address) + ")")

    def flash_sector_option(self, option: int, address: int) -> str:
        return self.__conn._fnc(
            "FLASH.SECTOR.OPTION(" + str(option) + ", " + str(address) + ")"
        )

    def flash_target_build(self, file: int) -> int:
        return self.__conn._fnc("FLASH.TARGET.BUILD(" + str(file) + ")")

    def flash_target_file(self) -> str:
        return self.__conn._fnc("FLASH.TARGET.FILE()")

    def flash_target_coderange(self) -> object:
        return self.__conn._fnc("FLASH.TARGET.CODERANGE()")

    def flash_target_datarange(self) -> object:
        return self.__conn._fnc("FLASH.TARGET.DATARANGE()")

    def flash_target2_file(self) -> str:
        return self.__conn._fnc("FLASH.TARGET2.FILE()")

    def flash_target2_coderange(self) -> object:
        return self.__conn._fnc("FLASH.TARGET2.CODERANGE()")

    def flash_target2_datarange(self) -> object:
        return self.__conn._fnc("FLASH.TARGET2.DATARANGE()")

    def flash_unit_begin(self, unit: int) -> object:
        return self.__conn._fnc("FLASH.UNIT.BEGIN(" + str(unit) + ")")

    def flash_unit_end(self, unit: int) -> object:
        return self.__conn._fnc("FLASH.UNIT.END(" + str(unit) + ")")

    def flash_unit_exist(self, unit: int) -> bool:
        return self.__conn._fnc("FLASH.UNIT.EXIST(" + str(unit) + ")")

    def flash_unit_next(self, unit: int) -> int:
        return self.__conn._fnc("FLASH.UNIT.NEXT(" + str(unit) + ")")

    def flashfile_spareaddress(self, address: int) -> int:
        return self.__conn._fnc("FLASHFILE.SPAREADDRESS(" + str(address) + ")")

    def flashfile_getbadblock_count(self) -> int:
        return self.__conn._fnc("FLASHFILE.GETBADBLOCK.COUNT()")

    def flashfile_getbadblock_next(self) -> int:
        return self.__conn._fnc("FLASHFILE.GETBADBLOCK.NEXT()")

    def autofocus_frequency(self) -> int:
        return self.__conn._fnc("AUTOFOCUS.FREQUENCY()")

    def autofocus_ok(self) -> bool:
        return self.__conn._fnc("AUTOFOCUS.OK()")

    def flag_read(self, address_range: int) -> int:
        return self.__conn._fnc("FLAG.READ(" + str(address_range) + ")")

    def flag_write(self, address_range: int) -> int:
        return self.__conn._fnc("FLAG.WRITE(" + str(address_range) + ")")

    def macho_lastuuid(self) -> str:
        return self.__conn._fnc("MACHO.LASTUUID()")

    def var_address(self, hll_expression: int) -> object:
        return self.__conn._fnc("Var.ADDRESS(" + str(hll_expression) + ")")

    def var_bitpos(self, hll_expression: int) -> int:
        return self.__conn._fnc("Var.BITPOS(" + str(hll_expression) + ")")

    def var_bitsize(self, hll_expression: int) -> int:
        return self.__conn._fnc("Var.BITSIZE(" + str(hll_expression) + ")")

    def var_end(self, hll_expression: int) -> object:
        return self.__conn._fnc("Var.END(" + str(hll_expression) + ")")

    def var_exist(self, hll_expression: int) -> bool:
        return self.__conn._fnc("Var.EXIST(" + str(hll_expression) + ")")

    def var_fvalue(self, hll_expression: int) -> float:
        return self.__conn._fnc("Var.FVALUE(" + str(hll_expression) + ")")

    def var_isbit(self, hll_expression: int) -> bool:
        return self.__conn._fnc("Var.ISBIT(" + str(hll_expression) + ")")

    def var_isregister(self, path: int) -> bool:
        return self.__conn._fnc("Var.ISREGISTER(" + str(path) + ")")

    def var_isstack(self, path: int) -> bool:
        return self.__conn._fnc("Var.ISSTACK(" + str(path) + ")")

    def var_isstatic(self, path: int) -> bool:
        return self.__conn._fnc("Var.ISSTATIC(" + str(path) + ")")

    def var_range(self, hll_expression: int) -> object:
        return self.__conn._fnc("Var.RANGE(" + str(hll_expression) + ")")

    def var_register(self, path: int) -> str:
        return self.__conn._fnc("Var.REGISTER(" + str(path) + ")")

    def var_sizeof(self, hll_expression: int) -> int:
        return self.__conn._fnc("Var.SIZEOF(" + str(hll_expression) + ")")

    def var_string(self, hll_expression: int) -> str:
        return self.__conn._fnc("Var.STRing(" + str(hll_expression) + ")")

    def var_typeof(self, hll_expression: int) -> str:
        return self.__conn._fnc("Var.TYPEOF(" + str(hll_expression) + ")")

    def var_value(self, hll_expression: int) -> int:
        return self.__conn._fnc("Var.VALUE(" + str(hll_expression) + ")")

    def symbol_attribute(self, paddr: int) -> int:
        return self.__conn._fnc("sYmbol.ATTRIBUTE(" + str(paddr) + ")")

    def symbol_autoload_check(self) -> str:
        return self.__conn._fnc("sYmbol.AutoLOAD.CHECK()")

    def symbol_autoload_checkcmd(self) -> str:
        return self.__conn._fnc("sYmbol.AutoLOAD.CHECKCMD()")

    def symbol_autoload_config(self) -> str:
        return self.__conn._fnc("sYmbol.AutoLOAD.CONFIG()")

    def symbol_begin(self, symbol: int) -> object:
        return self.__conn._fnc("sYmbol.BEGIN(" + str(symbol) + ")")

    def symbol_count(self, symbol: int) -> int:
        return self.__conn._fnc("sYmbol.COUNT(" + str(symbol) + ")")

    def symbol_end(self, symbol: int) -> object:
        return self.__conn._fnc("sYmbol.END(" + str(symbol) + ")")

    def symbol_epilog(self, symbol: int) -> object:
        return self.__conn._fnc("sYmbol.EPILOG(" + str(symbol) + ")")

    def symbol_exist(self, symbol: int) -> bool:
        return self.__conn._fnc("sYmbol.EXIST(" + str(symbol) + ")")

    def symbol_exit(self, symbol: int) -> object:
        return self.__conn._fnc("sYmbol.EXIT(" + str(symbol) + ")")

    def symbol_function(self, address: int) -> str:
        return self.__conn._fnc("sYmbol.FUNCTION(" + str(address) + ")")

    def symbol_import(self) -> str:
        return self.__conn._fnc("sYmbol.IMPORT()")

    def symbol_isregister(self, path: int) -> bool:
        return self.__conn._fnc("sYmbol.ISREGISTER(" + str(path) + ")")

    def symbol_isstack(self, path: int) -> bool:
        return self.__conn._fnc("sYmbol.ISSTACK(" + str(path) + ")")

    def symbol_isstatic(self, path: int) -> bool:
        return self.__conn._fnc("sYmbol.ISSTATIC(" + str(path) + ")")

    def symbol_list_map_begin(self, index: int) -> object:
        return self.__conn._fnc("sYmbol.List.MAP.BEGIN(" + str(index) + ")")

    def symbol_list_map_count(self) -> int:
        return self.__conn._fnc("sYmbol.List.MAP.COUNT()")

    def symbol_list_map_end(self, index: int) -> object:
        return self.__conn._fnc("sYmbol.List.MAP.END(" + str(index) + ")")

    def symbol_list_map_range(self, index: int) -> object:
        return self.__conn._fnc("sYmbol.List.MAP.RANGE(" + str(index) + ")")

    def symbol_list_program(self, StartOver: int) -> str:
        return self.__conn._fnc("sYmbol.List.PROGRAM(" + str(StartOver) + ")")

    def symbol_list_source(
        self, LoadAll: int, OnlyExisting: int, StartOver: int
    ) -> str:
        return self.__conn._fnc(
            "sYmbol.List.SOURCE("
            + str(LoadAll)
            + ", "
            + str(OnlyExisting)
            + ", "
            + str(StartOver)
            + ")"
        )

    def symbol_loadedbytes(self) -> int:
        return self.__conn._fnc("sYmbol.LOADEDBYTES()")

    def symbol_matches(self) -> int:
        return self.__conn._fnc("sYmbol.MATCHES()")

    def symbol_name_at(self, context_address: int, address: int) -> str:
        return self.__conn._fnc(
            "sYmbol.NAME.AT(" + str(context_address) + ", " + str(address) + ")"
        )

    def symbol_next_begin(self, symbol: int) -> object:
        return self.__conn._fnc("sYmbol.NEXT.BEGIN(" + str(symbol) + ")")

    def symbol_prange(self, symbol: int) -> object:
        return self.__conn._fnc("sYmbol.PRANGE(" + str(symbol) + ")")

    def symbol_range(self, symbol: int) -> object:
        return self.__conn._fnc("sYmbol.RANGE(" + str(symbol) + ")")

    def symbol_register(self, path: int) -> str:
        return self.__conn._fnc("sYmbol.REGISTER(" + str(path) + ")")

    def symbol_searchfile(self, file: int) -> str:
        return self.__conn._fnc("sYmbol.SEARCHFILE(" + str(file) + ")")

    def symbol_secaddress(self, section: int) -> object:
        return self.__conn._fnc("sYmbol.SECADDRESS(" + str(section) + ")")

    def symbol_secend(self, section: int) -> object:
        return self.__conn._fnc("sYmbol.SECEND(" + str(section) + ")")

    def symbol_secname(self, address: int) -> str:
        return self.__conn._fnc("sYmbol.SECNAME(" + str(address) + ")")

    def symbol_secprange(self, section: int) -> object:
        return self.__conn._fnc("sYmbol.SECPRANGE(" + str(section) + ")")

    def symbol_secrange(self, section: int) -> object:
        return self.__conn._fnc("sYmbol.SECRANGE(" + str(section) + ")")

    def symbol_sizeof(self, symbol: int) -> int:
        return self.__conn._fnc("sYmbol.SIZEOF(" + str(symbol) + ")")

    def symbol_sourcefile(self, address: int) -> str:
        return self.__conn._fnc("sYmbol.SOURCEFILE(" + str(address) + ")")

    def symbol_sourceline(self, address: int) -> int:
        return self.__conn._fnc("sYmbol.SOURCELINE(" + str(address) + ")")

    def symbol_sourcepath(self, directory_path: int) -> bool:
        return self.__conn._fnc("sYmbol.SOURCEPATH(" + str(directory_path) + ")")

    def symbol_state(self, name: int) -> str:
        return self.__conn._fnc("sYmbol.STATE(" + str(name) + ")")

    def symbol_type(self, symbol: int) -> int:
        return self.__conn._fnc("sYmbol.TYPE(" + str(symbol) + ")")

    def symbol_varname(self, address: int) -> str:
        return self.__conn._fnc("sYmbol.VARNAME(" + str(address) + ")")

    def coverage_bdone(self, address_range: int) -> int:
        return self.__conn._fnc("COVerage.BDONE(" + str(address_range) + ")")

    def coverage_scope(self, address_range: int) -> int:
        return self.__conn._fnc("COVerage.SCOPE(" + str(address_range) + ")")

    def coverage_sourcemetric(self) -> str:
        return self.__conn._fnc("COVerage.SourceMetric()")

    def coverage_treewalk(self, action: int) -> str:
        return self.__conn._fnc("COVerage.TreeWalk(" + str(action) + ")")

    def group_exist(self, group_name: int) -> bool:
        return self.__conn._fnc("GROUP.EXIST(" + str(group_name) + ")")

    def vco(self) -> int:
        return self.__conn._fnc("VCO()")

    def count_frequency(self) -> int:
        return self.__conn._fnc("Count.Frequency()")

    def count_level(self) -> int:
        return self.__conn._fnc("Count.LEVEL()")

    def count_time(self) -> object:
        return self.__conn._fnc("Count.Time()")

    def count_value(self) -> int:
        return self.__conn._fnc("Count.VALUE()")

    def analyzer_config_ecc8(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.ECC8()")

    def analyzer_config_fec(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.FEC()")

    def analyzer_config_ha120(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.HA120()")

    def analyzer_config_hac(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.HAC()")

    def analyzer_config_powertrace(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.POWERTRACE()")

    def analyzer_config_powertrace2(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.POWERTRACE2()")

    def analyzer_config_powertraceserial(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.POWERTRACESERIAL()")

    def analyzer_config_risctrace(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.RISCTRACE()")

    def analyzer_config_sa120(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.SA120()")

    def analyzer_config_stu(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.STU()")

    def analyzer_config_tsu(self) -> bool:
        return self.__conn._fnc("Analyzer.CONFIG.TSU()")

    def analyzer_counter_event(self, counter_name: int) -> int:
        return self.__conn._fnc("Analyzer.COUNTER.EVENT(" + str(counter_name) + ")")

    def analyzer_counter_extern(self, counter_name: int) -> int:
        return self.__conn._fnc("Analyzer.COUNTER.EXTERN(" + str(counter_name) + ")")

    def analyzer_counter_time(self, counter_name: int) -> object:
        return self.__conn._fnc("Analyzer.COUNTER.TIME(" + str(counter_name) + ")")

    def analyzer_dsel(self) -> str:
        return self.__conn._fnc("Analyzer.DSEL()")

    def analyzer_flag(self, flag_name: int) -> bool:
        return self.__conn._fnc("Analyzer.FLAG(" + str(flag_name) + ")")

    def analyzer_flow_errors(self) -> int:
        return self.__conn._fnc("Analyzer.FLOW.ERRORS()")

    def analyzer_flow_fifofull(self) -> int:
        return self.__conn._fnc("Analyzer.FLOW.FIFOFULL()")

    def analyzer_ischannelup(self) -> bool:
        return self.__conn._fnc("Analyzer.ISCHANNELUP()")

    def analyzer_access_vm(self) -> bool:
        return self.__conn._fnc("Analyzer.ACCESS.VM()")

    def analyzer_first(self) -> int:
        return self.__conn._fnc("Analyzer.FIRST()")

    def analyzer_maxsize(self) -> int:
        return self.__conn._fnc("Analyzer.MAXSIZE()")

    def analyzer_mode_flow(self) -> bool:
        return self.__conn._fnc("Analyzer.MODE.FLOW()")

    def analyzer_pc(self) -> int:
        return self.__conn._fnc("Analyzer.PC()")

    def analyzer_pcie_config(self, register_field: int) -> int:
        return self.__conn._fnc("Analyzer.PCIE.CONFIG(" + str(register_field) + ")")

    def analyzer_pcie_isconfigured(self) -> bool:
        return self.__conn._fnc("Analyzer.PCIE.ISCONFIGURED()")

    def analyzer_pcie_islinkup(self) -> bool:
        return self.__conn._fnc("Analyzer.PCIE.ISLINKUP()")

    def analyzer_pcie_register(self, register_offset: int) -> int:
        return self.__conn._fnc(
            "Analyzer.PCIE.Register(" + str(register_offset) + ")"
        )

    def analyzer_record_address(self, record_number: int) -> object:
        return self.__conn._fnc("Analyzer.RECORD.ADDRESS(" + str(record_number) + ")")

    def analyzer_record_data(self, record_number: int) -> int:
        return self.__conn._fnc("Analyzer.RECORD.DATA(" + str(record_number) + ")")

    def analyzer_record_offset(self, record_number: int) -> int:
        return self.__conn._fnc("Analyzer.RECORD.OFFSET(" + str(record_number) + ")")

    def analyzer_record_time(self, record_number: int) -> object:
        return self.__conn._fnc("Analyzer.RECORD.TIME(" + str(record_number) + ")")

    def analyzer_records(self) -> int:
        return self.__conn._fnc("Analyzer.RECORDS()")

    def analyzer_ref(self) -> int:
        return self.__conn._fnc("Analyzer.REF()")

    def analyzer_size(self) -> int:
        return self.__conn._fnc("Analyzer.SIZE()")

    def analyzer_state(self) -> int:
        return self.__conn._fnc("Analyzer.STATE()")

    def analyzer_traceconnect(self) -> str:
        return self.__conn._fnc("Analyzer.TraceCONNECT()")

    def analyzer_track_record(self) -> int:
        return self.__conn._fnc("Analyzer.TRACK.RECORD()")

    def analyzer_trigger_a(self) -> int:
        return self.__conn._fnc("Analyzer.TRIGGER.A()")

    def analyzer_trigger_b(self) -> int:
        return self.__conn._fnc("Analyzer.TRIGGER.B()")

    def analyzer_trigger_time(self) -> object:
        return self.__conn._fnc("Analyzer.TRIGGER.TIME()")

    def analyzer_focus_eye(
        self, n: int, am: int, tm: int, c_voltage: int, c_time: int, channel: int
    ) -> int:
        return self.__conn._fnc(
            "Analyzer.FOCUS.EYE("
            + str(n)
            + ", "
            + str(am)
            + ", "
            + str(tm)
            + ", "
            + str(c_voltage)
            + ", "
            + str(c_time)
            + ", "
            + str(channel)
            + ")"
        )

    def analyzer_threshold(self) -> float:
        return self.__conn._fnc("Analyzer.THRESHOLD()")

    def analyzer_proberevision(self) -> int:
        return self.__conn._fnc("Analyzer.PROBEREVISION()")

    def analyzer_min(self) -> object:
        return self.__conn._fnc("Analyzer.MIN()")

    def analyzer_max(self) -> object:
        return self.__conn._fnc("Analyzer.MAX()")

    def step_diverge_reachedtarget(self, paddr: int) -> bool:
        return self.__conn._fnc("Step.Diverge.ReachedTarget(" + str(paddr) + ")")

    def rts_error(self) -> bool:
        return self.__conn._fnc("RTS.ERROR()")

    def rts_nocode(self) -> bool:
        return self.__conn._fnc("RTS.NOCODE()")

    def rts_fifofull(self) -> bool:
        return self.__conn._fnc("RTS.FIFOFULL()")

    def rts_record(self) -> int:
        return self.__conn._fnc("RTS.RECORD()")

    def rts_records(self) -> int:
        return self.__conn._fnc("RTS.RECORDS()")

    def art_first(self) -> int:
        return self.__conn._fnc("ART.FIRST()")

    def art_maxsize(self) -> int:
        return self.__conn._fnc("ART.MAXSIZE()")

    def art_mode(self) -> int:
        return self.__conn._fnc("ART.MODE()")

    def art_record_address(self, record_number: int) -> object:
        return self.__conn._fnc("ART.RECORD.ADDRESS(" + str(record_number) + ")")

    def art_record_offset(self, record_number: int) -> int:
        return self.__conn._fnc("ART.RECORD.OFFSET(" + str(record_number) + ")")

    def art_record_time(self, record_number: int) -> object:
        return self.__conn._fnc("ART.RECORD.TIME(" + str(record_number) + ")")

    def art_records(self) -> int:
        return self.__conn._fnc("ART.RECORDS()")

    def art_ref(self) -> int:
        return self.__conn._fnc("ART.REF()")

    def art_size(self) -> int:
        return self.__conn._fnc("ART.SIZE()")

    def art_state(self) -> int:
        return self.__conn._fnc("ART.STATE()")

    def art_track_record(self) -> int:
        return self.__conn._fnc("ART.TRACK.RECORD()")

    def portanalyzer(self) -> bool:
        return self.__conn._fnc("PORTANALYZER()")

    def port_get(self, channel_name: int) -> int:
        return self.__conn._fnc("PORT.GET(" + str(channel_name) + ")")

    def port_maxsize(self) -> int:
        return self.__conn._fnc("PORT.MAXSIZE()")

    def port_records(self) -> int:
        return self.__conn._fnc("PORT.RECORDS()")

    def port_ref(self) -> int:
        return self.__conn._fnc("PORT.REF()")

    def port_size(self) -> int:
        return self.__conn._fnc("PORT.SIZE()")

    def port_state(self) -> int:
        return self.__conn._fnc("PORT.STATE()")

    def port_track_record(self) -> int:
        return self.__conn._fnc("PORT.TRACK.RECORD()")

    def probe_counter_event(self, p_countername: int) -> int:
        return self.__conn._fnc("Probe.COUNTER.EVENT(" + str(p_countername) + ")")

    def probe_counter_extern(self, p_countername: int) -> int:
        return self.__conn._fnc("Probe.COUNTER.EXTERN(" + str(p_countername) + ")")

    def probe_counter_time(self, p_countername: int) -> object:
        return self.__conn._fnc("Probe.COUNTER.TIME(" + str(p_countername) + ")")

    def probe_first(self) -> int:
        return self.__conn._fnc("Probe.FIRST()")

    def probe_flag(self, p_flagname: int) -> bool:
        return self.__conn._fnc("Probe.FLAG(" + str(p_flagname) + ")")

    def probe_maxsize(self) -> int:
        return self.__conn._fnc("Probe.MAXSIZE()")

    def probe_record_data(self, portname: int, precord: int) -> int:
        return self.__conn._fnc(
            "Probe.RECORD.DATA(" + str(portname) + ", " + str(precord) + ")"
        )

    def probe_record_time(self, precord: int) -> object:
        return self.__conn._fnc("Probe.RECORD.TIME(" + str(precord) + ")")

    def probe_size(self) -> int:
        return self.__conn._fnc("Probe.SIZE()")

    def probe_get(self, channel_name: int) -> int:
        return self.__conn._fnc("PROBE.GET(" + str(channel_name) + ")")

    def probe_records(self) -> int:
        return self.__conn._fnc("PROBE.RECORDS()")

    def probe_ref(self) -> int:
        return self.__conn._fnc("PROBE.REF()")

    def probe_state(self) -> int:
        return self.__conn._fnc("PROBE.STATE()")

    def probe_track_record(self) -> int:
        return self.__conn._fnc("PROBE.TRACK.RECORD()")

    def hardware_esi(self) -> bool:
        return self.__conn._fnc("hardware.ESI()")

    def hardware_fire(self) -> bool:
        return self.__conn._fnc("hardware.FIRE()")

    def hardware_icd(self) -> bool:
        return self.__conn._fnc("hardware.ICD()")

    def hardware_ice(self) -> bool:
        return self.__conn._fnc("hardware.ICE()")

    def hardware_powerdebug(self) -> bool:
        return self.__conn._fnc("hardware.POWERDEBUG()")

    def hardware_powernexus(self) -> bool:
        return self.__conn._fnc("hardware.POWERNEXUS()")

    def hardware_powerprobe(self) -> bool:
        return self.__conn._fnc("hardware.POWERPROBE()")

    def hardware_powertrace(self) -> bool:
        return self.__conn._fnc("hardware.POWERTRACE()")

    def hardware_powertracepx(self) -> bool:
        return self.__conn._fnc("hardware.POWERTRACEPX()")

    def hardware_powertrace2(self) -> bool:
        return self.__conn._fnc("hardware.POWERTRACE2()")

    def hardware_powertraceserial(self) -> bool:
        return self.__conn._fnc("hardware.POWERTRACESERIAL()")

    def hardware_combiprobe(self) -> bool:
        return self.__conn._fnc("hardware.COMBIPROBE()")

    def hardware_powerintegrator(self) -> bool:
        return self.__conn._fnc("hardware.POWERINTEGRATOR()")

    def hardware_powerintegrator2(self) -> bool:
        return self.__conn._fnc("hardware.POWERINTEGRATOR2()")

    def hardware_utrace(self) -> bool:
        return self.__conn._fnc("hardware.UTRACE()")

    def hardware_lcp(self) -> bool:
        return self.__conn._fnc("hardware.LCP()")

    def hardware_scu(self) -> bool:
        return self.__conn._fnc("hardware.SCU()")

    def hardware_stg(self) -> bool:
        return self.__conn._fnc("hardware.STG()")

    def hardware_ta32(self) -> bool:
        return self.__conn._fnc("hardware.TA32()")

    def iprobe_adc_enable(self, channel: int) -> bool:
        return self.__conn._fnc("IProbe.ADC.ENABLE(" + str(channel) + ")")

    def iprobe_adc_shunt(self, channel: int) -> float:
        return self.__conn._fnc("IProbe.ADC.SHUNT(" + str(channel) + ")")

    def iprobe_analog(self) -> bool:
        return self.__conn._fnc("IProbe.ANALOG()")

    def iprobe_first(self) -> int:
        return self.__conn._fnc("IProbe.FIRST()")

    def iprobe_get(self, channel_name: int) -> int:
        return self.__conn._fnc("IProbe.GET(" + str(channel_name) + ")")

    def iprobe_maxsize(self) -> int:
        return self.__conn._fnc("IProbe.MAXSIZE()")

    def iprobe_probe(self) -> bool:
        return self.__conn._fnc("IProbe.PROBE()")

    def iprobe_record_data(self, channel: int, record_number: int) -> int:
        return self.__conn._fnc(
            "IProbe.RECORD.DATA(" + str(channel) + ", " + str(record_number) + ")"
        )

    def iprobe_record_time(self, record_number: int) -> object:
        return self.__conn._fnc("IProbe.RECORD.TIME(" + str(record_number) + ")")

    def iprobe_records(self) -> int:
        return self.__conn._fnc("IProbe.RECORDS()")

    def iprobe_ref(self) -> int:
        return self.__conn._fnc("IProbe.REF()")

    def iprobe_size(self) -> int:
        return self.__conn._fnc("IProbe.SIZE()")

    def iprobe_state(self) -> int:
        return self.__conn._fnc("IProbe.STATE()")

    def iprobe_track_record(self) -> int:
        return self.__conn._fnc("IProbe.TRACK.RECORD()")

    def canalyzer_bothcables(self) -> bool:
        return self.__conn._fnc("CAnalyzer.BOTHCables()")

    def canalyzer_cabletype(self, connector: int) -> int:
        return self.__conn._fnc("CAnalyzer.CableTYPE(" + str(connector) + ")")

    def canalyzer_debugcable(self) -> str:
        return self.__conn._fnc("CAnalyzer.DebugCable()")

    def canalyzer_exportclock(self) -> int:
        return self.__conn._fnc("CAnalyzer.ExportCLOCK()")

    def canalyzer_feature(self, strParam: int) -> bool:
        return self.__conn._fnc("CAnalyzer.FEATURE(" + str(strParam) + ")")

    def canalyzer_first(self) -> int:
        return self.__conn._fnc("CAnalyzer.FIRST()")

    def canalyzer_maxsize(self) -> int:
        return self.__conn._fnc("CAnalyzer.MAXSIZE()")

    def canalyzer_pin(self, pin_name: int) -> int:
        return self.__conn._fnc("CAnalyzer.PIN(" + str(pin_name) + ")")

    def canalyzer_record_address(self, record_number: int) -> object:
        return self.__conn._fnc(
            "CAnalyzer.RECORD.ADDRESS(" + str(record_number) + ")"
        )

    def canalyzer_record_data(self, record_number: int) -> int:
        return self.__conn._fnc("CAnalyzer.RECORD.DATA(" + str(record_number) + ")")

    def canalyzer_record_offset(self, record_number: int) -> int:
        return self.__conn._fnc("CAnalyzer.RECORD.OFFSET(" + str(record_number) + ")")

    def canalyzer_record_time(self, record_number: int) -> object:
        return self.__conn._fnc("CAnalyzer.RECORD.TIME(" + str(record_number) + ")")

    def canalyzer_records(self) -> int:
        return self.__conn._fnc("CAnalyzer.RECORDS()")

    def canalyzer_ref(self) -> int:
        return self.__conn._fnc("CAnalyzer.REF()")

    def canalyzer_size(self) -> int:
        return self.__conn._fnc("CAnalyzer.SIZE()")

    def canalyzer_state(self) -> int:
        return self.__conn._fnc("CAnalyzer.STATE()")

    def canalyzer_track_record(self) -> int:
        return self.__conn._fnc("CAnalyzer.TRACK.RECORD()")

    def canalyzer_traceclock(self) -> int:
        return self.__conn._fnc("CAnalyzer.TraceCLOCK()")

    def canalyzer_traceconnect(self) -> str:
        return self.__conn._fnc("CAnalyzer.TraceCONNECT()")

    def canalyzer_traceport(self) -> str:
        return self.__conn._fnc("CAnalyzer.TracePort()")

    def ciprobe_adc_enable(self, channel: int) -> bool:
        return self.__conn._fnc("CIProbe.ADC.ENABLE(" + str(channel) + ")")

    def ciprobe_adc_shunt(self, channel: int) -> float:
        return self.__conn._fnc("CIProbe.ADC.SHUNT(" + str(channel) + ")")

    def ciprobe_maxsize(self) -> int:
        return self.__conn._fnc("CIProbe.MAXSIZE()")

    def ciprobe_records(self) -> int:
        return self.__conn._fnc("CIProbe.RECORDS()")

    def ciprobe_size(self) -> int:
        return self.__conn._fnc("CIProbe.SIZE()")

    def ciprobe_state(self) -> int:
        return self.__conn._fnc("CIProbe.STATE()")

    def ciprobe_track_record(self) -> int:
        return self.__conn._fnc("CIProbe.TRACK.RECORD()")

    def intercom_podport(self, index: int) -> int:
        return self.__conn._fnc("InterCom.PODPORT(" + str(index) + ")")

    def intercom_podportname(self, index: int) -> str:
        return self.__conn._fnc("InterCom.PODPORTNAME(" + str(index) + ")")

    def intercom_podportnumber(self) -> int:
        return self.__conn._fnc("InterCom.PODPORTNUMBER()")

    def intercom_ping(self, intercom_name: int) -> bool:
        return self.__conn._fnc("InterCom.PING(" + str(intercom_name) + ")")

    def intercom_port(self) -> int:
        return self.__conn._fnc("InterCom.PORT()")

    def intercom_name(self) -> str:
        return self.__conn._fnc("InterCom.NAME()")

    def gdb_port(self) -> int:
        return self.__conn._fnc("GDB.PORT()")

    def rcl_port(self, index: int) -> int:
        return self.__conn._fnc("RCL.PORT(" + str(index) + ")")

    def tcf_port(self) -> int:
        return self.__conn._fnc("TCF.PORT()")

    def tcf_discovery(self) -> bool:
        return self.__conn._fnc("TCF.DISCOVERY()")

    def integrator_adc_enable(self, channel: int) -> bool:
        return self.__conn._fnc("Integrator.ADC.ENABLE(" + str(channel) + ")")

    def integrator_adc_shunt(self, channel: int) -> float:
        return self.__conn._fnc("Integrator.ADC.SHUNT(" + str(channel) + ")")

    def integrator_analog(self) -> int:
        return self.__conn._fnc("Integrator.ANALOG()")

    def integrator_counter_event(self, counter_name: int) -> int:
        return self.__conn._fnc("Integrator.COUNTER.EVENT(" + str(counter_name) + ")")

    def integrator_counter_extern(self, counter_name: int) -> int:
        return self.__conn._fnc(
            "Integrator.COUNTER.EXTERN(" + str(counter_name) + ")"
        )

    def integrator_counter_time(self, counter_name: int) -> object:
        return self.__conn._fnc("Integrator.COUNTER.TIME(" + str(counter_name) + ")")

    def integrator_dsel(self) -> str:
        return self.__conn._fnc("Integrator.DSEL()")

    def integrator_find_pi_channel(self, signal_name: int) -> int:
        return self.__conn._fnc(
            "Integrator.FIND.PI_CHANNEL(" + str(signal_name) + ")"
        )

    def integrator_find_pi_word(self, signal_word: int) -> bool:
        return self.__conn._fnc("Integrator.FIND.PI_WORD(" + str(signal_word) + ")")

    def integrator_first(self) -> int:
        return self.__conn._fnc("Integrator.FIRST()")

    def integrator_flag(self, flag_name: int) -> bool:
        return self.__conn._fnc("Integrator.FLAG(" + str(flag_name) + ")")

    def integrator_get(self, channel_name: int) -> int:
        return self.__conn._fnc("Integrator.GET(" + str(channel_name) + ")")

    def integrator_maxsize(self) -> int:
        return self.__conn._fnc("Integrator.MAXSIZE()")

    def integrator_probe(self) -> int:
        return self.__conn._fnc("Integrator.PROBE()")

    def integrator_programfilename(self) -> str:
        return self.__conn._fnc("Integrator.PROGRAMFILENAME()")

    def integrator_record_data(self, channel: int, record_number: int) -> int:
        return self.__conn._fnc(
            "Integrator.RECORD.DATA(" + str(channel) + ", " + str(record_number) + ")"
        )

    def integrator_record_time(self, record_number: int) -> object:
        return self.__conn._fnc("Integrator.RECORD.TIME(" + str(record_number) + ")")

    def integrator_records(self) -> int:
        return self.__conn._fnc("Integrator.RECORDS()")

    def integrator_ref(self) -> int:
        return self.__conn._fnc("Integrator.REF()")

    def integrator_size(self) -> int:
        return self.__conn._fnc("Integrator.SIZE()")

    def integrator_state(self) -> int:
        return self.__conn._fnc("Integrator.STATE()")

    def integrator_track_record(self) -> int:
        return self.__conn._fnc("Integrator.TRACK.RECORD()")

    def integrator_usb(self) -> int:
        return self.__conn._fnc("Integrator.USB()")

    def integrator_dialogdsel(self, string: int) -> int:
        return self.__conn._fnc("Integrator.DIALOGDSEL(" + str(string) + ")")

    def integrator_dialogdselget(self) -> str:
        return self.__conn._fnc("Integrator.DIALOGDSELGET()")

    def i2c_pin(self, pin_name: int) -> int:
        return self.__conn._fnc("I2C.PIN(" + str(pin_name) + ")")

    def i2c_data(self, index: int) -> int:
        return self.__conn._fnc("I2C.DATA(" + str(index) + ")")

    def pattern(self) -> bool:
        return self.__conn._fnc("PATTERN()")

    def snooper_first(self) -> int:
        return self.__conn._fnc("SNOOPer.FIRST()")

    def snooper_maxsize(self) -> int:
        return self.__conn._fnc("SNOOPer.MAXSIZE()")

    def snooper_record_address(self, record_number: int) -> object:
        return self.__conn._fnc("SNOOPer.RECORD.ADDRESS(" + str(record_number) + ")")

    def snooper_record_data(self, record_number: int) -> int:
        return self.__conn._fnc("SNOOPer.RECORD.DATA(" + str(record_number) + ")")

    def snooper_record_offset(self, record_number: int) -> int:
        return self.__conn._fnc("SNOOPer.RECORD.OFFSET(" + str(record_number) + ")")

    def snooper_record_time(self, record_number: int) -> object:
        return self.__conn._fnc("SNOOPer.RECORD.TIME(" + str(record_number) + ")")

    def snooper_records(self) -> int:
        return self.__conn._fnc("SNOOPer.RECORDS()")

    def snooper_ref(self) -> int:
        return self.__conn._fnc("SNOOPer.REF()")

    def snooper_size(self) -> int:
        return self.__conn._fnc("SNOOPer.SIZE()")

    def snooper_state(self) -> int:
        return self.__conn._fnc("SNOOPer.STATE()")

    def onchip_first(self) -> int:
        return self.__conn._fnc("Onchip.FIRST()")

    def onchip_flow_errors(self) -> int:
        return self.__conn._fnc("Onchip.FLOW.ERRORS()")

    def onchip_flow_fifofull(self) -> int:
        return self.__conn._fnc("Onchip.FLOW.FIFOFULL()")

    def onchip_maxsize(self) -> int:
        return self.__conn._fnc("Onchip.MAXSIZE()")

    def onchip_record_address(self, record_number: int) -> object:
        return self.__conn._fnc("Onchip.RECORD.ADDRESS(" + str(record_number) + ")")

    def onchip_record_data(self, record_number: int) -> int:
        return self.__conn._fnc("Onchip.RECORD.DATA(" + str(record_number) + ")")

    def onchip_record_offset(self, record_number: int) -> int:
        return self.__conn._fnc("Onchip.RECORD.OFFSET(" + str(record_number) + ")")

    def onchip_record_time(self, record_number: int) -> object:
        return self.__conn._fnc("Onchip.RECORD.TIME(" + str(record_number) + ")")

    def onchip_records(self) -> int:
        return self.__conn._fnc("Onchip.RECORDS()")

    def onchip_ref(self) -> int:
        return self.__conn._fnc("Onchip.REF()")

    def onchip_size(self) -> int:
        return self.__conn._fnc("Onchip.SIZE()")

    def onchip_state(self) -> int:
        return self.__conn._fnc("Onchip.STATE()")

    def onchip_traceconnect(self) -> str:
        return self.__conn._fnc("Onchip.TraceCONNECT()")

    def onchip_track_record(self) -> int:
        return self.__conn._fnc("Onchip.TRACK.RECORD()")

    def os_presentdemodirectory(self) -> str:
        return self.__conn._fnc("OS.PresentDemoDirectory()")

    def os_dir_access(self, access_right: int, directory_name: int) -> bool:
        return self.__conn._fnc(
            "OS.DIR.ACCESS(" + str(access_right) + ", " + str(directory_name) + ")"
        )

    def os_env(self, env_var: int) -> str:
        return self.__conn._fnc("OS.ENV(" + str(env_var) + ")")

    def os_file_abspath(self, file: int) -> str:
        return self.__conn._fnc("OS.FILE.ABSPATH(" + str(file) + ")")

    def os_file_access(self, access_type: int, file: int) -> bool:
        return self.__conn._fnc(
            "OS.FILE.ACCESS(" + str(access_type) + ", " + str(file) + ")"
        )

    def os_file_date(self, file: int) -> str:
        return self.__conn._fnc("OS.FILE.DATE(" + str(file) + ")")

    def os_file_date2(self, file: int) -> str:
        return self.__conn._fnc("OS.FILE.DATE2(" + str(file) + ")")

    def os_file_extension(self, file: int) -> str:
        return self.__conn._fnc("OS.FILE.EXTENSION(" + str(file) + ")")

    def os_file_link(self, file: int) -> str:
        return self.__conn._fnc("OS.FILE.LINK(" + str(file) + ")")

    def os_file_name(self, path: int) -> str:
        return self.__conn._fnc("OS.FILE.NAME(" + str(path) + ")")

    def os_file_path(self, file: int) -> str:
        return self.__conn._fnc("OS.FILE.PATH(" + str(file) + ")")

    def os_file_realpath(self, file: int) -> str:
        return self.__conn._fnc("OS.FILE.REALPATH(" + str(file) + ")")

    def os_file_size(self, file: int) -> int:
        return self.__conn._fnc("OS.FILE.SIZE(" + str(file) + ")")

    def os_file_time(self, file: int) -> str:
        return self.__conn._fnc("OS.FILE.TIME(" + str(file) + ")")

    def os_file_unixtime(self, file: int) -> int:
        return self.__conn._fnc("OS.FILE.UnixTime(" + str(file) + ")")

    def os_firstfile(self, pattern: int) -> str:
        return self.__conn._fnc("OS.FIRSTFILE(" + str(pattern) + ")")

    def os_id(self) -> str:
        return self.__conn._fnc("OS.ID()")

    def os_name(self) -> str:
        return self.__conn._fnc("OS.NAME()")

    def os_nextfile(self) -> str:
        return self.__conn._fnc("OS.NEXTFILE()")

    def os_presentconfigurationfile(self) -> str:
        return self.__conn._fnc("OS.PresentConfigurationFile()")

    def os_presentexecutabledirectory(self) -> str:
        return self.__conn._fnc("OS.PresentExecutableDirectory()")

    def os_presentexecutablefile(self) -> str:
        return self.__conn._fnc("OS.PresentExecutableFile()")

    def os_presenthomedirectory(self) -> str:
        return self.__conn._fnc("OS.PresentHomeDirectory()")

    def os_presenthelpdirectory(self) -> str:
        return self.__conn._fnc("OS.PresentHELPDirectory()")

    def os_presentlicensefile(self) -> str:
        return self.__conn._fnc("OS.PresentLicenseFile()")

    def os_presentpracticedirectory(self) -> str:
        return self.__conn._fnc("OS.PresentPracticeDirectory()")

    def os_presentpracticefile(self) -> str:
        return self.__conn._fnc("OS.PresentPracticeFile()")

    def os_presentsystemdirectory(self) -> str:
        return self.__conn._fnc("OS.PresentSystemDirectory()")

    def os_presenttemporarydirectory(self) -> str:
        return self.__conn._fnc("OS.PresentTemporaryDirectory()")

    def os_presentworkingdirectory(self) -> str:
        return self.__conn._fnc("OS.PresentWorkingDirectory()")

    def os_return(self) -> int:
        return self.__conn._fnc("OS.RETURN()")

    def os_timer(self) -> int:
        return self.__conn._fnc("OS.TIMER()")

    def os_tmpfile(self) -> str:
        return self.__conn._fnc("OS.TMPFILE()")

    def os_version(self, version_data_type: int) -> int:
        return self.__conn._fnc("OS.VERSION(" + str(version_data_type) + ")")

    def os_portavailable_udp(self, port_number: int) -> bool:
        return self.__conn._fnc("OS.PORTAVAILABLE.UDP(" + str(port_number) + ")")

    def os_portavailable_tcp(self, port_number: int) -> bool:
        return self.__conn._fnc("OS.PORTAVAILABLE.TCP(" + str(port_number) + ")")

    def logger_first(self) -> int:
        return self.__conn._fnc("LOGGER.FIRST()")

    def logger_record_address(self, record_number: int) -> object:
        return self.__conn._fnc("LOGGER.RECORD.ADDRESS(" + str(record_number) + ")")

    def logger_record_data(self, record_number: int) -> int:
        return self.__conn._fnc("LOGGER.RECORD.DATA(" + str(record_number) + ")")

    def logger_record_offset(self, record_number: int) -> int:
        return self.__conn._fnc("LOGGER.RECORD.OFFSET(" + str(record_number) + ")")

    def logger_record_time(self, record_number: int) -> object:
        return self.__conn._fnc("LOGGER.RECORD.TIME(" + str(record_number) + ")")

    def logger_records(self) -> int:
        return self.__conn._fnc("LOGGER.RECORDS()")

    def logger_ref(self) -> int:
        return self.__conn._fnc("LOGGER.REF()")

    def logger_size(self) -> int:
        return self.__conn._fnc("LOGGER.SIZE()")

    def logger_state(self) -> int:
        return self.__conn._fnc("LOGGER.STATE()")

    def la_ref(self) -> int:
        return self.__conn._fnc("LA.REF()")

    def la_records(self) -> int:
        return self.__conn._fnc("LA.RECORDS()")

    def la_state(self) -> int:
        return self.__conn._fnc("LA.STATE()")

    def la_size(self) -> int:
        return self.__conn._fnc("LA.SIZE()")

    def la_maxsize(self) -> int:
        return self.__conn._fnc("LA.MAXSIZE()")

    def fdx_records(self) -> int:
        return self.__conn._fnc("FDX.RECORDS()")

    def fdx_ref(self) -> int:
        return self.__conn._fnc("FDX.REF()")

    def fdx_state(self) -> int:
        return self.__conn._fnc("FDX.STATE()")

    def fdx_instring(self, address: int) -> str:
        return self.__conn._fnc("FDX.INSTRING(" + str(address) + ")")

    def atrace_records(self) -> int:
        return self.__conn._fnc("ATrace.RECORDS()")

    def atrace_ref(self) -> int:
        return self.__conn._fnc("ATrace.REF()")

    def atrace_state(self) -> int:
        return self.__conn._fnc("ATrace.STATE()")

    def atrace_size(self) -> int:
        return self.__conn._fnc("ATrace.SIZE()")

    def btrace_records(self) -> int:
        return self.__conn._fnc("BTrace.RECORDS()")

    def btrace_ref(self) -> int:
        return self.__conn._fnc("BTrace.REF()")

    def btrace_state(self) -> int:
        return self.__conn._fnc("BTrace.STATE()")

    def btrace_size(self) -> int:
        return self.__conn._fnc("BTrace.SIZE()")

    def trace_first(self) -> int:
        return self.__conn._fnc("Trace.FIRST()")

    def trace_flow_errors(self) -> int:
        return self.__conn._fnc("Trace.FLOW.ERRORS()")

    def trace_flow_fifofull(self) -> int:
        return self.__conn._fnc("Trace.FLOW.FIFOFULL()")

    def trace_method_analyzer(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.Analyzer()")

    def trace_method_art(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.ART()")

    def trace_method_atrace(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.ATrace()")

    def trace_method_canalyzer(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.CAnalyzer()")

    def trace_method_fdx(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.FDX()")

    def trace_method_hanalyzer(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.HAnalyzer()")

    def trace_method_integrator(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.Integrator()")

    def trace_method_iprobe(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.IProbe()")

    def trace_method_la(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.LA()")

    def trace_method_logger(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.LOGGER()")

    def trace_method_onchip(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.ONCHIP()")

    def trace_method_probe(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.Probe()")

    def trace_method_snooper(self) -> bool:
        return self.__conn._fnc("Trace.METHOD.SNOOPer()")

    def trace_records(self) -> int:
        return self.__conn._fnc("Trace.RECORDS()")

    def trace_size(self) -> int:
        return self.__conn._fnc("Trace.SIZE()")

    def trace_maxsize(self) -> int:
        return self.__conn._fnc("Trace.MAXSIZE()")

    def trace_record_address(self, record_number: int) -> object:
        return self.__conn._fnc("Trace.RECORD.ADDRESS(" + str(record_number) + ")")

    def trace_record_data(self, record_number: int) -> int:
        return self.__conn._fnc("Trace.RECORD.DATA(" + str(record_number) + ")")

    def trace_record_offset(self, record_number: int) -> int:
        return self.__conn._fnc("Trace.RECORD.OFFSET(" + str(record_number) + ")")

    def trace_record_time(self, record_number: int) -> object:
        return self.__conn._fnc("Trace.RECORD.TIME(" + str(record_number) + ")")

    def trace_state(self) -> int:
        return self.__conn._fnc("Trace.STATE()")

    def trace_stream_overflows(self) -> bool:
        return self.__conn._fnc("Trace.STREAM.OVERFLOWS()")

    def trace_traceconnect(self) -> str:
        return self.__conn._fnc("Trace.TraceCONNECT()")

    def trace_load(self) -> str:
        return self.__conn._fnc("Trace.LOAD()")

    def trace_file(self) -> str:
        return self.__conn._fnc("Trace.FILE()")

    def tronchip_counter(self, pnumber: int) -> int:
        return self.__conn._fnc("TrOnchip.COUNTER(" + str(pnumber) + ")")

    def tronchip_isavailable(self, trigger_name: int) -> bool:
        return self.__conn._fnc("TrOnchip.IsAvailable(" + str(trigger_name) + ")")

    def tronchip_isset(self, trigger_name: int) -> bool:
        return self.__conn._fnc("TrOnchip.IsSet(" + str(trigger_name) + ")")

    def bmc_counter_byname_core(self, core_index: int, counter_name: int) -> int:
        return self.__conn._fnc(
            "BMC.COUNTER.BYNAME.CORE("
            + str(core_index)
            + ", "
            + str(counter_name)
            + ")"
        )

    def bmc_counter_core(self, core_index: int, counter_index: int) -> int:
        return self.__conn._fnc(
            "BMC.COUNTER.CORE(" + str(core_index) + ", " + str(counter_index) + ")"
        )

    def bmc_overflow_byname_core(self, core_index: int, counter_name: int) -> bool:
        return self.__conn._fnc(
            "BMC.OVERFLOW.BYNAME.CORE("
            + str(core_index)
            + ", "
            + str(counter_name)
            + ")"
        )

    def bmc_overflow_core(self, core_index: int, counter_index: int) -> bool:
        return self.__conn._fnc(
            "BMC.OVERFLOW.CORE(" + str(core_index) + ", " + str(counter_index) + ")"
        )

    def bmc_clock(self) -> int:
        return self.__conn._fnc("BMC.CLOCK()")

    def mcds_module_name(self) -> str:
        return self.__conn._fnc("MCDS.Module.NAME()")

    def mcds_module_number(self) -> int:
        return self.__conn._fnc("MCDS.Module.NUMBER()")

    def mcds_module_revision(self) -> int:
        return self.__conn._fnc("MCDS.Module.REVision()")

    def mcds_module_type(self) -> int:
        return self.__conn._fnc("MCDS.Module.TYPE()")

    def mcds_state(self) -> int:
        return self.__conn._fnc("MCDS.STATE()")

    def mcds_tracebuffer_lowergap(self) -> int:
        return self.__conn._fnc("MCDS.TraceBuffer.LowerGAP()")

    def mcds_tracebuffer_size(self) -> int:
        return self.__conn._fnc("MCDS.TraceBuffer.SIZE()")

    def mcds_tracebuffer_uppergap(self) -> int:
        return self.__conn._fnc("MCDS.TraceBuffer.UpperGAP()")

    def trigger_offset(self) -> int:
        return self.__conn._fnc("TRIGGER.OFFSET()")

    def trigger_access(self) -> int:
        return self.__conn._fnc("TRIGGER.ACCESS()")

    def trigger_address(self) -> object:
        return self.__conn._fnc("TRIGGER.ADDRESS()")

    def trigger_bytes(self) -> int:
        return self.__conn._fnc("TRIGGER.BYTES()")

    def trigger_count_alpha(self) -> int:
        return self.__conn._fnc("TRIGGER.COUNT.ALPHA()")

    def trigger_count_beta(self) -> int:
        return self.__conn._fnc("TRIGGER.COUNT.BETA()")

    def trigger_count_charly(self) -> int:
        return self.__conn._fnc("TRIGGER.COUNT.CHARLY()")

    def trigger_cycle(self) -> int:
        return self.__conn._fnc("TRIGGER.CYCLE()")

    def trigger_delay_cycle(self) -> int:
        return self.__conn._fnc("TRIGGER.DELAY.CYCLE()")

    def trigger_delay_time(self) -> object:
        return self.__conn._fnc("TRIGGER.DELAY.TIME()")

    def trigger_delay_trace(self) -> int:
        return self.__conn._fnc("TRIGGER.DELAY.TRACE()")

    def trigger_source(self) -> int:
        return self.__conn._fnc("TRIGGER.SOURCE()")

    def trigger_state(self) -> int:
        return self.__conn._fnc("TRIGGER.STATE()")

    def map_ramsize(self) -> int:
        return self.__conn._fnc("MAP.RAMSIZE()")

    def map_romsize(self) -> int:
        return self.__conn._fnc("MAP.ROMSIZE()")

    def map_config_fdpram(self) -> bool:
        return self.__conn._fnc("MAP.CONFIG.FDPRAM()")

    def perf_memory_hits(self, core: int, value: int) -> int:
        return self.__conn._fnc(
            "PERF.MEMORY.HITS(" + str(core) + ", " + str(value) + ")"
        )

    def perf_memory_snoopaddress(self) -> object:
        return self.__conn._fnc("PERF.MEMORY.SnoopAddress()")

    def perf_memory_snoopsize(self) -> int:
        return self.__conn._fnc("PERF.MEMORY.SnoopSize()")

    def perf_method(self) -> int:
        return self.__conn._fnc("PERF.METHOD()")

    def perf_mode(self) -> int:
        return self.__conn._fnc("PERF.Mode()")

    def perf_pc_hits(self, core: int, address_range: int) -> int:
        return self.__conn._fnc(
            "PERF.PC.HITS(" + str(core) + ", " + str(address_range) + ")"
        )

    def perf_rate(self) -> int:
        return self.__conn._fnc("PERF.RATE()")

    def perf_runtime(self) -> str:
        return self.__conn._fnc("PERF.RunTime()")

    def perf_snoopfails(self) -> int:
        return self.__conn._fnc("PERF.SNOOPFAILS()")

    def perf_state(self) -> int:
        return self.__conn._fnc("PERF.STATE()")

    def perf_task_hits(self, core: int, task_magic: int) -> int:
        return self.__conn._fnc(
            "PERF.TASK.HITS(" + str(core) + ", " + str(task_magic) + ")"
        )

    def perf_watchtime(self, index: int) -> object:
        return self.__conn._fnc("PERF.WATCHTIME(" + str(index) + ")")

    def trin_value(self) -> int:
        return self.__conn._fnc("TRIN.VALUE()")

    def break_program_exist(self, address: int) -> bool:
        return self.__conn._fnc("Break.Program.EXIST(" + str(address) + ")")

    def break_readwrite_exist(self, address: int) -> bool:
        return self.__conn._fnc("Break.ReadWrite.EXIST(" + str(address) + ")")

    def break_alpha_exist(self, address: int) -> bool:
        return self.__conn._fnc("Break.Alpha.EXIST(" + str(address) + ")")

    def break_beta_exist(self, address: int) -> bool:
        return self.__conn._fnc("Break.Beta.EXIST(" + str(address) + ")")

    def break_charly_exist(self, address: int) -> bool:
        return self.__conn._fnc("Break.Charly.EXIST(" + str(address) + ")")

    def term_line(self, line_number: int, address: int) -> str:
        return self.__conn._fnc(
            "TERM.LINE(" + str(line_number) + ", " + str(address) + ")"
        )

    def term_returncode(self, address: int) -> int:
        return self.__conn._fnc("TERM.RETURNCODE(" + str(address) + ")")

    def term_triggered(self, address_out: int) -> bool:
        return self.__conn._fnc("TERM.TRIGGERED(" + str(address_out) + ")")

    def runtime_accuracy(self) -> object:
        return self.__conn._fnc("RunTime.ACCURACY()")

    def runtime_actual(self) -> object:
        return self.__conn._fnc("RunTime.ACTUAL()")

    def runtime_last(self) -> object:
        return self.__conn._fnc("RunTime.LAST()")

    def runtime_lastrun(self) -> object:
        return self.__conn._fnc("RunTime.LASTRUN()")

    def runtime_refa(self) -> object:
        return self.__conn._fnc("RunTime.REFA()")

    def runtime_refb(self) -> object:
        return self.__conn._fnc("RunTime.REFB()")

    def component_available(self, component_name: int) -> bool:
        return self.__conn._fnc("COMPonent.AVAILABLE(" + str(component_name) + ")")

    def component_base(self, core: int, component_name: int) -> object:
        return self.__conn._fnc(
            "COMPonent.BASE(" + str(core) + ", " + str(component_name) + ")"
        )

    def component_name(self, core: int, component_name: int) -> str:
        return self.__conn._fnc(
            "COMPonent.NAME(" + str(core) + ", " + str(component_name) + ")"
        )

    def component_type(self, strComponentName: int) -> str:
        return self.__conn._fnc("COMPonent.TYPE(" + str(strComponentName) + ")")

    def etm_version(self) -> int:
        return self.__conn._fnc("ETM.VERSION()")

    def etm_addrcomptotal(self) -> int:
        return self.__conn._fnc("ETM.ADDRCOMPTOTAL()")

    def etm_addrcomp(self) -> int:
        return self.__conn._fnc("ETM.ADDRCOMP()")

    def etm_datacomp(self) -> int:
        return self.__conn._fnc("ETM.DATACOMP()")

    def etm_contextcomp(self) -> int:
        return self.__conn._fnc("ETM.CONTEXTCOMP()")

    def etm_counters(self) -> int:
        return self.__conn._fnc("ETM.COUNTERS()")

    def etm_extin(self) -> int:
        return self.__conn._fnc("ETM.EXTIN()")

    def etm_extout(self) -> int:
        return self.__conn._fnc("ETM.EXTOUT()")

    def etm_fifofull(self) -> int:
        return self.__conn._fnc("ETM.FIFOFULL()")

    def etm_map(self) -> int:
        return self.__conn._fnc("ETM.MAP()")

    def etm_protocol(self) -> int:
        return self.__conn._fnc("ETM.PROTOCOL()")

    def etm_sequencer(self) -> int:
        return self.__conn._fnc("ETM.SEQUENCER()")

    def etmbase(self) -> object:
        return self.__conn._fnc("ETMBASE()")

    def aet(self) -> bool:
        return self.__conn._fnc("AET()")

    def tpiu_portmode(self) -> str:
        return self.__conn._fnc("TPIU.PortMode()")

    def tpiu_portsize(self) -> str:
        return self.__conn._fnc("TPIU.PortSize()")

    def tpiu_swvprescaler(self) -> int:
        return self.__conn._fnc("TPIU.SWVPrescaler()")

    def etbavailable(self) -> bool:
        return self.__conn._fnc("ETBAVAILABLE()")

    def etbbase(self) -> object:
        return self.__conn._fnc("ETBBASE()")

    def etbscorpion(self) -> bool:
        return self.__conn._fnc("ETBSCORPION()")

    def etbcoresight(self) -> bool:
        return self.__conn._fnc("ETBCORESIGHT()")

    def tpiuavailable(self) -> bool:
        return self.__conn._fnc("TPIUAVAILABLE()")

    def tpiubase(self) -> object:
        return self.__conn._fnc("TPIUBASE()")

    def funnelavailable(self) -> bool:
        return self.__conn._fnc("FUNNELAVAILABLE()")

    def funnelbase(self) -> object:
        return self.__conn._fnc("FUNNELBASE()")

    def funnel2available(self) -> bool:
        return self.__conn._fnc("FUNNEL2AVAILABLE()")

    def funnel2base(self) -> object:
        return self.__conn._fnc("FUNNEL2BASE()")

    def tpiufunnelavailable(self) -> bool:
        return self.__conn._fnc("TPIUFUNNELAVAILABLE()")

    def tpiufunnelbase(self) -> object:
        return self.__conn._fnc("TPIUFUNNELBASE()")

    def etbfunnelavailable(self) -> bool:
        return self.__conn._fnc("ETBFUNNELAVAILABLE()")

    def etbfunnelbase(self) -> object:
        return self.__conn._fnc("ETBFUNNELBASE()")

    def etb(self) -> bool:
        return self.__conn._fnc("ETB()")

    def htm(self) -> bool:
        return self.__conn._fnc("HTM()")

    def htmbase(self) -> object:
        return self.__conn._fnc("HTMBASE()")

    def itm(self) -> bool:
        return self.__conn._fnc("ITM()")

    def itmbase(self, thread: int) -> object:
        return self.__conn._fnc("ITMBASE(" + str(thread) + ")")

    def dwtbase(self) -> object:
        return self.__conn._fnc("DWTBASE()")

    def corebase(self) -> object:
        return self.__conn._fnc("COREBASE()")

    def ctibase(self) -> object:
        return self.__conn._fnc("CTIBASE()")

    def rtpbase(self) -> object:
        return self.__conn._fnc("RTPBASE()")

    def ocpbase(self) -> object:
        return self.__conn._fnc("OCPBASE()")

    def ocptype(self) -> int:
        return self.__conn._fnc("OCPTYPE()")

    def sdtibase(self) -> object:
        return self.__conn._fnc("SDTIBASE()")

    def stmbase(self) -> object:
        return self.__conn._fnc("STMBASE()")

    def pmibase(self) -> object:
        return self.__conn._fnc("PMIBASE()")

    def cmibase(self, instance: int) -> object:
        return self.__conn._fnc("CMIBASE(" + str(instance) + ")")

    def ela_version(self) -> int:
        return self.__conn._fnc("ELA.VERSION()")

    def elabase(self) -> object:
        return self.__conn._fnc("ELABASE()")

    def etk(self) -> bool:
        return self.__conn._fnc("ETK()")

    def portsharing(self) -> int:
        return self.__conn._fnc("PORTSHARING()")

    def chip_astep(self) -> bool:
        return self.__conn._fnc("CHIP.AStep()")

    def chip_stepping(self) -> str:
        return self.__conn._fnc("CHIP.STEPping()")

    def chip_emulationdevice(self) -> bool:
        return self.__conn._fnc("CHIP.EmulationDevice()")

    def chip_gtmversion(self) -> int:
        return self.__conn._fnc("CHIP.GTMVersion()")

    def chip_gtm_mcsmodule(self) -> int:
        return self.__conn._fnc("CHIP.GTM.MCSModule()")

    def chip_gtm_atommodule(self) -> int:
        return self.__conn._fnc("CHIP.GTM.ATOMModule()")

    def chip_gtm_tommodule(self) -> int:
        return self.__conn._fnc("CHIP.GTM.TOMModule()")

    def chip_gtm_timmodule(self) -> int:
        return self.__conn._fnc("CHIP.GTM.TIMModule()")

    def cerberus_ioinfo_iflck(self) -> bool:
        return self.__conn._fnc("CERBERUS.IOINFO.IFLCK()")

    def dap_available(self) -> bool:
        return self.__conn._fnc("DAP.Available()")

    def dap_user0(self) -> bool:
        return self.__conn._fnc("DAP.USER0()")

    def dap_user1(self) -> bool:
        return self.__conn._fnc("DAP.USER1()")

    def nexus_portmode(self) -> str:
        return self.__conn._fnc("NEXUS.PortMode()")

    def nexus_portsize(self) -> str:
        return self.__conn._fnc("NEXUS.PortSize()")

    def nexus_rttbuild(self, register_index: int) -> int:
        return self.__conn._fnc("NEXUS.RTTBUILD(" + str(register_index) + ")")

    def traceport_lanecount(self, index: int) -> int:
        return self.__conn._fnc("TRACEPORT.LaneCount(" + str(index) + ")")

    def ipt_rtit(self) -> bool:
        return self.__conn._fnc("IPT.RTIT()")

    def id_cable(self) -> int:
        return self.__conn._fnc("ID.CABLE()")

    def id_preprocessor(self) -> int:
        return self.__conn._fnc("ID.PREPROcessor()")

    def id_whisker(self, int: int) -> int:
        return self.__conn._fnc("ID.WHISKER(" + str(int) + ")")

    def cable_name(self) -> str:
        return self.__conn._fnc("CABLE.NAME()")

    def cable_serial(self) -> str:
        return self.__conn._fnc("CABLE.SERIAL()")

    def cable_galvanicisolation_serial(self) -> str:
        return self.__conn._fnc("CABLE.GalvanicISOlation.SERIAL()")

    def cable_twowire(self) -> bool:
        return self.__conn._fnc("CABLE.TWOWIRE()")

    def license_havefeature(self, name: int) -> bool:
        return self.__conn._fnc("LICENSE.HAVEFEATURE(" + str(name) + ")")

    def license_features(self, index: int) -> str:
        return self.__conn._fnc("LICENSE.FEATURES(" + str(index) + ")")

    def license_family(self, index: int) -> str:
        return self.__conn._fnc("LICENSE.FAMILY(" + str(index) + ")")

    def license_multicore(self) -> bool:
        return self.__conn._fnc("LICENSE.MULTICORE()")

    def license_date(self, index: int) -> str:
        return self.__conn._fnc("LICENSE.DATE(" + str(index) + ")")

    def license_getindex(self) -> int:
        return self.__conn._fnc("LICENSE.getINDEX()")

    def license_granted(self, version: int, product: int) -> int:
        return self.__conn._fnc(
            "LICENSE.GRANTED(" + str(version) + ", " + str(product) + ")"
        )

    def license_mserial(self, index: int) -> str:
        return self.__conn._fnc("LICENSE.MSERIAL(" + str(index) + ")")

    def license_serial(self, index: int) -> str:
        return self.__conn._fnc("LICENSE.SERIAL(" + str(index) + ")")

    def version_cable(self) -> int:
        return self.__conn._fnc("VERSION.CABLE()")

    def version_firmware_debug(self) -> float:
        return self.__conn._fnc("VERSION.FirmWare.DEBUG()")

    def version_serial_cable(self) -> str:
        return self.__conn._fnc("VERSION.SERIAL.CABLE()")

    def version_serial_debug(self) -> str:
        return self.__conn._fnc("VERSION.SERIAL.DEBUG()")

    def version_serial_integrator(self) -> str:
        return self.__conn._fnc("VERSION.SERIAL.Integrator()")

    def version_serial_nexusadapter(self) -> str:
        return self.__conn._fnc("VERSION.SERIAL.NEXUSadapter()")

    def version_serial_powerprobe(self) -> str:
        return self.__conn._fnc("VERSION.SERIAL.POWERPROBE()")

    def version_serial_preprocessor(self) -> str:
        return self.__conn._fnc("VERSION.SERIAL.PREPROcessor()")

    def version_serial_trace(self) -> str:
        return self.__conn._fnc("VERSION.SERIAL.TRACE()")

    def version_build_base(self) -> int:
        return self.__conn._fnc("VERSION.BUILD.BASE()")

    def version_date(self) -> str:
        return self.__conn._fnc("VERSION.DATE()")

    def version_environment(self, name: int) -> str:
        return self.__conn._fnc("VERSION.ENVironment(" + str(name) + ")")

    def version_software(self) -> str:
        return self.__conn._fnc("VERSION.SOFTWARE()")

    def pod(self, podname: int) -> int:
        return self.__conn._fnc("POD(" + str(podname) + ")")

    def level(self) -> int:
        return self.__conn._fnc("LEVEL()")

    def con(self) -> bool:
        return self.__conn._fnc("CON()")

    def found_count(self) -> int:
        return self.__conn._fnc("FOUND.COUNT()")

    def timeout(self) -> bool:
        return self.__conn._fnc("TIMEOUT()")

    def warnings(self) -> bool:
        return self.__conn._fnc("WARNINGS()")

    def help_message(self) -> str:
        return self.__conn._fnc("HELP.MESSAGE()")

    def help_filter(self) -> str:
        return self.__conn._fnc("HELP.Filter()")

    def processid(self) -> int:
        return self.__conn._fnc("ProcessID()")

    def random_range(self, max: int, min: int) -> int:
        return self.__conn._fnc("RANDOM.RANGE(" + str(max) + ", " + str(min) + ")")

    def radix(self) -> int:
        return self.__conn._fnc("RADIX()")

    def date_date(self) -> str:
        return self.__conn._fnc("DATE.DATE()")

    def date_day(self) -> int:
        return self.__conn._fnc("DATE.DAY()")

    def date_makeunixtime(
        self, second: int, minute: int, hour: int, day: int, month: int, year: int
    ) -> int:
        return self.__conn._fnc(
            "DATE.MakeUnixTime("
            + str(second)
            + ", "
            + str(minute)
            + ", "
            + str(hour)
            + ", "
            + str(day)
            + ", "
            + str(month)
            + ", "
            + str(year)
            + ")"
        )

    def date_month(self) -> int:
        return self.__conn._fnc("DATE.MONTH()")

    def date_seconds(self) -> int:
        return self.__conn._fnc("DATE.SECONDS()")

    def date_time(self) -> str:
        return self.__conn._fnc("DATE.TIME()")

    def date_timezone(self) -> str:
        return self.__conn._fnc("DATE.TimeZone()")

    def date_unixtime(self) -> int:
        return self.__conn._fnc("DATE.UnixTime()")

    def date_utcoffset(self) -> int:
        return self.__conn._fnc("DATE.utcOffset()")

    def date_year(self) -> int:
        return self.__conn._fnc("DATE.YEAR()")

    def string_char(self, index: int, string: int) -> int:
        return self.__conn._fnc(
            "STRing.CHAR(" + str(index) + ", " + str(string) + ")"
        )

    def string_compare(self, pattern: int, string: int) -> bool:
        return self.__conn._fnc(
            "STRing.ComPare(" + str(pattern) + ", " + str(string) + ")"
        )

    def string_count(self, substring: int, string: int) -> int:
        return self.__conn._fnc(
            "STRing.COUNT(" + str(substring) + ", " + str(string) + ")"
        )

    def string_cut(self, length: int, string: int) -> str:
        return self.__conn._fnc(
            "STRing.CUT(" + str(length) + ", " + str(string) + ")"
        )

    def string_find(self, string2: int, string1: int) -> bool:
        return self.__conn._fnc(
            "STRing.FIND(" + str(string2) + ", " + str(string1) + ")"
        )

    def string_length(self, string: int) -> int:
        return self.__conn._fnc("STRing.LENgth(" + str(string) + ")")

    def string_lower(self, string: int) -> str:
        return self.__conn._fnc("STRing.LoWeR(" + str(string) + ")")

    def string_mid(self, length: int, start_at: int, string: int) -> str:
        return self.__conn._fnc(
            "STRing.MID("
            + str(length)
            + ", "
            + str(start_at)
            + ", "
            + str(string)
            + ")"
        )

    def string_replace(
        self,
        no_replaces: int,
        replace_string: int,
        search_string: int,
        source_string: int,
    ) -> str:
        return self.__conn._fnc(
            "STRing.Replace("
            + str(no_replaces)
            + ", "
            + str(replace_string)
            + ", "
            + str(search_string)
            + ", "
            + str(source_string)
            + ")"
        )

    def string_scan(self, start_at: int, search_string: int, source_string: int) -> int:
        return self.__conn._fnc(
            "STRing.SCAN("
            + str(start_at)
            + ", "
            + str(search_string)
            + ", "
            + str(source_string)
            + ")"
        )

    def string_scanandextract(self, default_value: int, key: int, string: int) -> str:
        return self.__conn._fnc(
            "STRing.SCANAndExtract("
            + str(default_value)
            + ", "
            + str(key)
            + ", "
            + str(string)
            + ")"
        )

    def string_scanback(
        self, start_at: int, search_string: int, source_string: int
    ) -> int:
        return self.__conn._fnc(
            "STRing.SCANBack("
            + str(start_at)
            + ", "
            + str(search_string)
            + ", "
            + str(source_string)
            + ")"
        )

    def string_split(self, index: int, separator: int, string: int) -> str:
        return self.__conn._fnc(
            "STRing.SPLIT("
            + str(index)
            + ", "
            + str(separator)
            + ", "
            + str(string)
            + ")"
        )

    def string_trim(self, string: int) -> str:
        return self.__conn._fnc("STRing.TRIM(" + str(string) + ")")

    def string_upper(self, string: int) -> str:
        return self.__conn._fnc("STRing.UPpeR(" + str(string) + ")")

    def string_escapequotes(self, source: int) -> str:
        return self.__conn._fnc("STRing.ESCapeQuotes(" + str(source) + ")")

    def math_abs(self, integer: int) -> int:
        return self.__conn._fnc("math.ABS(" + str(integer) + ")")

    def math_fabs(self, float: int) -> float:
        return self.__conn._fnc("math.FABS(" + str(float) + ")")

    def math_fcos(self, float: int) -> float:
        return self.__conn._fnc("math.FCOS(" + str(float) + ")")

    def math_fexp(self, float: int) -> float:
        return self.__conn._fnc("math.FEXP(" + str(float) + ")")

    def math_fexp10(self, float: int) -> float:
        return self.__conn._fnc("math.FEXP10(" + str(float) + ")")

    def math_finf(self) -> float:
        return self.__conn._fnc("math.FINF()")

    def math_flog(self, float: int) -> float:
        return self.__conn._fnc("math.FLOG(" + str(float) + ")")

    def math_flog10(self, float: int) -> float:
        return self.__conn._fnc("math.FLOG10(" + str(float) + ")")

    def math_fmax(self, float2: int, float1: int) -> float:
        return self.__conn._fnc("math.FMAX(" + str(float2) + ", " + str(float1) + ")")

    def math_fmin(self, float2: int, float1: int) -> float:
        return self.__conn._fnc("math.FMIN(" + str(float2) + ", " + str(float1) + ")")

    def math_fnan(self) -> float:
        return self.__conn._fnc("math.FNAN()")

    def math_fpow(self, float_y: int, float_x: int) -> float:
        return self.__conn._fnc(
            "math.FPOW(" + str(float_y) + ", " + str(float_x) + ")"
        )

    def math_fsin(self, value: int) -> float:
        return self.__conn._fnc("math.FSIN(" + str(value) + ")")

    def math_fsqrt(self, value: int) -> float:
        return self.__conn._fnc("math.FSQRT(" + str(value) + ")")

    def math_max(self, integer2: int, integer1: int) -> int:
        return self.__conn._fnc(
            "math.MAX(" + str(integer2) + ", " + str(integer1) + ")"
        )

    def math_min(self, integer2: int, integer1: int) -> int:
        return self.__conn._fnc(
            "math.MIN(" + str(integer2) + ", " + str(integer1) + ")"
        )

    def math_sign(self, integer: int) -> int:
        return self.__conn._fnc("math.SIGN(" + str(integer) + ")")

    def math_signum(self, integer: int) -> int:
        return self.__conn._fnc("math.SIGNUM(" + str(integer) + ")")

    def math_timemax(self, time2: int, time1: int) -> object:
        return self.__conn._fnc(
            "math.TimeMAX(" + str(time2) + ", " + str(time1) + ")"
        )

    def math_timemin(self, time2: int, time1: int) -> object:
        return self.__conn._fnc(
            "math.TimeMIN(" + str(time2) + ", " + str(time1) + ")"
        )

    def format_binary(self, number: int, width: int) -> str:
        return self.__conn._fnc(
            "FORMAT.BINary(" + str(number) + ", " + str(width) + ")"
        )

    def format_char(self, fill_character: int, width: int, value: int) -> str:
        return self.__conn._fnc(
            "FORMAT.CHAR("
            + str(fill_character)
            + ", "
            + str(width)
            + ", "
            + str(value)
            + ")"
        )

    def format_decimal(self, number: int, width: int) -> str:
        return self.__conn._fnc(
            "FORMAT.Decimal(" + str(number) + ", " + str(width) + ")"
        )

    def format_decimalu(self, number: int, width: int) -> str:
        return self.__conn._fnc(
            "FORMAT.DecimalU(" + str(number) + ", " + str(width) + ")"
        )

    def format_decimaluz(self, number: int, width: int) -> str:
        return self.__conn._fnc(
            "FORMAT.DecimalUZ(" + str(number) + ", " + str(width) + ")"
        )

    def format_float(self, number: int, precision: int, width: int) -> str:
        return self.__conn._fnc(
            "FORMAT.FLOAT("
            + str(number)
            + ", "
            + str(precision)
            + ", "
            + str(width)
            + ")"
        )

    def format_hex(self, number: int, width: int) -> str:
        return self.__conn._fnc("FORMAT.HEX(" + str(number) + ", " + str(width) + ")")

    def format_string(self, fill_character: int, width: int, source_string: int) -> str:
        return self.__conn._fnc(
            "FORMAT.STRing("
            + str(fill_character)
            + ", "
            + str(width)
            + ", "
            + str(source_string)
            + ")"
        )

    def format_time(self, tim: int, scale_in: int, pprec: int, plen: int) -> str:
        return self.__conn._fnc(
            "FORMAT.Time("
            + str(tim)
            + ", "
            + str(scale_in)
            + ", "
            + str(pprec)
            + ", "
            + str(plen)
            + ")"
        )

    def format_unixtime(self, utc_offset: int, timestamp: int, formatstr: int) -> str:
        return self.__conn._fnc(
            "FORMAT.UnixTime("
            + str(utc_offset)
            + ", "
            + str(timestamp)
            + ", "
            + str(formatstr)
            + ")"
        )

    def dialog_boolean(self, label: int) -> bool:
        return self.__conn._fnc("DIALOG.BOOLEAN(" + str(label) + ")")

    def dialog_exist(self, label: int) -> bool:
        return self.__conn._fnc("DIALOG.EXIST(" + str(label) + ")")

    def dialog_string(self, label: int) -> str:
        return self.__conn._fnc("DIALOG.STRing(" + str(label) + ")")

    def dialog_string2(self, label: int) -> str:
        return self.__conn._fnc("DIALOG.STRing2(" + str(label) + ")")

    def window_command(self, window_name: int) -> str:
        return self.__conn._fnc("WINdow.COMMAND(" + str(window_name) + ")")

    def window_exist(self, window_name: int) -> bool:
        return self.__conn._fnc("WINdow.EXIST(" + str(window_name) + ")")

    def window_position(self, position_item_name: int, window_name: int) -> float:
        return self.__conn._fnc(
            "WINdow.POSition(" + str(position_item_name) + ", " + str(window_name) + ")"
        )

    def winpage_exist(self, page_name: int) -> bool:
        return self.__conn._fnc("WINPAGE.EXIST(" + str(page_name) + ")")

    def title(self) -> str:
        return self.__conn._fnc("TITLE()")

    def false(self) -> bool:
        return self.__conn._fnc("FALSE()")

    def true(self) -> bool:
        return self.__conn._fnc("TRUE()")

    def simulator(self) -> bool:
        return self.__conn._fnc("SIMULATOR()")

    def headid(self) -> int:
        return self.__conn._fnc("HEADID()")

    def __file__(self) -> str:
        return self.__conn._fnc("__FILE__()")

    def __line__(self) -> int:
        return self.__conn._fnc("__LINE__()")

    def dongleid(self, wibukey_index: int) -> int:
        return self.__conn._fnc("DONGLEID(" + str(wibukey_index) + ")")

    def hostid(self) -> int:
        return self.__conn._fnc("HOSTID()")

    def hostip(self) -> int:
        return self.__conn._fnc("HOSTIP()")

    def language(self) -> str:
        return self.__conn._fnc("LANGUAGE()")

    def nodename(self) -> str:
        return self.__conn._fnc("NODENAME()")

    def software_64bit(self) -> bool:
        return self.__conn._fnc("SOFTWARE.64BIT()")

    def software_build(self) -> int:
        return self.__conn._fnc("SOFTWARE.BUILD()")

    def software_build_base(self) -> int:
        return self.__conn._fnc("SOFTWARE.BUILD.BASE()")

    def software_scubased(self) -> bool:
        return self.__conn._fnc("SOFTWARE.SCUBASED()")

    def software_version(self) -> str:
        return self.__conn._fnc("SOFTWARE.VERSION()")

    def config_screen(self) -> bool:
        return self.__conn._fnc("CONFIG.SCREEN()")

    def diag_memusage(self) -> int:
        return self.__conn._fnc("DIAG.MEMUSAGE()")

    def iftest_download(self) -> int:
        return self.__conn._fnc("IFTEST.DOWNLOAD()")

    def iftest_latency(self) -> object:
        return self.__conn._fnc("IFTEST.LATENCY()")

    def iftest_upload(self) -> int:
        return self.__conn._fnc("IFTEST.UPLOAD()")

    def ifconfig_collisions(self) -> int:
        return self.__conn._fnc("IFCONFIG.COLLISIONS()")

    def ifconfig_configuration(self) -> str:
        return self.__conn._fnc("IFCONFIG.CONFIGURATION()")

    def ifconfig_devicename(self) -> str:
        return self.__conn._fnc("IFCONFIG.DEVICENAME()")

    def ifconfig_errors(self) -> int:
        return self.__conn._fnc("IFCONFIG.ERRORS()")

    def ifconfig_ethernetaddress(self) -> int:
        return self.__conn._fnc("IFCONFIG.ETHernetADDRESS()")

    def ifconfig_ipaddress(self) -> str:
        return self.__conn._fnc("IFCONFIG.IPADDRESS()")

    def ifconfig_resyncs(self) -> int:
        return self.__conn._fnc("IFCONFIG.RESYNCS()")

    def ifconfig_retries(self) -> int:
        return self.__conn._fnc("IFCONFIG.RETRIES()")

    def practice_arg_size(self) -> int:
        return self.__conn._fnc("PRACTICE.ARG.SIZE()")

    def practice_caller_file(self, index: int) -> str:
        return self.__conn._fnc("PRACTICE.CALLER.FILE(" + str(index) + ")")

    def practice_caller_line(self, index: int) -> int:
        return self.__conn._fnc("PRACTICE.CALLER.LINE(" + str(index) + ")")

    def practice_command_available(self, command: int) -> bool:
        return self.__conn._fnc("PRACTICE.CoMmanD.AVAILable(" + str(command) + ")")

    def practice_function_available(self, function: int) -> bool:
        return self.__conn._fnc("PRACTICE.FUNCtion.AVAILable(" + str(function) + ")")

    def practice_macro_exist(self, macroName: int) -> bool:
        return self.__conn._fnc("PRACTICE.MACRO.EXIST(" + str(macroName) + ")")

    def printer_filename(self) -> str:
        return self.__conn._fnc("PRINTER.FILENAME()")

    def log_do_file(self) -> str:
        return self.__conn._fnc("LOG.DO.FILE()")

    def test_timeisvalid(self, timevalue: int) -> bool:
        return self.__conn._fnc("TEST.TIMEISVALID(" + str(timevalue) + ")")

    def area_count(self) -> int:
        return self.__conn._fnc("AREA.COUNT()")

    def area_maxcount(self) -> int:
        return self.__conn._fnc("AREA.MAXCOUNT()")

    def area_exist(self, area_name: int) -> bool:
        return self.__conn._fnc("AREA.EXIST(" + str(area_name) + ")")

    def area_line(self, line: int, area_name: int) -> str:
        return self.__conn._fnc(
            "AREA.LINE(" + str(line) + ", " + str(area_name) + ")"
        )

    def area_name(self, index: int) -> str:
        return self.__conn._fnc("AREA.NAME(" + str(index) + ")")

    def area_selected(self) -> str:
        return self.__conn._fnc("AREA.SELECTed()")

    def area_size_lines(self, name: int, presult: int) -> int:
        return self.__conn._fnc(
            "AREA.SIZE.LINES(" + str(name) + ", " + str(presult) + ")"
        )

    def area_size_columns(self, name: int, presult: int) -> int:
        return self.__conn._fnc(
            "AREA.SIZE.COLUMNS(" + str(name) + ", " + str(presult) + ")"
        )

    def path_number(self) -> int:
        return self.__conn._fnc("PATH.NUMBER()")

    def path_path(self, index: int) -> str:
        return self.__conn._fnc("PATH.PATH(" + str(index) + ")")

    def scu_version_ppc(self) -> bool:
        return self.__conn._fnc("SCU_VERSION_PPC()")
