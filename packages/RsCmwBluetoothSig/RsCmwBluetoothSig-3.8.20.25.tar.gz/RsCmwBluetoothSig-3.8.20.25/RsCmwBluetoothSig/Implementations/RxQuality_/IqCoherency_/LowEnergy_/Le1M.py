from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le1M:
	"""Le1M commands group definition. 12 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le1M", core, parent)

	@property
	def a0Reference(self):
		"""a0Reference commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_a0Reference'):
			from .Le1M_.A0Reference import A0Reference
			self._a0Reference = A0Reference(self._core, self._base)
		return self._a0Reference

	@property
	def a1Nreference(self):
		"""a1Nreference commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_a1Nreference'):
			from .Le1M_.A1Nreference import A1Nreference
			self._a1Nreference = A1Nreference(self._core, self._base)
		return self._a1Nreference

	@property
	def a2Nreference(self):
		"""a2Nreference commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_a2Nreference'):
			from .Le1M_.A2Nreference import A2Nreference
			self._a2Nreference = A2Nreference(self._core, self._base)
		return self._a2Nreference

	@property
	def a3Nreference(self):
		"""a3Nreference commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_a3Nreference'):
			from .Le1M_.A3Nreference import A3Nreference
			self._a3Nreference = A3Nreference(self._core, self._base)
		return self._a3Nreference

	def clone(self) -> 'Le1M':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Le1M(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
