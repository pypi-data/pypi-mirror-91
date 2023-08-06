from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 14 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("limit", core, parent)

	@property
	def mper(self):
		"""mper commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_mper'):
			from .Limit_.Mper import Mper
			self._mper = Mper(self._core, self._base)
		return self._mper

	@property
	def mber(self):
		"""mber commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_mber'):
			from .Limit_.Mber import Mber
			self._mber = Mber(self._core, self._base)
		return self._mber

	def clone(self) -> 'Limit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Limit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
