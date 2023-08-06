from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmode:
	"""Tmode commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmode", core, parent)

	def get_low_energy(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TMODe:LENergy \n
		Snippet: value: bool = driver.configure.tmode.get_low_energy() \n
		Enables or disables LE test mode at the R&S CMW. \n
			:return: enable_test_mode: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TMODe:LENergy?')
		return Conversions.str_to_bool(response)

	def set_low_energy(self, enable_test_mode: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TMODe:LENergy \n
		Snippet: driver.configure.tmode.set_low_energy(enable_test_mode = False) \n
		Enables or disables LE test mode at the R&S CMW. \n
			:param enable_test_mode: OFF | ON
		"""
		param = Conversions.bool_to_str(enable_test_mode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TMODe:LENergy {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.TestMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TMODe \n
		Snippet: value: enums.TestMode = driver.configure.tmode.get_value() \n
		Selects the test mode that the EUT enters in a test mode connection. \n
			:return: test_mode: LOOPback | TXTest LOOPback: BR/EDR loopback test mode TXTest: BR/EDR transmitter test mode
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TestMode)

	def set_value(self, test_mode: enums.TestMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TMODe \n
		Snippet: driver.configure.tmode.set_value(test_mode = enums.TestMode.LOOPback) \n
		Selects the test mode that the EUT enters in a test mode connection. \n
			:param test_mode: LOOPback | TXTest LOOPback: BR/EDR loopback test mode TXTest: BR/EDR transmitter test mode
		"""
		param = Conversions.enum_scalar_to_str(test_mode, enums.TestMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TMODe {param}')
