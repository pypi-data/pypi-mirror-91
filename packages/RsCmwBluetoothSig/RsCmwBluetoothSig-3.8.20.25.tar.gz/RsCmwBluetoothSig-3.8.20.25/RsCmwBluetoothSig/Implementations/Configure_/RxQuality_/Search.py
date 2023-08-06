from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Search:
	"""Search commands group definition. 35 total commands, 4 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("search", core, parent)

	@property
	def rintegrity(self):
		"""rintegrity commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rintegrity'):
			from .Search_.Rintegrity import Rintegrity
			self._rintegrity = Rintegrity(self._core, self._base)
		return self._rintegrity

	@property
	def limit(self):
		"""limit commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Search_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	@property
	def packets(self):
		"""packets commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_packets'):
			from .Search_.Packets import Packets
			self._packets = Packets(self._core, self._base)
		return self._packets

	@property
	def step(self):
		"""step commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Search_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:TOUT \n
		Snippet: value: float = driver.configure.rxQuality.search.get_timeout() \n
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
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, timeout: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:TOUT \n
		Snippet: driver.configure.rxQuality.search.set_timeout(timeout = 1.0) \n
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
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:TOUT {param}')

	def clone(self) -> 'Search':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Search(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
