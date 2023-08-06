from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AfHopping:
	"""AfHopping commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("afHopping", core, parent)

	def get_uchannels(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AFHopping:UCHannels \n
		Snippet: value: List[int] = driver.configure.rfSettings.afHopping.get_uchannels() \n
		Specifies user-defined channels for adaptive frequency hopping (AFH) . The setting is relevant for mode = USER, see
		method RsCmwBluetoothSig.Configure.RfSettings.AfHopping.value. \n
			:return: channel_list: integer 79 comma-separated values, one value per channel: 0: channel is blocked for AFH 1: channel is released for AFH Range: 0 to 1
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AFHopping:UCHannels?')
		return response

	def set_uchannels(self, channel_list: List[int]) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AFHopping:UCHannels \n
		Snippet: driver.configure.rfSettings.afHopping.set_uchannels(channel_list = [1, 2, 3]) \n
		Specifies user-defined channels for adaptive frequency hopping (AFH) . The setting is relevant for mode = USER, see
		method RsCmwBluetoothSig.Configure.RfSettings.AfHopping.value. \n
			:param channel_list: integer 79 comma-separated values, one value per channel: 0: channel is blocked for AFH 1: channel is released for AFH Range: 0 to 1
		"""
		param = Conversions.list_to_csv_str(channel_list)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AFHopping:UCHannels {param}')

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Adaptive_Hopping: bool: OFF | ON Disables, enables adaptive hopping.
			- Mode: enums.AfHopingMode: EUT | NORM | USER EUT: only the EUT reports bad channels NORM: both, the EUT and instrument report bad channels USER: bad channels specified manually via [CMDLINK: CONFigure:BLUetooth:SIGNi:RFSettings:AFHopping:UCHannels CMDLINK]"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Adaptive_Hopping'),
			ArgStruct.scalar_enum('Mode', enums.AfHopingMode)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Adaptive_Hopping: bool = None
			self.Mode: enums.AfHopingMode = None

	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AFHopping \n
		Snippet: value: ValueStruct = driver.configure.rfSettings.afHopping.get_value() \n
		Specifies the parameters of adaptive hopping. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AFHopping?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AFHopping \n
		Snippet: driver.configure.rfSettings.afHopping.set_value(value = ValueStruct()) \n
		Specifies the parameters of adaptive hopping. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AFHopping', value)
