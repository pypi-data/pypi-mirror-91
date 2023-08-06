from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PacketLength:
	"""PacketLength commands group definition. 5 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("packetLength", core, parent)

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .PacketLength_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	def get_brate(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:BRATe \n
		Snippet: value: List[int] = driver.configure.connection.packets.packetLength.get_brate() \n
		Sets the payload length for BR test mode. \n
			:return: payload_length: numeric Range: Three values, see table below
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:BRATe?')
		return response

	def set_brate(self, payload_length: List[int]) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:BRATe \n
		Snippet: driver.configure.connection.packets.packetLength.set_brate(payload_length = [1, 2, 3]) \n
		Sets the payload length for BR test mode. \n
			:param payload_length: numeric Range: Three values, see table below
		"""
		param = Conversions.list_to_csv_str(payload_length)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:BRATe {param}')

	def get_edrate(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:EDRate \n
		Snippet: value: List[int] = driver.configure.connection.packets.packetLength.get_edrate() \n
		Sets the payload length for EDR test mode. \n
			:return: payload_length: numeric Range: Six values, see table below
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:EDRate?')
		return response

	def set_edrate(self, payload_length: List[int]) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:EDRate \n
		Snippet: driver.configure.connection.packets.packetLength.set_edrate(payload_length = [1, 2, 3]) \n
		Sets the payload length for EDR test mode. \n
			:param payload_length: numeric Range: Six values, see table below
		"""
		param = Conversions.list_to_csv_str(payload_length)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:EDRate {param}')

	def clone(self) -> 'PacketLength':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PacketLength(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
