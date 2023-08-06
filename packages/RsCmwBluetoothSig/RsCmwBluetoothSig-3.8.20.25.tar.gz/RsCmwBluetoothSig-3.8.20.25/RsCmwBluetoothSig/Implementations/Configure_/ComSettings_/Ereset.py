from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ereset:
	"""Ereset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ereset", core, parent)

	def set(self, eut_reset: bool, commSettings=repcap.CommSettings.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:ERESet \n
		Snippet: driver.configure.comSettings.ereset.set(eut_reset = False, commSettings = repcap.CommSettings.Default) \n
		Commands to reset the EUT before starting tests. \n
			:param eut_reset: ON | OFF
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')"""
		param = Conversions.bool_to_str(eut_reset)
		commSettings_cmd_val = self._base.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:ERESet {param}')

	def get(self, commSettings=repcap.CommSettings.Default) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:ERESet \n
		Snippet: value: bool = driver.configure.comSettings.ereset.get(commSettings = repcap.CommSettings.Default) \n
		Commands to reset the EUT before starting tests. \n
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
			:return: eut_reset: ON | OFF"""
		commSettings_cmd_val = self._base.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:ERESet?')
		return Conversions.str_to_bool(response)
