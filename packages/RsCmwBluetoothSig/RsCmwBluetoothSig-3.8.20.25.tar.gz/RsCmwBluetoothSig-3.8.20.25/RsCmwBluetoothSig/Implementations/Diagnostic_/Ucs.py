from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ucs:
	"""Ucs commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ucs", core, parent)

	# noinspection PyTypeChecker
	def get_state(self) -> enums.LeDiagState:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:STATe \n
		Snippet: value: enums.LeDiagState = driver.diagnostic.ucs.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.LeDiagState)

	# noinspection PyTypeChecker
	class FrequencyStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Cmw_Rx_Frequency: float: No parameter help available
			- Cmw_Tx_Frequency: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Cmw_Rx_Frequency'),
			ArgStruct.scalar_float('Cmw_Tx_Frequency')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cmw_Rx_Frequency: float = None
			self.Cmw_Tx_Frequency: float = None

	def get_frequency(self) -> FrequencyStruct:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:FREQuency \n
		Snippet: value: FrequencyStruct = driver.diagnostic.ucs.get_frequency() \n
		No command help available \n
			:return: structure: for return value, see the help for FrequencyStruct structure arguments.
		"""
		return self._core.io.query_struct('DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:FREQuency?', self.__class__.FrequencyStruct())

	def set_frequency(self, value: FrequencyStruct) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:FREQuency \n
		Snippet: driver.diagnostic.ucs.set_frequency(value = FrequencyStruct()) \n
		No command help available \n
			:param value: see the help for FrequencyStruct structure arguments.
		"""
		self._core.io.write_struct('DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:FREQuency', value)

	def get_mode(self) -> bool:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:MODE \n
		Snippet: value: bool = driver.diagnostic.ucs.get_mode() \n
		No command help available \n
			:return: ucs_mode: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, ucs_mode: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:MODE \n
		Snippet: driver.diagnostic.ucs.set_mode(ucs_mode = False) \n
		No command help available \n
			:param ucs_mode: No help available
		"""
		param = Conversions.bool_to_str(ucs_mode)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:MODE {param}')

	# noinspection PyTypeChecker
	def get_test_vector(self) -> enums.TestVector:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:TESTvector \n
		Snippet: value: enums.TestVector = driver.diagnostic.ucs.get_test_vector() \n
		No command help available \n
			:return: test_vector: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:TESTvector?')
		return Conversions.str_to_scalar_enum(response, enums.TestVector)

	def set_test_vector(self, test_vector: enums.TestVector) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:TESTvector \n
		Snippet: driver.diagnostic.ucs.set_test_vector(test_vector = enums.TestVector.INITstack) \n
		No command help available \n
			:param test_vector: No help available
		"""
		param = Conversions.enum_scalar_to_str(test_vector, enums.TestVector)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:TESTvector {param}')
