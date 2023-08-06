from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	def reset(self) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling<Instance>:LENergy:RESet \n
		Snippet: driver.call.lowEnergy.reset() \n
		Sends the HCI reset command to the EUT via USB. \n
		"""
		self._core.io.write(f'CALL:BLUetooth:SIGNaling<Instance>:LENergy:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling<Instance>:LENergy:RESet \n
		Snippet: driver.call.lowEnergy.reset_with_opc() \n
		Sends the HCI reset command to the EUT via USB. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALL:BLUetooth:SIGNaling<Instance>:LENergy:RESet')
