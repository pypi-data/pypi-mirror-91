from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	def get_lrange(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LRANge \n
		Snippet: value: float or bool = driver.configure.rxQuality.limit.mper.lowEnergy.get_lrange() \n
		Specifies the upper PER limit for LE RX measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:return: limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default value)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LRANge?')
		return Conversions.str_to_float_or_bool(response)

	def set_lrange(self, limit: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LRANge \n
		Snippet: driver.configure.rxQuality.limit.mper.lowEnergy.set_lrange(limit = 1.0) \n
		Specifies the upper PER limit for LE RX measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:param limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default value)
		"""
		param = Conversions.decimal_or_bool_value_to_str(limit)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LRANge {param}')

	def get_le_2_m(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LE2M \n
		Snippet: value: float or bool = driver.configure.rxQuality.limit.mper.lowEnergy.get_le_2_m() \n
		Specifies the upper PER limit for LE RX measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:return: limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default value)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LE2M?')
		return Conversions.str_to_float_or_bool(response)

	def set_le_2_m(self, limit: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.limit.mper.lowEnergy.set_le_2_m(limit = 1.0) \n
		Specifies the upper PER limit for LE RX measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:param limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default value)
		"""
		param = Conversions.decimal_or_bool_value_to_str(limit)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LE2M {param}')

	def get_le_1_m(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy[:LE1M] \n
		Snippet: value: float or bool = driver.configure.rxQuality.limit.mper.lowEnergy.get_le_1_m() \n
		Specifies the upper PER limit for LE RX measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:return: limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default value)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LE1M?')
		return Conversions.str_to_float_or_bool(response)

	def set_le_1_m(self, limit: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy[:LE1M] \n
		Snippet: driver.configure.rxQuality.limit.mper.lowEnergy.set_le_1_m(limit = 1.0) \n
		Specifies the upper PER limit for LE RX measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands ..:NMODe:LENergy:.. are available.
			- LE test mode: Commands ..:TMODe:LENergy:.. are available. \n
			:param limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default value)
		"""
		param = Conversions.decimal_or_bool_value_to_str(limit)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MPER:LENergy:LE1M {param}')
