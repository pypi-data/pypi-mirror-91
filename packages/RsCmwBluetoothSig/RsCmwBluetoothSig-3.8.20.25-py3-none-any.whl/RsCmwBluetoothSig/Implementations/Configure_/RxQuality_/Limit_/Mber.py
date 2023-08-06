from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mber:
	"""Mber commands group definition. 5 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mber", core, parent)

	@property
	def tmode(self):
		"""tmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmode'):
			from .Mber_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	def get_brate(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MBER:BRATe \n
		Snippet: value: float or bool = driver.configure.rxQuality.limit.mber.get_brate() \n
		Specifies the upper BER limit for BR RX measurements. \n
			:return: limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default level)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MBER:BRATe?')
		return Conversions.str_to_float_or_bool(response)

	def set_brate(self, limit: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MBER:BRATe \n
		Snippet: driver.configure.rxQuality.limit.mber.set_brate(limit = 1.0) \n
		Specifies the upper BER limit for BR RX measurements. \n
			:param limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default level)
		"""
		param = Conversions.decimal_or_bool_value_to_str(limit)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MBER:BRATe {param}')

	def get_edrate(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MBER:EDRate \n
		Snippet: value: float or bool = driver.configure.rxQuality.limit.mber.get_edrate() \n
		Specifies the upper BER limit for EDR RX measurements. \n
			:return: limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default level)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MBER:EDRate?')
		return Conversions.str_to_float_or_bool(response)

	def set_edrate(self, limit: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MBER:EDRate \n
		Snippet: driver.configure.rxQuality.limit.mber.set_edrate(limit = 1.0) \n
		Specifies the upper BER limit for EDR RX measurements. \n
			:param limit: numeric | ON | OFF Range: 0 % to 100 %, Unit: % Additional parameters: OFF | ON (disables the limit | enables the limit using the previous/default level)
		"""
		param = Conversions.decimal_or_bool_value_to_str(limit)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:LIMit:MBER:EDRate {param}')

	def clone(self) -> 'Mber':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mber(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
