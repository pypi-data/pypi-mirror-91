from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 396 total commands, 12 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_delay'):
			from .Configure_.Delay import Delay
			self._delay = Delay(self._core, self._base)
		return self._delay

	@property
	def tmode(self):
		"""tmode commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tmode'):
			from .Configure_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	@property
	def audio(self):
		"""audio commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_audio'):
			from .Configure_.Audio import Audio
			self._audio = Audio(self._core, self._base)
		return self._audio

	@property
	def connection(self):
		"""connection commands group. 24 Sub-classes, 3 commands."""
		if not hasattr(self, '_connection'):
			from .Configure_.Connection import Connection
			self._connection = Connection(self._core, self._base)
		return self._connection

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Configure_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	@property
	def usbSettings(self):
		"""usbSettings commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_usbSettings'):
			from .Configure_.UsbSettings import UsbSettings
			self._usbSettings = UsbSettings(self._core, self._base)
		return self._usbSettings

	@property
	def comSettings(self):
		"""comSettings commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_comSettings'):
			from .Configure_.ComSettings import ComSettings
			self._comSettings = ComSettings(self._core, self._base)
		return self._comSettings

	@property
	def hwInterface(self):
		"""hwInterface commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hwInterface'):
			from .Configure_.HwInterface import HwInterface
			self._hwInterface = HwInterface(self._core, self._base)
		return self._hwInterface

	@property
	def debug(self):
		"""debug commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_debug'):
			from .Configure_.Debug import Debug
			self._debug = Debug(self._core, self._base)
		return self._debug

	@property
	def tconnection(self):
		"""tconnection commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_tconnection'):
			from .Configure_.Tconnection import Tconnection
			self._tconnection = Tconnection(self._core, self._base)
		return self._tconnection

	@property
	def rfSettings(self):
		"""rfSettings commands group. 10 Sub-classes, 7 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Configure_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def rxQuality(self):
		"""rxQuality commands group. 10 Sub-classes, 4 commands."""
		if not hasattr(self, '_rxQuality'):
			from .Configure_.RxQuality import RxQuality
			self._rxQuality = RxQuality(self._core, self._base)
		return self._rxQuality

	# noinspection PyTypeChecker
	def get_op_mode(self) -> enums.OperatingMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:OPMode \n
		Snippet: value: enums.OperatingMode = driver.configure.get_op_mode() \n
		Specifies operating mode of R&S CMW. \n
			:return: operating_mode: CNTest | RFTest | ECMode | PROFiles | AUDio | LETMode CNTest: connection test for BR/EDR or LE (OTA) RFTest: test mode for BR/EDR or direct test for LE ECMode: echo mode for BR/EDR PROFiles: profiles for BR/EDR AUDio: audio mode for BR/EDR LETMode: LE test mode (OTA)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:OPMode?')
		return Conversions.str_to_scalar_enum(response, enums.OperatingMode)

	def set_op_mode(self, operating_mode: enums.OperatingMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:OPMode \n
		Snippet: driver.configure.set_op_mode(operating_mode = enums.OperatingMode.AUDio) \n
		Specifies operating mode of R&S CMW. \n
			:param operating_mode: CNTest | RFTest | ECMode | PROFiles | AUDio | LETMode CNTest: connection test for BR/EDR or LE (OTA) RFTest: test mode for BR/EDR or direct test for LE ECMode: echo mode for BR/EDR PROFiles: profiles for BR/EDR AUDio: audio mode for BR/EDR LETMode: LE test mode (OTA)
		"""
		param = Conversions.enum_scalar_to_str(operating_mode, enums.OperatingMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:OPMode {param}')

	# noinspection PyTypeChecker
	def get_cprotocol(self) -> enums.CommProtocol:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CPRotocol \n
		Snippet: value: enums.CommProtocol = driver.configure.get_cprotocol() \n
		Specifies the communication protocol for direct test mode. \n
			:return: communication_protocol: HCI | TWO HCI or two-wire UART interface
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CPRotocol?')
		return Conversions.str_to_scalar_enum(response, enums.CommProtocol)

	def set_cprotocol(self, communication_protocol: enums.CommProtocol) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CPRotocol \n
		Snippet: driver.configure.set_cprotocol(communication_protocol = enums.CommProtocol.HCI) \n
		Specifies the communication protocol for direct test mode. \n
			:param communication_protocol: HCI | TWO HCI or two-wire UART interface
		"""
		param = Conversions.enum_scalar_to_str(communication_protocol, enums.CommProtocol)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CPRotocol {param}')

	# noinspection PyTypeChecker
	def get_standard(self) -> enums.SignalingStandard:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:STANdard \n
		Snippet: value: enums.SignalingStandard = driver.configure.get_standard() \n
		Selects classic (BR/EDR) or low energy (LE) bursts. \n
			:return: sig_std: CLASsic | LESignaling
		"""
		response = self._core.io.query_str_with_opc('CONFigure:BLUetooth:SIGNaling<Instance>:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.SignalingStandard)

	def set_standard(self, sig_std: enums.SignalingStandard) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:STANdard \n
		Snippet: driver.configure.set_standard(sig_std = enums.SignalingStandard.CLASsic) \n
		Selects classic (BR/EDR) or low energy (LE) bursts. \n
			:param sig_std: CLASsic | LESignaling
		"""
		param = Conversions.enum_scalar_to_str(sig_std, enums.SignalingStandard)
		self._core.io.write_with_opc(f'CONFigure:BLUetooth:SIGNaling<Instance>:STANdard {param}')

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
