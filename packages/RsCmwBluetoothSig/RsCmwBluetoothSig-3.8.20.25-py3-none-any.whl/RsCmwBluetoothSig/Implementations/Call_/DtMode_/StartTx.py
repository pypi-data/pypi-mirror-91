from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StartTx:
	"""StartTx commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("startTx", core, parent)

	def set(self) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling:DTMode:STARttx \n
		Snippet: driver.call.dtMode.startTx.set() \n
		No command help available \n
		"""
		self._core.io.write(f'CALL:BLUetooth:SIGNaling:DTMode:STARttx')

	def set_with_opc(self) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling:DTMode:STARttx \n
		Snippet: driver.call.dtMode.startTx.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALL:BLUetooth:SIGNaling:DTMode:STARttx')
