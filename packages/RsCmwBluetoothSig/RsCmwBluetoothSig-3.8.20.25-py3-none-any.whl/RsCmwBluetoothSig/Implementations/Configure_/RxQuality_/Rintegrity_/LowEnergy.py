from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	def get_lrange(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LRANge \n
		Snippet: value: bool = driver.configure.rxQuality.rintegrity.lowEnergy.get_lrange() \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE RF tests (direct test mode) : Commands for LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:return: report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LRANge?')
		return Conversions.str_to_bool(response)

	def set_lrange(self, report_integrity: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LRANge \n
		Snippet: driver.configure.rxQuality.rintegrity.lowEnergy.set_lrange(report_integrity = False) \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE RF tests (direct test mode) : Commands for LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:param report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		param = Conversions.bool_to_str(report_integrity)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LRANge {param}')

	def get_le_2_m(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LE2M \n
		Snippet: value: bool = driver.configure.rxQuality.rintegrity.lowEnergy.get_le_2_m() \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE RF tests (direct test mode) : Commands for LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:return: report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LE2M?')
		return Conversions.str_to_bool(response)

	def set_le_2_m(self, report_integrity: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.rintegrity.lowEnergy.set_le_2_m(report_integrity = False) \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE RF tests (direct test mode) : Commands for LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:param report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		param = Conversions.bool_to_str(report_integrity)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LE2M {param}')

	def get_le_1_m(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy[:LE1M] \n
		Snippet: value: bool = driver.configure.rxQuality.rintegrity.lowEnergy.get_le_1_m() \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE RF tests (direct test mode) : Commands for LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:return: report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LE1M?')
		return Conversions.str_to_bool(response)

	def set_le_1_m(self, report_integrity: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy[:LE1M] \n
		Snippet: driver.configure.rxQuality.rintegrity.lowEnergy.set_le_1_m(report_integrity = False) \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE RF tests (direct test mode) : Commands for LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:param report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		param = Conversions.bool_to_str(report_integrity)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:RINTegrity:LENergy:LE1M {param}')
