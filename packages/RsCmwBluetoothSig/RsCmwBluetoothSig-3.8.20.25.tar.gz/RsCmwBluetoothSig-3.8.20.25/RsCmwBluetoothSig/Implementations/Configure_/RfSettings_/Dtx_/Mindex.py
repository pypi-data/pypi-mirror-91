from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mindex:
	"""Mindex commands group definition. 6 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mindex", core, parent)

	@property
	def mode(self):
		"""mode commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_mode'):
			from .Mindex_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	def clone(self) -> 'Mindex':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mindex(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
