from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)

	@property
	def tmode(self):
		"""tmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmode'):
			from .Step_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	@property
	def nmode(self):
		"""nmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nmode'):
			from .Step_.Nmode import Nmode
			self._nmode = Nmode(self._core, self._base)
		return self._nmode

	def get_bredr(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:BREDr \n
		Snippet: value: float or bool = driver.configure.rxQuality.search.step.get_bredr() \n
		Specifies the power step for the BR/EDR search iteration of BER search measurements. \n
			:return: level_step: numeric Range: 0.01 dBm to 5 dBm, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:BREDr?')
		return Conversions.str_to_float_or_bool(response)

	def set_bredr(self, level_step: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:BREDr \n
		Snippet: driver.configure.rxQuality.search.step.set_bredr(level_step = 1.0) \n
		Specifies the power step for the BR/EDR search iteration of BER search measurements. \n
			:param level_step: numeric Range: 0.01 dBm to 5 dBm, Unit: dB
		"""
		param = Conversions.decimal_or_bool_value_to_str(level_step)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:BREDr {param}')

	def get_low_energy(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:LENergy \n
		Snippet: value: float or bool = driver.configure.rxQuality.search.step.get_low_energy() \n
		Specifies the power step for the LE search iteration of PER search measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- For LE connection tests (normal mode) , command for LE 1M PHY - uncoded (..:NMODe:LENergy:LE1M..) is available.
			- For LE test mode, command ..:SEARch:STEP:TMODe:LENergy.. is available.
			- For LE RF tests (direct test mode) , command ..:SEARch:STEP:LENergy.. is available. \n
			:return: level_step: numeric Range: 0.01 dB to 5 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:LENergy?')
		return Conversions.str_to_float_or_bool(response)

	def set_low_energy(self, level_step: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:LENergy \n
		Snippet: driver.configure.rxQuality.search.step.set_low_energy(level_step = 1.0) \n
		Specifies the power step for the LE search iteration of PER search measurements.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- For LE connection tests (normal mode) , command for LE 1M PHY - uncoded (..:NMODe:LENergy:LE1M..) is available.
			- For LE test mode, command ..:SEARch:STEP:TMODe:LENergy.. is available.
			- For LE RF tests (direct test mode) , command ..:SEARch:STEP:LENergy.. is available. \n
			:param level_step: numeric Range: 0.01 dB to 5 dB, Unit: dB
		"""
		param = Conversions.decimal_or_bool_value_to_str(level_step)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:STEP:LENergy {param}')

	def clone(self) -> 'Step':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Step(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
