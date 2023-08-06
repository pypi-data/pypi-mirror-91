from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	def read(self, start: float = None, count: float = None, decimation: float = None, segment=repcap.Segment.Default) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness:SEGMent<seg>:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.spectrFlatness.segment.maximum.read(start = 1.0, count = 1.0, decimation = 1.0, segment = repcap.Segment.Default) \n
		Return the spectrum flatness traces for segment <seg>, for SISO measurements and bandwidths with two segments (80+80 MHz)
		. The results of the current, average, minimum and maximum traces can be retrieved. The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param count: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param decimation: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: spec_flat_trace_segment_max: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness:SEGMent{segment_cmd_val}:MAXimum? {param}'.rstrip(), suppressed)
		return response

	def fetch(self, start: float = None, count: float = None, decimation: float = None, segment=repcap.Segment.Default) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness:SEGMent<seg>:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.spectrFlatness.segment.maximum.fetch(start = 1.0, count = 1.0, decimation = 1.0, segment = repcap.Segment.Default) \n
		Return the spectrum flatness traces for segment <seg>, for SISO measurements and bandwidths with two segments (80+80 MHz)
		. The results of the current, average, minimum and maximum traces can be retrieved. The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param count: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param decimation: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: spec_flat_trace_segment_max: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness:SEGMent{segment_cmd_val}:MAXimum? {param}'.rstrip(), suppressed)
		return response

	# noinspection PyTypeChecker
	def calculate(self, start: float = None, count: float = None, decimation: float = None, segment=repcap.Segment.Default) -> List[enums.ResultStatus2]:
		"""SCPI: CALCulate:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness:SEGMent<seg>:MAXimum \n
		Snippet: value: List[enums.ResultStatus2] = driver.multiEval.trace.spectrFlatness.segment.maximum.calculate(start = 1.0, count = 1.0, decimation = 1.0, segment = repcap.Segment.Default) \n
		Return the spectrum flatness traces for segment <seg>, for SISO measurements and bandwidths with two segments (80+80 MHz)
		. The results of the current, average, minimum and maximum traces can be retrieved. The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param count: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param decimation: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: spec_flat_trace_segment_max: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:WLAN:MEASurement<Instance>:MEValuation:TRACe:SFLatness:SEGMent{segment_cmd_val}:MAXimum? {param}'.rstrip(), suppressed)
		return Conversions.str_to_list_enum(response, enums.ResultStatus2)
