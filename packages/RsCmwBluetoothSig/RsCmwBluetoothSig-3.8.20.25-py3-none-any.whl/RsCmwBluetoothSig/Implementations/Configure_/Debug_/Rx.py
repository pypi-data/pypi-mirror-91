from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rx:
	"""Rx commands group definition. 3 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rx", core, parent)

	@property
	def correlation(self):
		"""correlation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_correlation'):
			from .Rx_.Correlation import Correlation
			self._correlation = Correlation(self._core, self._base)
		return self._correlation

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Rx_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def clone(self) -> 'Rx':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rx(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
