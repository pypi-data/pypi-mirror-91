from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Action:
	"""Action commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("action", core, parent)

	def set_le_signaling(self, pcontrol: enums.PowerControl) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion:LESignaling \n
		Snippet: driver.configure.connection.powerControl.step.action.set_le_signaling(pcontrol = enums.PowerControl.DOWN) \n
		Sends a command to the DUT to increase/decrease power. \n
			:param pcontrol: UP | DOWN | MAX One step up, one step down, command to maximum DUT Tx power
		"""
		param = Conversions.enum_scalar_to_str(pcontrol, enums.PowerControl)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion:LESignaling {param}')

	def set_value(self, pcontrol: enums.PowerControl) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion \n
		Snippet: driver.configure.connection.powerControl.step.action.set_value(pcontrol = enums.PowerControl.DOWN) \n
		Sends a command to the EUT to increase/decrease power. \n
			:param pcontrol: UP | DOWN | MAX One step up, one step down, command to maximum EUT power
		"""
		param = Conversions.enum_scalar_to_str(pcontrol, enums.PowerControl)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion {param}')
