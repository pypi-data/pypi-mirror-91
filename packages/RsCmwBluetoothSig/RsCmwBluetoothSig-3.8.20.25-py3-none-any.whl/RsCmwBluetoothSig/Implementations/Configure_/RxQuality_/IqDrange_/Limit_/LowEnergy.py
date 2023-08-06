from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	class Le1MStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ref_Ant_Enable: bool: No parameter help available
			- Ant_1_Enable: bool: No parameter help available
			- Ant_2_Enable: bool: No parameter help available
			- Ant_3_Enable: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Ref_Ant_Enable'),
			ArgStruct.scalar_bool('Ant_1_Enable'),
			ArgStruct.scalar_bool('Ant_2_Enable'),
			ArgStruct.scalar_bool('Ant_3_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ref_Ant_Enable: bool = None
			self.Ant_1_Enable: bool = None
			self.Ant_2_Enable: bool = None
			self.Ant_3_Enable: bool = None

	def get_le_1_m(self) -> Le1MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE1M \n
		Snippet: value: Le1MStruct = driver.configure.rxQuality.iqDrange.limit.lowEnergy.get_le_1_m() \n
		No command help available \n
			:return: structure: for return value, see the help for Le1MStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE1M?', self.__class__.Le1MStruct())

	def set_le_1_m(self, value: Le1MStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE1M \n
		Snippet: driver.configure.rxQuality.iqDrange.limit.lowEnergy.set_le_1_m(value = Le1MStruct()) \n
		No command help available \n
			:param value: see the help for Le1MStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE1M', value)

	# noinspection PyTypeChecker
	class Le2MStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ref_Ant_Enable: bool: No parameter help available
			- Ant_1_Enable: bool: No parameter help available
			- Ant_2_Enable: bool: No parameter help available
			- Ant_3_Enable: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Ref_Ant_Enable'),
			ArgStruct.scalar_bool('Ant_1_Enable'),
			ArgStruct.scalar_bool('Ant_2_Enable'),
			ArgStruct.scalar_bool('Ant_3_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ref_Ant_Enable: bool = None
			self.Ant_1_Enable: bool = None
			self.Ant_2_Enable: bool = None
			self.Ant_3_Enable: bool = None

	def get_le_2_m(self) -> Le2MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE2M \n
		Snippet: value: Le2MStruct = driver.configure.rxQuality.iqDrange.limit.lowEnergy.get_le_2_m() \n
		No command help available \n
			:return: structure: for return value, see the help for Le2MStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE2M?', self.__class__.Le2MStruct())

	def set_le_2_m(self, value: Le2MStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.iqDrange.limit.lowEnergy.set_le_2_m(value = Le2MStruct()) \n
		No command help available \n
			:param value: see the help for Le2MStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE2M', value)
