from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpinEnable:
	"""SpinEnable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spinEnable", core, parent)

	def get_low_energy(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:SPINenable:LENergy \n
		Snippet: value: bool = driver.configure.tconnection.spinEnable.get_low_energy() \n
		Enables or disables LE test mode on the DUT using a PIN. The PIN to sent is specified via: method RsCmwBluetoothSig.
		Configure.Tconnection.SpinEnable.lowEnergy \n
			:return: send_enable_pin: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:SPINenable:LENergy?')
		return Conversions.str_to_bool(response)

	def set_low_energy(self, send_enable_pin: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:SPINenable:LENergy \n
		Snippet: driver.configure.tconnection.spinEnable.set_low_energy(send_enable_pin = False) \n
		Enables or disables LE test mode on the DUT using a PIN. The PIN to sent is specified via: method RsCmwBluetoothSig.
		Configure.Tconnection.SpinEnable.lowEnergy \n
			:param send_enable_pin: OFF | ON
		"""
		param = Conversions.bool_to_str(send_enable_pin)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:SPINenable:LENergy {param}')
