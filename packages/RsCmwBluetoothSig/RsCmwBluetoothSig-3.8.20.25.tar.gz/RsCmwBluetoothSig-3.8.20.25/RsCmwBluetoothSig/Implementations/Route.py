from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Route:
	"""Route commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("route", core, parent)

	@property
	def scenario(self):
		"""scenario commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_scenario'):
			from .Route_.Scenario import Scenario
			self._scenario = Scenario(self._core, self._base)
		return self._scenario

	def clone(self) -> 'Route':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Route(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
