from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxQuality:
	"""RxQuality commands group definition. 113 total commands, 10 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxQuality", core, parent)

	@property
	def smIndex(self):
		"""smIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smIndex'):
			from .RxQuality_.SmIndex import SmIndex
			self._smIndex = SmIndex(self._core, self._base)
		return self._smIndex

	@property
	def search(self):
		"""search commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_search'):
			from .RxQuality_.Search import Search
			self._search = Search(self._core, self._base)
		return self._search

	@property
	def packets(self):
		"""packets commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_packets'):
			from .RxQuality_.Packets import Packets
			self._packets = Packets(self._core, self._base)
		return self._packets

	@property
	def rintegrity(self):
		"""rintegrity commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rintegrity'):
			from .RxQuality_.Rintegrity import Rintegrity
			self._rintegrity = Rintegrity(self._core, self._base)
		return self._rintegrity

	@property
	def limit(self):
		"""limit commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .RxQuality_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	@property
	def ibLength(self):
		"""ibLength commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ibLength'):
			from .RxQuality_.IbLength import IbLength
			self._ibLength = IbLength(self._core, self._base)
		return self._ibLength

	@property
	def iqCoherency(self):
		"""iqCoherency commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqCoherency'):
			from .RxQuality_.IqCoherency import IqCoherency
			self._iqCoherency = IqCoherency(self._core, self._base)
		return self._iqCoherency

	@property
	def iqDrange(self):
		"""iqDrange commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqDrange'):
			from .RxQuality_.IqDrange import IqDrange
			self._iqDrange = IqDrange(self._core, self._base)
		return self._iqDrange

	@property
	def itend(self):
		"""itend commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_itend'):
			from .RxQuality_.Itend import Itend
			self._itend = Itend(self._core, self._base)
		return self._itend

	@property
	def cbits(self):
		"""cbits commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cbits'):
			from .RxQuality_.Cbits import Cbits
			self._cbits = Cbits(self._core, self._base)
		return self._cbits

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.rxQuality.get_repetition() \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single-shot or repeated continuously. Use CONFigure:BLUetooth:SIGN<i>:RXQuality or method RsCmwBluetoothSig.Configure.
		RxQuality.Packets.bedr to determine the number of transport blocks per single shot. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot: single-shot measurement CONTinuous: continuous measurement
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:REPetition \n
		Snippet: driver.configure.rxQuality.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single-shot or repeated continuously. Use CONFigure:BLUetooth:SIGN<i>:RXQuality or method RsCmwBluetoothSig.Configure.
		RxQuality.Packets.bedr to determine the number of transport blocks per single shot. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot: single-shot measurement CONTinuous: continuous measurement
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:REPetition {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:TOUT \n
		Snippet: value: float = driver.configure.rxQuality.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually ([ON | OFF] key or [RESTART | STOP] key) .
		When the measurement has completed the first measurement cycle (first single shot) , the statistical depth is reached and
		the timer is reset. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped. The measurement state changes to RDY. The reliability indicator is set to 1, indicating that a measurement
		timeout occurred. Still running READ, FETCh or CALCulate commands are completed, returning the available results.
		At least for some results, there are no values at all or the statistical depth has not been reached. A timeout of 0 s
		corresponds to an infinite measurement timeout. \n
			:return: timeout: numeric Unit: s
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, timeout: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:TOUT \n
		Snippet: driver.configure.rxQuality.set_timeout(timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually ([ON | OFF] key or [RESTART | STOP] key) .
		When the measurement has completed the first measurement cycle (first single shot) , the statistical depth is reached and
		the timer is reset. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped. The measurement state changes to RDY. The reliability indicator is set to 1, indicating that a measurement
		timeout occurred. Still running READ, FETCh or CALCulate commands are completed, returning the available results.
		At least for some results, there are no values at all or the statistical depth has not been reached. A timeout of 0 s
		corresponds to an infinite measurement timeout. \n
			:param timeout: numeric Unit: s
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:TOUT {param}')

	def get_scondition(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SCONdition \n
		Snippet: value: int = driver.configure.rxQuality.get_scondition() \n
		No command help available \n
			:return: condition: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SCONdition?')
		return Conversions.str_to_int(response)

	def set_scondition(self, condition: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SCONdition \n
		Snippet: driver.configure.rxQuality.set_scondition(condition = 1) \n
		No command help available \n
			:param condition: No help available
		"""
		param = Conversions.decimal_value_to_str(condition)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SCONdition {param}')

	def get_iqsdump(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQSDump \n
		Snippet: value: bool = driver.configure.rxQuality.get_iqsdump() \n
		Enables or disables dumping of the Rx IQ events received from the EUT via HCI. \n
			:return: dump_iq_pairs: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQSDump?')
		return Conversions.str_to_bool(response)

	def set_iqsdump(self, dump_iq_pairs: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQSDump \n
		Snippet: driver.configure.rxQuality.set_iqsdump(dump_iq_pairs = False) \n
		Enables or disables dumping of the Rx IQ events received from the EUT via HCI. \n
			:param dump_iq_pairs: OFF | ON
		"""
		param = Conversions.bool_to_str(dump_iq_pairs)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQSDump {param}')

	def clone(self) -> 'RxQuality':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxQuality(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
