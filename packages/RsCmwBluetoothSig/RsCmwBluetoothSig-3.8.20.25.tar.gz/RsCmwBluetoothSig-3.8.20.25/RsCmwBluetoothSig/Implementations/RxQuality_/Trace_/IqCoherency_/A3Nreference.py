from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A3Nreference:
	"""A3Nreference commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("a3Nreference", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:TRACe:IQCoherency:A3NReference \n
		Snippet: value: List[float] = driver.rxQuality.trace.iqCoherency.a3Nreference.read() \n
		Return the trace results of relative phase values RP(m) for IQ samples coherency Rx measurements. Commands for mandatory
		second (non-reference) antenna (...:A1NReference) , and optional third and fourth non-reference antennas are available. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: mrp: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:TRACe:IQCoherency:A3NReference?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:TRACe:IQCoherency:A3NReference \n
		Snippet: value: List[float] = driver.rxQuality.trace.iqCoherency.a3Nreference.fetch() \n
		Return the trace results of relative phase values RP(m) for IQ samples coherency Rx measurements. Commands for mandatory
		second (non-reference) antenna (...:A1NReference) , and optional third and fourth non-reference antennas are available. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: mrp: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:TRACe:IQCoherency:A3NReference?', suppressed)
		return response
