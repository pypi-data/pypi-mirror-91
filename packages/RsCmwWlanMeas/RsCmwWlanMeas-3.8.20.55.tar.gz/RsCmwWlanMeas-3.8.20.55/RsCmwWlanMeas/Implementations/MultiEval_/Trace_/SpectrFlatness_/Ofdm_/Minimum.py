from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Minimum:
	"""Minimum commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("minimum", core, parent)

	def read(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness[:OFDM]:MINimum \n
		Snippet: value: List[float] = driver.multiEval.trace.spectrFlatness.ofdm.minimum.read(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the values of the spectrum flatness traces for OFDM SISO signals according to standard 802.11a, g, n, ac, ax, or p.
		The results of the current, average, minimum and maximum traces can be retrieved. For the optional query parameters
		<start>, <count> and <decimation>, see 'Trace Sub-Arrays'. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: sflat_min: float Comma-separated list of 2n+1 power values, for subcarrier -n to subcarrier +n (including data, pilot and unused subcarriers) n depends on the WLAN standard, channel bandwidth and mode, see Table 'OFDM subcarriers'. Range: -20 dB to 20 dB"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness:OFDM:MINimum? {param}'.rstrip(), suppressed)
		return response

	def fetch(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness[:OFDM]:MINimum \n
		Snippet: value: List[float] = driver.multiEval.trace.spectrFlatness.ofdm.minimum.fetch(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the values of the spectrum flatness traces for OFDM SISO signals according to standard 802.11a, g, n, ac, ax, or p.
		The results of the current, average, minimum and maximum traces can be retrieved. For the optional query parameters
		<start>, <count> and <decimation>, see 'Trace Sub-Arrays'. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: sflat_min: float Comma-separated list of 2n+1 power values, for subcarrier -n to subcarrier +n (including data, pilot and unused subcarriers) n depends on the WLAN standard, channel bandwidth and mode, see Table 'OFDM subcarriers'. Range: -20 dB to 20 dB"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness:OFDM:MINimum? {param}'.rstrip(), suppressed)
		return response
