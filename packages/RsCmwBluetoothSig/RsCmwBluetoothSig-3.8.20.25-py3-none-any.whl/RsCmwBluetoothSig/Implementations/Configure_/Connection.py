from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Connection:
	"""Connection commands group definition. 92 total commands, 24 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("connection", core, parent)

	@property
	def audio(self):
		"""audio commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_audio'):
			from .Connection_.Audio import Audio
			self._audio = Audio(self._core, self._base)
		return self._audio

	@property
	def packets(self):
		"""packets commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_packets'):
			from .Connection_.Packets import Packets
			self._packets = Packets(self._core, self._base)
		return self._packets

	@property
	def synWord(self):
		"""synWord commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_synWord'):
			from .Connection_.SynWord import SynWord
			self._synWord = SynWord(self._core, self._base)
		return self._synWord

	@property
	def cscheme(self):
		"""cscheme commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cscheme'):
			from .Connection_.Cscheme import Cscheme
			self._cscheme = Cscheme(self._core, self._base)
		return self._cscheme

	@property
	def fec(self):
		"""fec commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fec'):
			from .Connection_.Fec import Fec
			self._fec = Fec(self._core, self._base)
		return self._fec

	@property
	def phy(self):
		"""phy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_phy'):
			from .Connection_.Phy import Phy
			self._phy = Phy(self._core, self._base)
		return self._phy

	@property
	def powerControl(self):
		"""powerControl commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_powerControl'):
			from .Connection_.PowerControl import PowerControl
			self._powerControl = PowerControl(self._core, self._base)
		return self._powerControl

	@property
	def paging(self):
		"""paging commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_paging'):
			from .Connection_.Paging import Paging
			self._paging = Paging(self._core, self._base)
		return self._paging

	@property
	def bdAddress(self):
		"""bdAddress commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bdAddress'):
			from .Connection_.BdAddress import BdAddress
			self._bdAddress = BdAddress(self._core, self._base)
		return self._bdAddress

	@property
	def inquiry(self):
		"""inquiry commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_inquiry'):
			from .Connection_.Inquiry import Inquiry
			self._inquiry = Inquiry(self._core, self._base)
		return self._inquiry

	@property
	def eutCharacter(self):
		"""eutCharacter commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_eutCharacter'):
			from .Connection_.EutCharacter import EutCharacter
			self._eutCharacter = EutCharacter(self._core, self._base)
		return self._eutCharacter

	@property
	def wfcMap(self):
		"""wfcMap commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_wfcMap'):
			from .Connection_.WfcMap import WfcMap
			self._wfcMap = WfcMap(self._core, self._base)
		return self._wfcMap

	@property
	def slatency(self):
		"""slatency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_slatency'):
			from .Connection_.Slatency import Slatency
			self._slatency = Slatency(self._core, self._base)
		return self._slatency

	@property
	def rencryption(self):
		"""rencryption commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rencryption'):
			from .Connection_.Rencryption import Rencryption
			self._rencryption = Rencryption(self._core, self._base)
		return self._rencryption

	@property
	def iencryption(self):
		"""iencryption commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iencryption'):
			from .Connection_.Iencryption import Iencryption
			self._iencryption = Iencryption(self._core, self._base)
		return self._iencryption

	@property
	def cmw(self):
		"""cmw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmw'):
			from .Connection_.Cmw import Cmw
			self._cmw = Cmw(self._core, self._base)
		return self._cmw

	@property
	def address(self):
		"""address commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_address'):
			from .Connection_.Address import Address
			self._address = Address(self._core, self._base)
		return self._address

	@property
	def raddress(self):
		"""raddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_raddress'):
			from .Connection_.Raddress import Raddress
			self._raddress = Raddress(self._core, self._base)
		return self._raddress

	@property
	def svTimeout(self):
		"""svTimeout commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_svTimeout'):
			from .Connection_.SvTimeout import SvTimeout
			self._svTimeout = SvTimeout(self._core, self._base)
		return self._svTimeout

	@property
	def interval(self):
		"""interval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interval'):
			from .Connection_.Interval import Interval
			self._interval = Interval(self._core, self._base)
		return self._interval

	@property
	def sinterval(self):
		"""sinterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinterval'):
			from .Connection_.Sinterval import Sinterval
			self._sinterval = Sinterval(self._core, self._base)
		return self._sinterval

	@property
	def ainterval(self):
		"""ainterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ainterval'):
			from .Connection_.Ainterval import Ainterval
			self._ainterval = Ainterval(self._core, self._base)
		return self._ainterval

	@property
	def swindow(self):
		"""swindow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swindow'):
			from .Connection_.Swindow import Swindow
			self._swindow = Swindow(self._core, self._base)
		return self._swindow

	@property
	def pperiod(self):
		"""pperiod commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pperiod'):
			from .Connection_.Pperiod import Pperiod
			self._pperiod = Pperiod(self._core, self._base)
		return self._pperiod

	# noinspection PyTypeChecker
	def get_btype(self) -> enums.BurstType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BTYPe \n
		Snippet: value: enums.BurstType = driver.configure.connection.get_btype() \n
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- BR/EDR in test mode
			- LE in direct test mode \n
			:return: burst_type: BR | EDR | LE BR: 'Basic Rate' EDR: 'Enhanced Data Rate' LE: 'Low Energy'
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BurstType)

	def set_btype(self, burst_type: enums.BurstType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BTYPe \n
		Snippet: driver.configure.connection.set_btype(burst_type = enums.BurstType.BR) \n
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- BR/EDR in test mode
			- LE in direct test mode \n
			:param burst_type: BR | EDR | LE BR: 'Basic Rate' EDR: 'Enhanced Data Rate' LE: 'Low Energy'
		"""
		param = Conversions.enum_scalar_to_str(burst_type, enums.BurstType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BTYPe {param}')

	def get_delay(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:DELay \n
		Snippet: value: bool = driver.configure.connection.get_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:DELay?')
		return Conversions.str_to_bool(response)

	def set_delay(self, delay: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:DELay \n
		Snippet: driver.configure.connection.set_delay(delay = False) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.bool_to_str(delay)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:DELay {param}')

	def get_whitening(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WHITening \n
		Snippet: value: bool = driver.configure.connection.get_whitening() \n
		Sets whether the EUT has to transmit ACL packets scrambled with a particular data sequence in a loopback mode. \n
			:return: whitening: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WHITening?')
		return Conversions.str_to_bool(response)

	def set_whitening(self, whitening: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WHITening \n
		Snippet: driver.configure.connection.set_whitening(whitening = False) \n
		Sets whether the EUT has to transmit ACL packets scrambled with a particular data sequence in a loopback mode. \n
			:param whitening: OFF | ON
		"""
		param = Conversions.bool_to_str(whitening)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WHITening {param}')

	def clone(self) -> 'Connection':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Connection(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
