from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Connection:
	"""Connection commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("connection", core, parent)

	@property
	def packets(self):
		"""packets commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_packets'):
			from .Connection_.Packets import Packets
			self._packets = Packets(self._core, self._base)
		return self._packets

	def clone(self) -> 'Connection':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Connection(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
