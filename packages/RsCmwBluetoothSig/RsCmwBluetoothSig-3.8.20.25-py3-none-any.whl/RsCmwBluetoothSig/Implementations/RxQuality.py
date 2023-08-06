from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxQuality:
	"""RxQuality commands group definition. 150 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxQuality", core, parent)

	@property
	def iqDrange(self):
		"""iqDrange commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_iqDrange'):
			from .RxQuality_.IqDrange import IqDrange
			self._iqDrange = IqDrange(self._core, self._base)
		return self._iqDrange

	@property
	def iqCoherency(self):
		"""iqCoherency commands group. 2 Sub-classes, 4 commands."""
		if not hasattr(self, '_iqCoherency'):
			from .RxQuality_.IqCoherency import IqCoherency
			self._iqCoherency = IqCoherency(self._core, self._base)
		return self._iqCoherency

	@property
	def search(self):
		"""search commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_search'):
			from .RxQuality_.Search import Search
			self._search = Search(self._core, self._base)
		return self._search

	@property
	def per(self):
		"""per commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_per'):
			from .RxQuality_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	@property
	def ber(self):
		"""ber commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ber'):
			from .RxQuality_.Ber import Ber
			self._ber = Ber(self._core, self._base)
		return self._ber

	@property
	def trace(self):
		"""trace commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .RxQuality_.Trace import Trace
			self._trace = Trace(self._core, self._base)
		return self._trace

	def clone(self) -> 'RxQuality':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxQuality(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
