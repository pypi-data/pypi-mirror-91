from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqCoherency:
	"""IqCoherency commands group definition. 8 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iqCoherency", core, parent)

	@property
	def a0Reference(self):
		"""a0Reference commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_a0Reference'):
			from .IqCoherency_.A0Reference import A0Reference
			self._a0Reference = A0Reference(self._core, self._base)
		return self._a0Reference

	@property
	def a1Nreference(self):
		"""a1Nreference commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_a1Nreference'):
			from .IqCoherency_.A1Nreference import A1Nreference
			self._a1Nreference = A1Nreference(self._core, self._base)
		return self._a1Nreference

	@property
	def a2Nreference(self):
		"""a2Nreference commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_a2Nreference'):
			from .IqCoherency_.A2Nreference import A2Nreference
			self._a2Nreference = A2Nreference(self._core, self._base)
		return self._a2Nreference

	@property
	def a3Nreference(self):
		"""a3Nreference commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_a3Nreference'):
			from .IqCoherency_.A3Nreference import A3Nreference
			self._a3Nreference = A3Nreference(self._core, self._base)
		return self._a3Nreference

	def clone(self) -> 'IqCoherency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqCoherency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
