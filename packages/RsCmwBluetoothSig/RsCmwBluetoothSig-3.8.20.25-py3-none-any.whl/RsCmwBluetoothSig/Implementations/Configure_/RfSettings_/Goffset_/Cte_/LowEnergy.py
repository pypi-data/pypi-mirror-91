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
			- Ant_1_Gain_Offset: float: numeric Range: -20 dB to 6 dB
			- Ant_2_Gain_Offset: float: numeric Range: -20 dB to 6 dB
			- Ant_3_Gain_Offset: float: numeric Range: -20 dB to 6 dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ant_1_Gain_Offset'),
			ArgStruct.scalar_float('Ant_2_Gain_Offset'),
			ArgStruct.scalar_float('Ant_3_Gain_Offset')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ant_1_Gain_Offset: float = None
			self.Ant_2_Gain_Offset: float = None
			self.Ant_3_Gain_Offset: float = None

	def get_le_1_m(self) -> Le1MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE1M \n
		Snippet: value: Le1MStruct = driver.configure.rfSettings.goffset.cte.lowEnergy.get_le_1_m() \n
		Specifies the gain offset for non-reference antennas relative to the gain (or attenuation) of reference antenna for IQ
		sample dynamic range measurements. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for Le1MStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE1M?', self.__class__.Le1MStruct())

	def set_le_1_m(self, value: Le1MStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE1M \n
		Snippet: driver.configure.rfSettings.goffset.cte.lowEnergy.set_le_1_m(value = Le1MStruct()) \n
		Specifies the gain offset for non-reference antennas relative to the gain (or attenuation) of reference antenna for IQ
		sample dynamic range measurements. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param value: see the help for Le1MStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE1M', value)

	# noinspection PyTypeChecker
	class Le2MStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ant_1_Gain_Offset: float: numeric Range: -20 dB to 6 dB
			- Ant_2_Gain_Offset: float: numeric Range: -20 dB to 6 dB
			- Ant_3_Gain_Offset: float: numeric Range: -20 dB to 6 dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ant_1_Gain_Offset'),
			ArgStruct.scalar_float('Ant_2_Gain_Offset'),
			ArgStruct.scalar_float('Ant_3_Gain_Offset')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ant_1_Gain_Offset: float = None
			self.Ant_2_Gain_Offset: float = None
			self.Ant_3_Gain_Offset: float = None

	def get_le_2_m(self) -> Le2MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE2M \n
		Snippet: value: Le2MStruct = driver.configure.rfSettings.goffset.cte.lowEnergy.get_le_2_m() \n
		Specifies the gain offset for non-reference antennas relative to the gain (or attenuation) of reference antenna for IQ
		sample dynamic range measurements. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for Le2MStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE2M?', self.__class__.Le2MStruct())

	def set_le_2_m(self, value: Le2MStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE2M \n
		Snippet: driver.configure.rfSettings.goffset.cte.lowEnergy.set_le_2_m(value = Le2MStruct()) \n
		Specifies the gain offset for non-reference antennas relative to the gain (or attenuation) of reference antenna for IQ
		sample dynamic range measurements. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param value: see the help for Le2MStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE2M', value)
