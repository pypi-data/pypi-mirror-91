from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rencryption:
	"""Rencryption commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rencryption", core, parent)

	@property
	def leSignaling(self):
		"""leSignaling commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_leSignaling'):
			from .Rencryption_.LeSignaling import LeSignaling
			self._leSignaling = LeSignaling(self._core, self._base)
		return self._leSignaling

	def clone(self) -> 'Rencryption':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rencryption(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
