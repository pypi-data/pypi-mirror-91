from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Inquiry:
	"""Inquiry commands group definition. 8 total commands, 5 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inquiry", core, parent)

	@property
	def ptargets(self):
		"""ptargets commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptargets'):
			from .Inquiry_.Ptargets import Ptargets
			self._ptargets = Ptargets(self._core, self._base)
		return self._ptargets

	@property
	def noResponses(self):
		"""noResponses commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_noResponses'):
			from .Inquiry_.NoResponses import NoResponses
			self._noResponses = NoResponses(self._core, self._base)
		return self._noResponses

	@property
	def sinterval(self):
		"""sinterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinterval'):
			from .Inquiry_.Sinterval import Sinterval
			self._sinterval = Sinterval(self._core, self._base)
		return self._sinterval

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Inquiry_.Duration import Duration
			self._duration = Duration(self._core, self._base)
		return self._duration

	@property
	def swindow(self):
		"""swindow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swindow'):
			from .Inquiry_.Swindow import Swindow
			self._swindow = Swindow(self._core, self._base)
		return self._swindow

	def get_ilength(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:ILENgth \n
		Snippet: value: int = driver.configure.connection.inquiry.get_ilength() \n
		Sets/gets the Inquiry_Length parameter, i.e. the total duration of the inquiry mode. \n
			:return: inquiry_length: numeric The inquiry length in units of 1.28 s Range: 1 to 24, Unit: 1.28 s
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:ILENgth?')
		return Conversions.str_to_int(response)

	def set_ilength(self, inquiry_length: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:ILENgth \n
		Snippet: driver.configure.connection.inquiry.set_ilength(inquiry_length = 1) \n
		Sets/gets the Inquiry_Length parameter, i.e. the total duration of the inquiry mode. \n
			:param inquiry_length: numeric The inquiry length in units of 1.28 s Range: 1 to 24, Unit: 1.28 s
		"""
		param = Conversions.decimal_value_to_str(inquiry_length)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:ILENgth {param}')

	def clone(self) -> 'Inquiry':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Inquiry(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
