from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nmode:
	"""Nmode commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nmode", core, parent)

	@property
	def hmode(self):
		"""hmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hmode'):
			from .Nmode_.Hmode import Hmode
			self._hmode = Hmode(self._core, self._base)
		return self._hmode

	@property
	def mchannel(self):
		"""mchannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mchannel'):
			from .Nmode_.Mchannel import Mchannel
			self._mchannel = Mchannel(self._core, self._base)
		return self._mchannel

	def clone(self) -> 'Nmode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nmode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
