from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_lrange(self) -> enums.DriftRate:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LRANge \n
		Snippet: value: enums.DriftRate = driver.configure.rfSettings.dtx.modFrequency.tmode.lowEnergy.get_lrange() \n
		Specifies the drift rate for LE dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:return: drift_rate: HDRF | LDRF HDRF: 1250 Hz (high drift rate) LDRF: 625 Hz (low drift rate)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.DriftRate)

	def set_lrange(self, drift_rate: enums.DriftRate) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LRANge \n
		Snippet: driver.configure.rfSettings.dtx.modFrequency.tmode.lowEnergy.set_lrange(drift_rate = enums.DriftRate.HDRF) \n
		Specifies the drift rate for LE dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:param drift_rate: HDRF | LDRF HDRF: 1250 Hz (high drift rate) LDRF: 625 Hz (low drift rate)
		"""
		param = Conversions.enum_scalar_to_str(drift_rate, enums.DriftRate)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LRANge {param}')

	# noinspection PyTypeChecker
	def get_le_2_m(self) -> enums.DriftRate:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LE2M \n
		Snippet: value: enums.DriftRate = driver.configure.rfSettings.dtx.modFrequency.tmode.lowEnergy.get_le_2_m() \n
		Specifies the drift rate for LE dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:return: drift_rate: HDRF | LDRF HDRF: 1250 Hz (high drift rate) LDRF: 625 Hz (low drift rate)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LE2M?')
		return Conversions.str_to_scalar_enum(response, enums.DriftRate)

	def set_le_2_m(self, drift_rate: enums.DriftRate) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LE2M \n
		Snippet: driver.configure.rfSettings.dtx.modFrequency.tmode.lowEnergy.set_le_2_m(drift_rate = enums.DriftRate.HDRF) \n
		Specifies the drift rate for LE dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:param drift_rate: HDRF | LDRF HDRF: 1250 Hz (high drift rate) LDRF: 625 Hz (low drift rate)
		"""
		param = Conversions.enum_scalar_to_str(drift_rate, enums.DriftRate)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LE2M {param}')

	# noinspection PyTypeChecker
	def get_le_1_m(self) -> enums.DriftRate:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LE1M \n
		Snippet: value: enums.DriftRate = driver.configure.rfSettings.dtx.modFrequency.tmode.lowEnergy.get_le_1_m() \n
		Specifies the drift rate for LE dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:return: drift_rate: HDRF | LDRF HDRF: 1250 Hz (high drift rate) LDRF: 625 Hz (low drift rate)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LE1M?')
		return Conversions.str_to_scalar_enum(response, enums.DriftRate)

	def set_le_1_m(self, drift_rate: enums.DriftRate) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LE1M \n
		Snippet: driver.configure.rfSettings.dtx.modFrequency.tmode.lowEnergy.set_le_1_m(drift_rate = enums.DriftRate.HDRF) \n
		Specifies the drift rate for LE dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:param drift_rate: HDRF | LDRF HDRF: 1250 Hz (high drift rate) LDRF: 625 Hz (low drift rate)
		"""
		param = Conversions.enum_scalar_to_str(drift_rate, enums.DriftRate)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODFrequency:TMODe:LENergy:LE1M {param}')
