from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def read(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:FREQuency \n
		Snippet: value: List[float] = driver.multiEval.trace.tsMask.frequency.read(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the frequency values (X-values) of the transmit spectrum mask limit line trace, for SISO and MIMO, bandwidths with
		one or two segments. For the optional query parameters <start>, <count> and <decimation>, see 'Trace Sub-Arrays'. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: spec_trace_freq: float Comma-separated list of values, trace from left to right 0 Hz corresponds to the center of the channel, for 80+80 MHz signals to the center of the left segment. Unit: Hz"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:FREQuency? {param}'.rstrip(), suppressed)
		return response

	def fetch(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:FREQuency \n
		Snippet: value: List[float] = driver.multiEval.trace.tsMask.frequency.fetch(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the frequency values (X-values) of the transmit spectrum mask limit line trace, for SISO and MIMO, bandwidths with
		one or two segments. For the optional query parameters <start>, <count> and <decimation>, see 'Trace Sub-Arrays'. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: spec_trace_freq: float Comma-separated list of values, trace from left to right 0 Hz corresponds to the center of the channel, for 80+80 MHz signals to the center of the left segment. Unit: Hz"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:FREQuency? {param}'.rstrip(), suppressed)
		return response
