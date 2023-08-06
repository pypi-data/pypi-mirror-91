from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Call:
	"""Call commands group definition. 9 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("call", core, parent)

	@property
	def hciCustom(self):
		"""hciCustom commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hciCustom'):
			from .Call_.HciCustom import HciCustom
			self._hciCustom = HciCustom(self._core, self._base)
		return self._hciCustom

	@property
	def rdevices(self):
		"""rdevices commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rdevices'):
			from .Call_.Rdevices import Rdevices
			self._rdevices = Rdevices(self._core, self._base)
		return self._rdevices

	@property
	def dtMode(self):
		"""dtMode commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtMode'):
			from .Call_.DtMode import DtMode
			self._dtMode = DtMode(self._core, self._base)
		return self._dtMode

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Call_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	@property
	def connection(self):
		"""connection commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_connection'):
			from .Call_.Connection import Connection
			self._connection = Connection(self._core, self._base)
		return self._connection

	def clone(self) -> 'Call':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Call(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
