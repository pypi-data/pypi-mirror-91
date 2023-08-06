from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UsbSettings:
	"""UsbSettings commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: UsbSettings, default value after init: UsbSettings.Sett1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("usbSettings", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_usbSettings_get', 'repcap_usbSettings_set', repcap.UsbSettings.Sett1)

	def repcap_usbSettings_set(self, enum_value: repcap.UsbSettings) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UsbSettings.Default
		Default value after init: UsbSettings.Sett1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_usbSettings_get(self) -> repcap.UsbSettings:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def usbDevice(self):
		"""usbDevice commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_usbDevice'):
			from .UsbSettings_.UsbDevice import UsbDevice
			self._usbDevice = UsbDevice(self._core, self._base)
		return self._usbDevice

	@property
	def devices(self):
		"""devices commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_devices'):
			from .UsbSettings_.Devices import Devices
			self._devices = Devices(self._core, self._base)
		return self._devices

	def clone(self) -> 'UsbSettings':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UsbSettings(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
