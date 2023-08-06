from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mindex:
	"""Mindex commands group definition. 18 total commands, 5 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mindex", core, parent)

	@property
	def nmode(self):
		"""nmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmode'):
			from .Mindex_.Nmode import Nmode
			self._nmode = Nmode(self._core, self._base)
		return self._nmode

	@property
	def standard(self):
		"""standard commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_standard'):
			from .Mindex_.Standard import Standard
			self._standard = Standard(self._core, self._base)
		return self._standard

	@property
	def stable(self):
		"""stable commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_stable'):
			from .Mindex_.Stable import Stable
			self._stable = Stable(self._core, self._base)
		return self._stable

	@property
	def tmode(self):
		"""tmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmode'):
			from .Mindex_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Mindex_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	def get_brate(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:BRATe \n
		Snippet: value: float or bool = driver.configure.rfSettings.dtx.sing.mindex.get_brate() \n
		Specifies the modulation corruption of the signal. Modulation index of 0.32 means no corruption. \n
			:return: mod_index: numeric | ON | OFF Range: 0.2 to 0.44 Additional ON/OFF enables/disables modulation index.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:BRATe?')
		return Conversions.str_to_float_or_bool(response)

	def set_brate(self, mod_index: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:BRATe \n
		Snippet: driver.configure.rfSettings.dtx.sing.mindex.set_brate(mod_index = 1.0) \n
		Specifies the modulation corruption of the signal. Modulation index of 0.32 means no corruption. \n
			:param mod_index: numeric | ON | OFF Range: 0.2 to 0.44 Additional ON/OFF enables/disables modulation index.
		"""
		param = Conversions.decimal_or_bool_value_to_str(mod_index)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:BRATe {param}')

	def clone(self) -> 'Mindex':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mindex(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
