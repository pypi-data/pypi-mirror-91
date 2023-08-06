from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rdevices:
	"""Rdevices commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rdevices", core, parent)

	def set(self) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling<Instance>:RDEVices \n
		Snippet: driver.call.rdevices.set() \n
		Detects the DUTs connected to USB ports directly or via a USB-to-COM adapter. \n
		"""
		self._core.io.write(f'CALL:BLUetooth:SIGNaling<Instance>:RDEVices')

	def set_with_opc(self) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling<Instance>:RDEVices \n
		Snippet: driver.call.rdevices.set_with_opc() \n
		Detects the DUTs connected to USB ports directly or via a USB-to-COM adapter. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALL:BLUetooth:SIGNaling<Instance>:RDEVices')
