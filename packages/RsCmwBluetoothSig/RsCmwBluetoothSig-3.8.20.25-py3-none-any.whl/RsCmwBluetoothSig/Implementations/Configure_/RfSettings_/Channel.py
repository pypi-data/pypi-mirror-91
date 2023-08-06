from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channel:
	"""Channel commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channel", core, parent)

	def get_tmode(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TMODe \n
		Snippet: value: int = driver.configure.rfSettings.channel.get_tmode() \n
		Sets the RF channel for LE test mode. This mode supports both data and advertising channels. \n
			:return: rx_tx_chan: numeric Channel number Range: 0 Ch to 39 Ch
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TMODe?')
		return Conversions.str_to_int(response)

	def set_tmode(self, rx_tx_chan: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TMODe \n
		Snippet: driver.configure.rfSettings.channel.set_tmode(rx_tx_chan = 1) \n
		Sets the RF channel for LE test mode. This mode supports both data and advertising channels. \n
			:param rx_tx_chan: numeric Channel number Range: 0 Ch to 39 Ch
		"""
		param = Conversions.decimal_value_to_str(rx_tx_chan)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TMODe {param}')

	def get_dt_mode(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:DTMode \n
		Snippet: value: int = driver.configure.rfSettings.channel.get_dt_mode() \n
		Configures the channel number for direct test mode. \n
			:return: rx_tx_chan: numeric Range: 0 Ch to 39 Ch
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:DTMode?')
		return Conversions.str_to_int(response)

	def set_dt_mode(self, rx_tx_chan: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:DTMode \n
		Snippet: driver.configure.rfSettings.channel.set_dt_mode(rx_tx_chan = 1) \n
		Configures the channel number for direct test mode. \n
			:param rx_tx_chan: numeric Range: 0 Ch to 39 Ch
		"""
		param = Conversions.decimal_value_to_str(rx_tx_chan)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:DTMode {param}')

	# noinspection PyTypeChecker
	class LoopbackStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rx_Chan: int: numeric Range: 0 Ch to 78 Ch
			- Tx_Chan: int: numeric Range: 0 Ch to 78 Ch"""
		__meta_args_list = [
			ArgStruct.scalar_int('Rx_Chan'),
			ArgStruct.scalar_int('Tx_Chan')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rx_Chan: int = None
			self.Tx_Chan: int = None

	def get_loopback(self) -> LoopbackStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:LOOPback \n
		Snippet: value: LoopbackStruct = driver.configure.rfSettings.channel.get_loopback() \n
		Defines the channels used by the loopback test. \n
			:return: structure: for return value, see the help for LoopbackStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:LOOPback?', self.__class__.LoopbackStruct())

	def set_loopback(self, value: LoopbackStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:LOOPback \n
		Snippet: driver.configure.rfSettings.channel.set_loopback(value = LoopbackStruct()) \n
		Defines the channels used by the loopback test. \n
			:param value: see the help for LoopbackStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:LOOPback', value)

	def get_tx_test(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TXTest \n
		Snippet: value: int = driver.configure.rfSettings.channel.get_tx_test() \n
		Defines the channels used by the TX test. \n
			:return: rx_tx_chan: numeric Range: 0 Ch to 78 Ch
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TXTest?')
		return Conversions.str_to_int(response)

	def set_tx_test(self, rx_tx_chan: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TXTest \n
		Snippet: driver.configure.rfSettings.channel.set_tx_test(rx_tx_chan = 1) \n
		Defines the channels used by the TX test. \n
			:param rx_tx_chan: numeric Range: 0 Ch to 78 Ch
		"""
		param = Conversions.decimal_value_to_str(rx_tx_chan)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TXTest {param}')
