from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ComSettings:
	"""ComSettings commands group definition. 8 total commands, 8 Sub-groups, 0 group commands
	Repeated Capability: CommSettings, default value after init: CommSettings.Hw1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("comSettings", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_commSettings_get', 'repcap_commSettings_set', repcap.CommSettings.Hw1)

	def repcap_commSettings_set(self, enum_value: repcap.CommSettings) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CommSettings.Default
		Default value after init: CommSettings.Hw1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_commSettings_get(self) -> repcap.CommSettings:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def stopBits(self):
		"""stopBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stopBits'):
			from .ComSettings_.StopBits import StopBits
			self._stopBits = StopBits(self._core, self._base)
		return self._stopBits

	@property
	def parity(self):
		"""parity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_parity'):
			from .ComSettings_.Parity import Parity
			self._parity = Parity(self._core, self._base)
		return self._parity

	@property
	def dbits(self):
		"""dbits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dbits'):
			from .ComSettings_.Dbits import Dbits
			self._dbits = Dbits(self._core, self._base)
		return self._dbits

	@property
	def comPort(self):
		"""comPort commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_comPort'):
			from .ComSettings_.ComPort import ComPort
			self._comPort = ComPort(self._core, self._base)
		return self._comPort

	@property
	def baudrate(self):
		"""baudrate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_baudrate'):
			from .ComSettings_.Baudrate import Baudrate
			self._baudrate = Baudrate(self._core, self._base)
		return self._baudrate

	@property
	def protocol(self):
		"""protocol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_protocol'):
			from .ComSettings_.Protocol import Protocol
			self._protocol = Protocol(self._core, self._base)
		return self._protocol

	@property
	def ereset(self):
		"""ereset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ereset'):
			from .ComSettings_.Ereset import Ereset
			self._ereset = Ereset(self._core, self._base)
		return self._ereset

	@property
	def ports(self):
		"""ports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ports'):
			from .ComSettings_.Ports import Ports
			self._ports = Ports(self._core, self._base)
		return self._ports

	def clone(self) -> 'ComSettings':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ComSettings(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
