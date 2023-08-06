from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerControl:
	"""PowerControl commands group definition. 5 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("powerControl", core, parent)

	@property
	def step(self):
		"""step commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_step'):
			from .PowerControl_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	@property
	def ssize(self):
		"""ssize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssize'):
			from .PowerControl_.Ssize import Ssize
			self._ssize = Ssize(self._core, self._base)
		return self._ssize

	@property
	def pcMode(self):
		"""pcMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcMode'):
			from .PowerControl_.PcMode import PcMode
			self._pcMode = PcMode(self._core, self._base)
		return self._pcMode

	# noinspection PyTypeChecker
	def get_epc_mode(self) -> enums.PowerControlMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:EPCMode \n
		Snippet: value: enums.PowerControlMode = driver.configure.connection.powerControl.get_epc_mode() \n
		Activates/deactivates enhanced power control mode. \n
			:return: pc_mode: AUTO | OFF AUTO : instrument uses enhanced power control if EUT supports it, otherwise it uses legacy power control OFF : instrument uses legacy power control
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:EPCMode?')
		return Conversions.str_to_scalar_enum(response, enums.PowerControlMode)

	def set_epc_mode(self, pc_mode: enums.PowerControlMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:EPCMode \n
		Snippet: driver.configure.connection.powerControl.set_epc_mode(pc_mode = enums.PowerControlMode.AUTO) \n
		Activates/deactivates enhanced power control mode. \n
			:param pc_mode: AUTO | OFF AUTO : instrument uses enhanced power control if EUT supports it, otherwise it uses legacy power control OFF : instrument uses legacy power control
		"""
		param = Conversions.enum_scalar_to_str(pc_mode, enums.PowerControlMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:EPCMode {param}')

	def clone(self) -> 'PowerControl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PowerControl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
