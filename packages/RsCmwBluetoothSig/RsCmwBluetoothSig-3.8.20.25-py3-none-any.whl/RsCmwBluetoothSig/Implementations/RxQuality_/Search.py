from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Search:
	"""Search commands group definition. 39 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("search", core, parent)

	@property
	def per(self):
		"""per commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_per'):
			from .Search_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	@property
	def ber(self):
		"""ber commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ber'):
			from .Search_.Ber import Ber
			self._ber = Ber(self._core, self._base)
		return self._ber

	def clone(self) -> 'Search':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Search(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
