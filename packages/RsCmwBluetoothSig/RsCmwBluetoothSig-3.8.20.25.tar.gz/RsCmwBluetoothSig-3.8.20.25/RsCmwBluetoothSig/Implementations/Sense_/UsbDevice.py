from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UsbDevice:
	"""UsbDevice commands group definition. 8 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("usbDevice", core, parent)

	@property
	def information(self):
		"""information commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_information'):
			from .UsbDevice_.Information import Information
			self._information = Information(self._core, self._base)
		return self._information

	def clone(self) -> 'UsbDevice':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UsbDevice(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
