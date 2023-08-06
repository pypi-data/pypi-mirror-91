from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	def get_lrange(self) -> List[float or bool]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:STANdard:TMODe:LENergy:LRANge \n
		Snippet: value: List[float or bool] = driver.configure.rfSettings.dtx.stab.mindex.standard.tmode.lowEnergy.get_lrange() \n
		Return the modulation index under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for BR (..:BRATe..) , LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless
		technology, see also 'Dirty Tx Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: mod_index: float | ON | OFF Range: 0.2 to 0.55
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:STANdard:TMODe:LENergy:LRANge?')
		return Conversions.str_to_float_or_bool_list(response)

	def get_le_2_m(self) -> List[float or bool]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:STANdard:TMODe:LENergy:LE2M \n
		Snippet: value: List[float or bool] = driver.configure.rfSettings.dtx.stab.mindex.standard.tmode.lowEnergy.get_le_2_m() \n
		Return the modulation index under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for BR (..:BRATe..) , LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless
		technology, see also 'Dirty Tx Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: mod_index: float | ON | OFF Range: 0.2 to 0.55
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:STANdard:TMODe:LENergy:LE2M?')
		return Conversions.str_to_float_or_bool_list(response)

	def get_le_1_m(self) -> List[float or bool]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:STANdard:TMODe:LENergy:LE1M \n
		Snippet: value: List[float or bool] = driver.configure.rfSettings.dtx.stab.mindex.standard.tmode.lowEnergy.get_le_1_m() \n
		Return the modulation index under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for BR (..:BRATe..) , LE 1M PHY - uncoded (..:LE1M..) , LE 2M PHY - uncoded (..:LE2M..) , and LE coded PHY (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless
		technology, see also 'Dirty Tx Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: mod_index: float | ON | OFF Range: 0.2 to 0.55
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:STANdard:TMODe:LENergy:LE1M?')
		return Conversions.str_to_float_or_bool_list(response)
