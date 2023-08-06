from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AntMeanAmp:
	"""AntMeanAmp commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("antMeanAmp", core, parent)

	@property
	def limit(self):
		"""limit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .AntMeanAmp_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	def clone(self) -> 'AntMeanAmp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AntMeanAmp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
