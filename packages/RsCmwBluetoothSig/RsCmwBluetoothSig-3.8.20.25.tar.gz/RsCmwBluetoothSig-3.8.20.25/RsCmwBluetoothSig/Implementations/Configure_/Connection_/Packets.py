from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Packets:
	"""Packets commands group definition. 21 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("packets", core, parent)

	@property
	def ptype(self):
		"""ptype commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_ptype'):
			from .Packets_.Ptype import Ptype
			self._ptype = Ptype(self._core, self._base)
		return self._ptype

	@property
	def packetLength(self):
		"""packetLength commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_packetLength'):
			from .Packets_.PacketLength import PacketLength
			self._packetLength = PacketLength(self._core, self._base)
		return self._packetLength

	@property
	def pattern(self):
		"""pattern commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_pattern'):
			from .Packets_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def units(self):
		"""units commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_units'):
			from .Packets_.Units import Units
			self._units = Units(self._core, self._base)
		return self._units

	@property
	def typePy(self):
		"""typePy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_typePy'):
			from .Packets_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	def clone(self) -> 'Packets':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Packets(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
