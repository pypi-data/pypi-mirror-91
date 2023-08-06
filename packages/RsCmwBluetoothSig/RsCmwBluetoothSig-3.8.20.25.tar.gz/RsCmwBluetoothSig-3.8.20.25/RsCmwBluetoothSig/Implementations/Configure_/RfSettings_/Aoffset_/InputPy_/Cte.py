from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cte:
	"""Cte commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cte", core, parent)

	# noinspection PyTypeChecker
	class LowEnergyStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ant_1_In_Att_Offset: float: No parameter help available
			- Ant_2_In_Att_Offset: float: No parameter help available
			- Ant_3_In_Att_Offset: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ant_1_In_Att_Offset'),
			ArgStruct.scalar_float('Ant_2_In_Att_Offset'),
			ArgStruct.scalar_float('Ant_3_In_Att_Offset')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ant_1_In_Att_Offset: float = None
			self.Ant_2_In_Att_Offset: float = None
			self.Ant_3_In_Att_Offset: float = None

	def get_low_energy(self) -> LowEnergyStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AOFFset:INPut:CTE:LENergy \n
		Snippet: value: LowEnergyStruct = driver.configure.rfSettings.aoffset.inputPy.cte.get_low_energy() \n
		Specifies the offset of external attenuation per EUT antenna relative to the reference antenna. For the reference antenna,
		the offset is fixed and set to 0 dB. The commands for input and output path are available. An SUA is required. \n
			:return: structure: for return value, see the help for LowEnergyStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AOFFset:INPut:CTE:LENergy?', self.__class__.LowEnergyStruct())

	def set_low_energy(self, value: LowEnergyStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AOFFset:INPut:CTE:LENergy \n
		Snippet: driver.configure.rfSettings.aoffset.inputPy.cte.set_low_energy(value = LowEnergyStruct()) \n
		Specifies the offset of external attenuation per EUT antenna relative to the reference antenna. For the reference antenna,
		the offset is fixed and set to 0 dB. The commands for input and output path are available. An SUA is required. \n
			:param value: see the help for LowEnergyStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AOFFset:INPut:CTE:LENergy', value)
