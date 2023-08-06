from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2M:
	"""Le2M commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le2M", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Per: float: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Packets_Received: int: decimal Number of correct packets received and reported by the EUT Range: 0 to 30E+3
			- Search_Result: float: float TX level of the R&S CMW resulting in the configured PER search limit Range: -999 dBm to 0 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_int('Packets_Received'),
			ArgStruct.scalar_float('Search_Result')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Packets_Received: int = None
			self.Search_Result: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:NMODe:LENergy:LE2M \n
		Snippet: value: ResultData = driver.rxQuality.search.per.nmode.lowEnergy.le2M.read() \n
		Return the results of PER search RX measurement for LE direct test mode and LE connection tests.
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:NMODe:LENergy:LE2M?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:NMODe:LENergy:LE2M \n
		Snippet: value: ResultData = driver.rxQuality.search.per.nmode.lowEnergy.le2M.fetch() \n
		Return the results of PER search RX measurement for LE direct test mode and LE connection tests.
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:NMODe:LENergy:LE2M?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Per: float: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Packets_Received: float: decimal Number of correct packets received and reported by the EUT Range: 0 to 30E+3
			- Search_Result: float: float TX level of the R&S CMW resulting in the configured PER search limit Range: -999 dBm to 0 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_float('Packets_Received'),
			ArgStruct.scalar_float('Search_Result')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Packets_Received: float = None
			self.Search_Result: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:NMODe:LENergy:LE2M \n
		Snippet: value: CalculateStruct = driver.rxQuality.search.per.nmode.lowEnergy.le2M.calculate() \n
		Return the results of PER search RX measurement for LE direct test mode and LE connection tests.
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:NMODe:LENergy:LE2M?', self.__class__.CalculateStruct())
