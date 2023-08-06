from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stime:
	"""Stime commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stime", core, parent)

	def set(self, segment_time: float, segmentB=repcap.SegmentB.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:STIMe \n
		Snippet: driver.configure.multiEval.listPy.segment.stime.set(segment_time = 1.0, segmentB = repcap.SegmentB.Default) \n
		Specifies the duration of the segment for segment <no> in list mode. \n
			:param segment_time: numeric Range: 4E-4 s to 1 s , Unit: s
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		param = Conversions.decimal_value_to_str(segment_time)
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:STIMe {param}')

	def get(self, segmentB=repcap.SegmentB.Default) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:STIMe \n
		Snippet: value: float = driver.configure.multiEval.listPy.segment.stime.get(segmentB = repcap.SegmentB.Default) \n
		Specifies the duration of the segment for segment <no> in list mode. \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: segment_time: numeric Range: 4E-4 s to 1 s , Unit: s"""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:STIMe?')
		return Conversions.str_to_float(response)
