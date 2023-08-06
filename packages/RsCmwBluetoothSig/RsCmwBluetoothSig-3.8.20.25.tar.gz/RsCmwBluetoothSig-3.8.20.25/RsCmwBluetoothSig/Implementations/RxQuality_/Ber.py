from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ber:
	"""Ber commands group definition. 8 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ber", core, parent)

	@property
	def state(self):
		"""state commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_state'):
			from .Ber_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def bedr(self):
		"""bedr commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_bedr'):
			from .Ber_.Bedr import Bedr
			self._bedr = Bedr(self._core, self._base)
		return self._bedr

	def clone(self) -> 'Ber':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ber(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
