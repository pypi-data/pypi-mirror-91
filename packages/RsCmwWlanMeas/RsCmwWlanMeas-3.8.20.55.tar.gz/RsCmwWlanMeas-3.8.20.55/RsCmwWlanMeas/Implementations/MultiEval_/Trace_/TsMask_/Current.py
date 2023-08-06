from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def read(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:CURRent \n
		Snippet: value: List[float] = driver.multiEval.trace.tsMask.current.read(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the values of the transmit spectrum mask traces for SISO measurements and bandwidths with one segment. The results
		of the current, average, minimum and maximum traces can be retrieved. For the optional query parameters <start>, <count>
		and <decimation>, see 'Trace Sub-Arrays'. For 802.11p signals, use method RsCmwWlanMeas.Configure.MultiEval.TsMask.
		mselection to switch between relative and absolute values. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: spectrum_trace: float Comma-separated list of power values, trace from left to right Range: -90 dB to 10 dB (relative) or -120 dBm to 25 dBm (absolute) , Unit: dB (relative) or dBm (absolute)"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:CURRent? {param}'.rstrip(), suppressed)
		return response

	def fetch(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:CURRent \n
		Snippet: value: List[float] = driver.multiEval.trace.tsMask.current.fetch(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the values of the transmit spectrum mask traces for SISO measurements and bandwidths with one segment. The results
		of the current, average, minimum and maximum traces can be retrieved. For the optional query parameters <start>, <count>
		and <decimation>, see 'Trace Sub-Arrays'. For 802.11p signals, use method RsCmwWlanMeas.Configure.MultiEval.TsMask.
		mselection to switch between relative and absolute values. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: spectrum_trace: float Comma-separated list of power values, trace from left to right Range: -90 dB to 10 dB (relative) or -120 dBm to 25 dBm (absolute) , Unit: dB (relative) or dBm (absolute)"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:CURRent? {param}'.rstrip(), suppressed)
		return response
