from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tconnection:
	"""Tconnection commands group definition. 11 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tconnection", core, parent)

	@property
	def interval(self):
		"""interval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interval'):
			from .Tconnection_.Interval import Interval
			self._interval = Interval(self._core, self._base)
		return self._interval

	@property
	def spinEnable(self):
		"""spinEnable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spinEnable'):
			from .Tconnection_.SpinEnable import SpinEnable
			self._spinEnable = SpinEnable(self._core, self._base)
		return self._spinEnable

	@property
	def pinCode(self):
		"""pinCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pinCode'):
			from .Tconnection_.PinCode import PinCode
			self._pinCode = PinCode(self._core, self._base)
		return self._pinCode

	@property
	def packets(self):
		"""packets commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_packets'):
			from .Tconnection_.Packets import Packets
			self._packets = Packets(self._core, self._base)
		return self._packets

	@property
	def phy(self):
		"""phy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phy'):
			from .Tconnection_.Phy import Phy
			self._phy = Phy(self._core, self._base)
		return self._phy

	@property
	def fec(self):
		"""fec commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fec'):
			from .Tconnection_.Fec import Fec
			self._fec = Fec(self._core, self._base)
		return self._fec

	def clone(self) -> 'Tconnection':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tconnection(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
