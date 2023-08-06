from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stab:
	"""Stab commands group definition. 51 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stab", core, parent)

	@property
	def mindex(self):
		"""mindex commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_mindex'):
			from .Stab_.Mindex import Mindex
			self._mindex = Mindex(self._core, self._base)
		return self._mindex

	@property
	def stError(self):
		"""stError commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_stError'):
			from .Stab_.StError import StError
			self._stError = StError(self._core, self._base)
		return self._stError

	@property
	def fdrift(self):
		"""fdrift commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_fdrift'):
			from .Stab_.Fdrift import Fdrift
			self._fdrift = Fdrift(self._core, self._base)
		return self._fdrift

	@property
	def freqOffset(self):
		"""freqOffset commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_freqOffset'):
			from .Stab_.FreqOffset import FreqOffset
			self._freqOffset = FreqOffset(self._core, self._base)
		return self._freqOffset

	def clone(self) -> 'Stab':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Stab(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
