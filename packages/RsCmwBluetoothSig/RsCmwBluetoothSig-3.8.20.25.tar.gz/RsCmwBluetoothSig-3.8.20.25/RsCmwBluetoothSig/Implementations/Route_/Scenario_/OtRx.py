from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OtRx:
	"""OtRx commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("otRx", core, parent)

	# noinspection PyTypeChecker
	class FlexibleStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Bb_Board: enums.BbBoard: Signaling unit
			- Rx_Connector: enums.RxConnector: RF connector for the input path
			- Rx_Converter: enums.RxConverter: RX module for the input path
			- Tx_Connector: enums.TxConnector: RF connector for the output path
			- Tx_Converter: enums.TxConverter: TX module for the output path"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Bb_Board', enums.BbBoard),
			ArgStruct.scalar_enum('Rx_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rx_Converter', enums.RxConverter),
			ArgStruct.scalar_enum('Tx_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Tx_Converter', enums.TxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Bb_Board: enums.BbBoard = None
			self.Rx_Connector: enums.RxConnector = None
			self.Rx_Converter: enums.RxConverter = None
			self.Tx_Connector: enums.TxConnector = None
			self.Tx_Converter: enums.TxConverter = None

	# noinspection PyTypeChecker
	def get_flexible(self) -> FlexibleStruct:
		"""SCPI: ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX:FLEXible \n
		Snippet: value: FlexibleStruct = driver.route.scenario.otRx.get_flexible() \n
		Activates the scenario with one output and one input signal paths. For possible signaling unit, connector and converter
		values, see 'Values for Signal Path Selection'. \n
			:return: structure: for return value, see the help for FlexibleStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX:FLEXible?', self.__class__.FlexibleStruct())

	def set_flexible(self, value: FlexibleStruct) -> None:
		"""SCPI: ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX:FLEXible \n
		Snippet: driver.route.scenario.otRx.set_flexible(value = FlexibleStruct()) \n
		Activates the scenario with one output and one input signal paths. For possible signaling unit, connector and converter
		values, see 'Values for Signal Path Selection'. \n
			:param value: see the help for FlexibleStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX:FLEXible', value)

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rx_Connector: enums.RxConnector: RF connector for the input path
			- Rx_Converter: enums.RxConverter: RX module for the input path
			- Tx_Connector: enums.TxConnector: RF connector for the output path
			- Tx_Converter: enums.TxConverter: TX module for the output path"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Rx_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rx_Converter', enums.RxConverter),
			ArgStruct.scalar_enum('Tx_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Tx_Converter', enums.TxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rx_Connector: enums.RxConnector = None
			self.Rx_Converter: enums.RxConverter = None
			self.Tx_Connector: enums.TxConnector = None
			self.Tx_Converter: enums.TxConverter = None

	# noinspection PyTypeChecker
	def get_value(self) -> ValueStruct:
		"""SCPI: ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX \n
		Snippet: value: ValueStruct = driver.route.scenario.otRx.get_value() \n
		Activates the scenario with one output and one input signal paths. For possible connector and converter values, see
		'Values for Signal Path Selection'. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX \n
		Snippet: driver.route.scenario.otRx.set_value(value = ValueStruct()) \n
		Activates the scenario with one output and one input signal paths. For possible connector and converter values, see
		'Values for Signal Path Selection'. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX', value)
