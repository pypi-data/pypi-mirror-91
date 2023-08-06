from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	class Le1MStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- No_Bits_To_Corrupt: int: No parameter help available
			- Byte_Start_Err: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('No_Bits_To_Corrupt'),
			ArgStruct.scalar_int('Byte_Start_Err')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.No_Bits_To_Corrupt: int = None
			self.Byte_Start_Err: int = None

	def get_le_1_m(self) -> Le1MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE1M \n
		Snippet: value: Le1MStruct = driver.configure.rxQuality.cbits.tmode.lowEnergy.get_le_1_m() \n
		No command help available \n
			:return: structure: for return value, see the help for Le1MStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE1M?', self.__class__.Le1MStruct())

	def set_le_1_m(self, value: Le1MStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE1M \n
		Snippet: driver.configure.rxQuality.cbits.tmode.lowEnergy.set_le_1_m(value = Le1MStruct()) \n
		No command help available \n
			:param value: see the help for Le1MStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE1M', value)

	# noinspection PyTypeChecker
	class Le2MStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- No_Bits_To_Corrupt: int: No parameter help available
			- Byte_Start_Err: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('No_Bits_To_Corrupt'),
			ArgStruct.scalar_int('Byte_Start_Err')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.No_Bits_To_Corrupt: int = None
			self.Byte_Start_Err: int = None

	def get_le_2_m(self) -> Le2MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE2M \n
		Snippet: value: Le2MStruct = driver.configure.rxQuality.cbits.tmode.lowEnergy.get_le_2_m() \n
		No command help available \n
			:return: structure: for return value, see the help for Le2MStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE2M?', self.__class__.Le2MStruct())

	def set_le_2_m(self, value: Le2MStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.cbits.tmode.lowEnergy.set_le_2_m(value = Le2MStruct()) \n
		No command help available \n
			:param value: see the help for Le2MStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE2M', value)

	# noinspection PyTypeChecker
	class LrangeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- No_Bits_To_Corrupt: int: No parameter help available
			- Byte_Start_Err: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('No_Bits_To_Corrupt'),
			ArgStruct.scalar_int('Byte_Start_Err')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.No_Bits_To_Corrupt: int = None
			self.Byte_Start_Err: int = None

	def get_lrange(self) -> LrangeStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LRANge \n
		Snippet: value: LrangeStruct = driver.configure.rxQuality.cbits.tmode.lowEnergy.get_lrange() \n
		No command help available \n
			:return: structure: for return value, see the help for LrangeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LRANge?', self.__class__.LrangeStruct())

	def set_lrange(self, value: LrangeStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LRANge \n
		Snippet: driver.configure.rxQuality.cbits.tmode.lowEnergy.set_lrange(value = LrangeStruct()) \n
		No command help available \n
			:param value: see the help for LrangeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LRANge', value)
