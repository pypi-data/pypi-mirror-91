from typing import List

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

	def get_brate(self) -> List[float or bool]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:BRATe \n
		Snippet: value: List[float or bool] = driver.configure.rfSettings.dtx.stab.mindex.get_brate() \n
		Return the modulation index under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for BR (..:BRATe..) , LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless
		technology, see also 'Dirty Tx Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: mod_index: float | ON | OFF Range: 0.2 to 0.55
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:BRATe?')
		return Conversions.str_to_float_or_bool_list(response)

	def clone(self) -> 'Mindex':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mindex(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
