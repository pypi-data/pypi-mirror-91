from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	def read(self, start: float = None, count: float = None, decimation: float = None, mimo=repcap.Mimo.Default, segment=repcap.Segment.Default) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:PVTime:FEDGe:MIMO<n>:SEGMent<seg>:TIME \n
		Snippet: value: List[float] = driver.multiEval.trace.powerVsTime.fallingEdge.mimo.segment.time.read(start = 1.0, count = 1.0, decimation = 1.0, mimo = repcap.Mimo.Default, segment = repcap.Segment.Default) \n
		Return the time indices for the power vs. time ramp traces (for 80+80 MHz, MIMO) , rising edge (REDGe) and falling edge
		(FEDGe) . Refer to method RsCmwWlanMeas.MultiEval.Trace.PowerVsTime.RisingEdge.Mimo.Segment.Current.fetch \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param count: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param decimation: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param mimo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mimo')
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: time_values: float Comma-separated list of time indices corresponding to the ramp power results. Unit: s"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		mimo_cmd_val = self._base.get_repcap_cmd_value(mimo, repcap.Mimo)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:PVTime:FEDGe:MIMO{mimo_cmd_val}:SEGMent{segment_cmd_val}:TIME? {param}'.rstrip(), suppressed)
		return response

	def fetch(self, start: float = None, count: float = None, decimation: float = None, mimo=repcap.Mimo.Default, segment=repcap.Segment.Default) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:PVTime:FEDGe:MIMO<n>:SEGMent<seg>:TIME \n
		Snippet: value: List[float] = driver.multiEval.trace.powerVsTime.fallingEdge.mimo.segment.time.fetch(start = 1.0, count = 1.0, decimation = 1.0, mimo = repcap.Mimo.Default, segment = repcap.Segment.Default) \n
		Return the time indices for the power vs. time ramp traces (for 80+80 MHz, MIMO) , rising edge (REDGe) and falling edge
		(FEDGe) . Refer to method RsCmwWlanMeas.MultiEval.Trace.PowerVsTime.RisingEdge.Mimo.Segment.Current.fetch \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param count: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param decimation: numeric For the optional query parameters start, count and decimation, see 'Trace Sub-Arrays'.
			:param mimo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mimo')
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: time_values: float Comma-separated list of time indices corresponding to the ramp power results. Unit: s"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		mimo_cmd_val = self._base.get_repcap_cmd_value(mimo, repcap.Mimo)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:PVTime:FEDGe:MIMO{mimo_cmd_val}:SEGMent{segment_cmd_val}:TIME? {param}'.rstrip(), suppressed)
		return response
