from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scenario:
	"""Scenario commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scenario", core, parent)

	@property
	def otRx(self):
		"""otRx commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_otRx'):
			from .Scenario_.OtRx import OtRx
			self._otRx = OtRx(self._core, self._base)
		return self._otRx

	# noinspection PyTypeChecker
	def get_state(self) -> enums.ConnectionState:
		"""SCPI: ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:STATe \n
		Snippet: value: enums.ConnectionState = driver.route.scenario.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.ConnectionState)

	def clone(self) -> 'Scenario':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scenario(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
