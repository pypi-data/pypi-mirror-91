from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Swindow:
	"""Swindow commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("swindow", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:SWINdow:LESignaling \n
		Snippet: value: int = driver.configure.connection.inquiry.swindow.get_le_signaling() \n
		Specifies Inquiry Scan Window - the inquiry scan duration. The duration in ms is calculated as the specified value
		multiplied by 0.625 ms. \n
			:return: inq_scan_window: numeric Range: 4 to 16.384E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:SWINdow:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, inq_scan_window: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:SWINdow:LESignaling \n
		Snippet: driver.configure.connection.inquiry.swindow.set_le_signaling(inq_scan_window = 1) \n
		Specifies Inquiry Scan Window - the inquiry scan duration. The duration in ms is calculated as the specified value
		multiplied by 0.625 ms. \n
			:param inq_scan_window: numeric Range: 4 to 16.384E+3
		"""
		param = Conversions.decimal_value_to_str(inq_scan_window)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:SWINdow:LESignaling {param}')
