from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	@property
	def all(self):
		"""all commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_all'):
			from .State_.All import All
			self._all = All(self._core, self._base)
		return self._all

	@property
	def bedr(self):
		"""bedr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bedr'):
			from .State_.Bedr import Bedr
			self._bedr = Bedr(self._core, self._base)
		return self._bedr

	def clone(self) -> 'State':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = State(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
