from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PinCode:
	"""PinCode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pinCode", core, parent)

	def get_low_energy(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PINCode:LENergy \n
		Snippet: value: List[int] = driver.configure.tconnection.pinCode.get_low_energy() \n
		Specifies the PIN for LE test mode. The value must match with the configuration on the DUT. \n
			:return: pin: integer Comma-separated sequence of eight integers Range: 0 to 255
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PINCode:LENergy?')
		return response

	def set_low_energy(self, pin: List[int]) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PINCode:LENergy \n
		Snippet: driver.configure.tconnection.pinCode.set_low_energy(pin = [1, 2, 3]) \n
		Specifies the PIN for LE test mode. The value must match with the configuration on the DUT. \n
			:param pin: integer Comma-separated sequence of eight integers Range: 0 to 255
		"""
		param = Conversions.list_to_csv_str(pin)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PINCode:LENergy {param}')
