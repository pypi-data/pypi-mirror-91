from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqCoherency:
	"""IqCoherency commands group definition. 20 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iqCoherency", core, parent)

	@property
	def moException(self):
		"""moException commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_moException'):
			from .IqCoherency_.MoException import MoException
			self._moException = MoException(self._core, self._base)
		return self._moException

	@property
	def noMeas(self):
		"""noMeas commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_noMeas'):
			from .IqCoherency_.NoMeas import NoMeas
			self._noMeas = NoMeas(self._core, self._base)
		return self._noMeas

	@property
	def packets(self):
		"""packets commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_packets'):
			from .IqCoherency_.Packets import Packets
			self._packets = Packets(self._core, self._base)
		return self._packets

	@property
	def limit(self):
		"""limit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .IqCoherency_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	def clone(self) -> 'IqCoherency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqCoherency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
