from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Address:
	"""Address commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("address", core, parent)

	@property
	def cmw(self):
		"""cmw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmw'):
			from .Address_.Cmw import Cmw
			self._cmw = Cmw(self._core, self._base)
		return self._cmw

	@property
	def eut(self):
		"""eut commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eut'):
			from .Address_.Eut import Eut
			self._eut = Eut(self._core, self._base)
		return self._eut

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Address_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	def clone(self) -> 'Address':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Address(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
