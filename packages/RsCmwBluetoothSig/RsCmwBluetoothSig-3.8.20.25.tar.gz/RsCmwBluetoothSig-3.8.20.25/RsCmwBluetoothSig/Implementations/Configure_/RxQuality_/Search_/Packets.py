from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Packets:
	"""Packets commands group definition. 10 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("packets", core, parent)

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Packets_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	@property
	def tmode(self):
		"""tmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmode'):
			from .Packets_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	@property
	def nmode(self):
		"""nmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmode'):
			from .Packets_.Nmode import Nmode
			self._nmode = Nmode(self._core, self._base)
		return self._nmode

	def get_bedr(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PACKets[:BEDR] \n
		Snippet: value: int = driver.configure.rxQuality.search.packets.get_bedr() \n
		Defines the number of data packets to be measured per measurement cycle (statistics cycle) . \n
			:return: number_packets: numeric Range: 1 to 400E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PACKets:BEDR?')
		return Conversions.str_to_int(response)

	def set_bedr(self, number_packets: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PACKets[:BEDR] \n
		Snippet: driver.configure.rxQuality.search.packets.set_bedr(number_packets = 1) \n
		Defines the number of data packets to be measured per measurement cycle (statistics cycle) . \n
			:param number_packets: numeric Range: 1 to 400E+3
		"""
		param = Conversions.decimal_value_to_str(number_packets)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PACKets:BEDR {param}')

	def clone(self) -> 'Packets':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Packets(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
