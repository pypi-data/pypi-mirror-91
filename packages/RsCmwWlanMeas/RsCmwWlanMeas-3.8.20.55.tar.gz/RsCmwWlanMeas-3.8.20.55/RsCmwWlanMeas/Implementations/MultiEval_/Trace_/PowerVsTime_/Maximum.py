from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	def read(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:PVTime:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.powerVsTime.maximum.read(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the values of the power vs. time traces for SISO connections. The results of the current, average, maximum and
		minimum traces can be retrieved. For the optional query parameters <start>, <count> and <decimation>, see 'Trace
		Sub-Arrays'. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: power_max: float Comma-separated list of max 1024 time values (1024 values without subarrays) Range: -100 dBm to 30 dBm, Unit: dBm"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:PVTime:MAXimum? {param}'.rstrip(), suppressed)
		return response

	def fetch(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:PVTime:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.powerVsTime.maximum.fetch(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the values of the power vs. time traces for SISO connections. The results of the current, average, maximum and
		minimum traces can be retrieved. For the optional query parameters <start>, <count> and <decimation>, see 'Trace
		Sub-Arrays'. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: power_max: float Comma-separated list of max 1024 time values (1024 values without subarrays) Range: -100 dBm to 30 dBm, Unit: dBm"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:PVTime:MAXimum? {param}'.rstrip(), suppressed)
		return response
