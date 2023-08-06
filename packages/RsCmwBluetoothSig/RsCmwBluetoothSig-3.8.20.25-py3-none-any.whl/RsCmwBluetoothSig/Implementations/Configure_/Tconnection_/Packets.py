from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Packets:
	"""Packets commands group definition. 6 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("packets", core, parent)

	@property
	def pattern(self):
		"""pattern commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pattern'):
			from .Packets_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def packetLength(self):
		"""packetLength commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_packetLength'):
			from .Packets_.PacketLength import PacketLength
			self._packetLength = PacketLength(self._core, self._base)
		return self._packetLength

	def clone(self) -> 'Packets':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Packets(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
