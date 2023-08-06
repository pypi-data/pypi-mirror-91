from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eut:
	"""Eut commands group definition. 23 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eut", core, parent)

	@property
	def capability(self):
		"""capability commands group. 1 Sub-classes, 10 commands."""
		if not hasattr(self, '_capability'):
			from .Eut_.Capability import Capability
			self._capability = Capability(self._core, self._base)
		return self._capability

	@property
	def information(self):
		"""information commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_information'):
			from .Eut_.Information import Information
			self._information = Information(self._core, self._base)
		return self._information

	@property
	def csettings(self):
		"""csettings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csettings'):
			from .Eut_.Csettings import Csettings
			self._csettings = Csettings(self._core, self._base)
		return self._csettings

	@property
	def powerControl(self):
		"""powerControl commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_powerControl'):
			from .Eut_.PowerControl import PowerControl
			self._powerControl = PowerControl(self._core, self._base)
		return self._powerControl

	def clone(self) -> 'Eut':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Eut(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
