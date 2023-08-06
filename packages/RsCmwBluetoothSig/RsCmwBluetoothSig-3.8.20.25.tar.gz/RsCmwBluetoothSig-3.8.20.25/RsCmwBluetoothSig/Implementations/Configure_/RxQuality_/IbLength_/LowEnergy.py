from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	class Le1MStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Inter_Burst_Len: int: integer Range: 0 slot(s) to 255 slot(s)"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_int('Inter_Burst_Len')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Inter_Burst_Len: int = None

	def get_le_1_m(self) -> Le1MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE1M \n
		Snippet: value: Le1MStruct = driver.configure.rxQuality.ibLength.lowEnergy.get_le_1_m() \n
		Enables and sets the number of slots to wait between transmissions for direction finding tests. \n
			:return: structure: for return value, see the help for Le1MStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE1M?', self.__class__.Le1MStruct())

	def set_le_1_m(self, value: Le1MStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE1M \n
		Snippet: driver.configure.rxQuality.ibLength.lowEnergy.set_le_1_m(value = Le1MStruct()) \n
		Enables and sets the number of slots to wait between transmissions for direction finding tests. \n
			:param value: see the help for Le1MStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE1M', value)

	# noinspection PyTypeChecker
	class Le2MStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Inter_Burst_Len: int: integer Range: 0 slot(s) to 255 slot(s)"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_int('Inter_Burst_Len')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Inter_Burst_Len: int = None

	def get_le_2_m(self) -> Le2MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE2M \n
		Snippet: value: Le2MStruct = driver.configure.rxQuality.ibLength.lowEnergy.get_le_2_m() \n
		Enables and sets the number of slots to wait between transmissions for direction finding tests. \n
			:return: structure: for return value, see the help for Le2MStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE2M?', self.__class__.Le2MStruct())

	def set_le_2_m(self, value: Le2MStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.ibLength.lowEnergy.set_le_2_m(value = Le2MStruct()) \n
		Enables and sets the number of slots to wait between transmissions for direction finding tests. \n
			:param value: see the help for Le2MStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE2M', value)
