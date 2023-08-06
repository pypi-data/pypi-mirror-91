from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DtMode:
	"""DtMode commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dtMode", core, parent)

	@property
	def endTx(self):
		"""endTx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_endTx'):
			from .DtMode_.EndTx import EndTx
			self._endTx = EndTx(self._core, self._base)
		return self._endTx

	@property
	def startTx(self):
		"""startTx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_startTx'):
			from .DtMode_.StartTx import StartTx
			self._startTx = StartTx(self._core, self._base)
		return self._startTx

	def clone(self) -> 'DtMode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DtMode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
