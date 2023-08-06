from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Paging:
	"""Paging commands group definition. 5 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("paging", core, parent)

	@property
	def timeout(self):
		"""timeout commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_timeout'):
			from .Paging_.Timeout import Timeout
			self._timeout = Timeout(self._core, self._base)
		return self._timeout

	@property
	def ptarget(self):
		"""ptarget commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ptarget'):
			from .Paging_.Ptarget import Ptarget
			self._ptarget = Ptarget(self._core, self._base)
		return self._ptarget

	# noinspection PyTypeChecker
	def get_psr_mode(self) -> enums.PsrMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PSRMode \n
		Snippet: value: enums.PsrMode = driver.configure.connection.paging.get_psr_mode() \n
		Sets/gets the page scan repetition mode to be used for the default device (see method RsCmwBluetoothSig.Configure.
		Connection.BdAddress.eut) . \n
			:return: psr_mode: R0 | R1 | R2 Paging mode R0, R1, R2. Select the value according to the page scan repetition mode of the default device.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PSRMode?')
		return Conversions.str_to_scalar_enum(response, enums.PsrMode)

	def set_psr_mode(self, psr_mode: enums.PsrMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PSRMode \n
		Snippet: driver.configure.connection.paging.set_psr_mode(psr_mode = enums.PsrMode.R0) \n
		Sets/gets the page scan repetition mode to be used for the default device (see method RsCmwBluetoothSig.Configure.
		Connection.BdAddress.eut) . \n
			:param psr_mode: R0 | R1 | R2 Paging mode R0, R1, R2. Select the value according to the page scan repetition mode of the default device.
		"""
		param = Conversions.enum_scalar_to_str(psr_mode, enums.PsrMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PSRMode {param}')

	def clone(self) -> 'Paging':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Paging(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
