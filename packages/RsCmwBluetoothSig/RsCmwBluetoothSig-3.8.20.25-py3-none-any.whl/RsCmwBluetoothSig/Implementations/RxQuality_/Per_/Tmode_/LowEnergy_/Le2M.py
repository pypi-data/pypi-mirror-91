from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2M:
	"""Le2M commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le2M", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Per: float: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Cor_Packets_Recv: float: decimal Number of correct received packets reported by the EUT Range: 0 to 30E+3
			- Ber: float: float Bit error rate Range: 0 % to 100 %
			- Packets_Received: float: decimal Number of received packets detected by the R&S CMW Range: 0 to 30E+3
			- Num_Invalid_Crc: enums.ResultStatus2: decimal Number of packets with detected CRC error
			- Num_Pattern_Err: enums.ResultStatus2: decimal Number of packets with detected pattern error
			- Num_Payload_Err: enums.ResultStatus2: decimal Number of packets with detected payload length error
			- Bit_Errors: enums.ResultStatus2: decimal Number of detected bit errors"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_float('Cor_Packets_Recv'),
			ArgStruct.scalar_float('Ber'),
			ArgStruct.scalar_float('Packets_Received'),
			ArgStruct.scalar_enum('Num_Invalid_Crc', enums.ResultStatus2),
			ArgStruct.scalar_enum('Num_Pattern_Err', enums.ResultStatus2),
			ArgStruct.scalar_enum('Num_Payload_Err', enums.ResultStatus2),
			ArgStruct.scalar_enum('Bit_Errors', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Cor_Packets_Recv: float = None
			self.Ber: float = None
			self.Packets_Received: float = None
			self.Num_Invalid_Crc: enums.ResultStatus2 = None
			self.Num_Pattern_Err: enums.ResultStatus2 = None
			self.Num_Payload_Err: enums.ResultStatus2 = None
			self.Bit_Errors: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:PER:TMODe:LENergy:LE2M \n
		Snippet: value: CalculateStruct = driver.rxQuality.per.tmode.lowEnergy.le2M.calculate() \n
		Return all results of the signaling Rx measurement in LE test mode. Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M.
		.) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..:TMODe:LENergy:LRANge..) are available. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:PER:TMODe:LENergy:LE2M?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Per: float: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Cor_Packets_Recv: int: decimal Number of correct received packets reported by the EUT Range: 0 to 30E+3
			- Ber: float: float Bit error rate Range: 0 % to 100 %
			- Packets_Received: int: decimal Number of received packets detected by the R&S CMW Range: 0 to 30E+3
			- Num_Invalid_Crc: int: decimal Number of packets with detected CRC error
			- Num_Pattern_Err: int: decimal Number of packets with detected pattern error
			- Num_Payload_Err: int: decimal Number of packets with detected payload length error
			- Bit_Errors: int: decimal Number of detected bit errors"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_int('Cor_Packets_Recv'),
			ArgStruct.scalar_float('Ber'),
			ArgStruct.scalar_int('Packets_Received'),
			ArgStruct.scalar_int('Num_Invalid_Crc'),
			ArgStruct.scalar_int('Num_Pattern_Err'),
			ArgStruct.scalar_int('Num_Payload_Err'),
			ArgStruct.scalar_int('Bit_Errors')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Cor_Packets_Recv: int = None
			self.Ber: float = None
			self.Packets_Received: int = None
			self.Num_Invalid_Crc: int = None
			self.Num_Pattern_Err: int = None
			self.Num_Payload_Err: int = None
			self.Bit_Errors: int = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:PER:TMODe:LENergy:LE2M \n
		Snippet: value: ResultData = driver.rxQuality.per.tmode.lowEnergy.le2M.fetch() \n
		Return all results of the signaling Rx measurement in LE test mode. Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M.
		.) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..:TMODe:LENergy:LRANge..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:PER:TMODe:LENergy:LE2M?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:PER:TMODe:LENergy:LE2M \n
		Snippet: value: ResultData = driver.rxQuality.per.tmode.lowEnergy.le2M.read() \n
		Return all results of the signaling Rx measurement in LE test mode. Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M.
		.) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..:TMODe:LENergy:LRANge..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:PER:TMODe:LENergy:LE2M?', self.__class__.ResultData())
