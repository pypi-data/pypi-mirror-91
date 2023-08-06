from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rtrigger:
	"""Rtrigger commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rtrigger", core, parent)

	def set(self, re_trigger: bool, segmentB=repcap.SegmentB.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:RTRigger \n
		Snippet: driver.configure.multiEval.listPy.segment.rtrigger.set(re_trigger = False, segmentB = repcap.SegmentB.Default) \n
		Specifies for segment <no> in list mode, whether the measurement waits for a trigger event before measuring the segment,
		or not. For the first segment, the value OFF is always interpreted as ON. The values in curly brackets {} are specified
		for each active segment: {...}seg 1, {...}seg 2, ..., {...}seg n. The number of active segments n is determined by method
		RsCmwWlanMeas.Configure.MultiEval.ListPy.count. \n
			:param re_trigger: OFF | ON OFF: measure the segment without retrigger ON: wait for a trigger event from the trigger source configured via method RsCmwWlanMeas.Trigger.MultiEval.source
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		param = Conversions.bool_to_str(re_trigger)
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:RTRigger {param}')

	def get(self, segmentB=repcap.SegmentB.Default) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:RTRigger \n
		Snippet: value: bool = driver.configure.multiEval.listPy.segment.rtrigger.get(segmentB = repcap.SegmentB.Default) \n
		Specifies for segment <no> in list mode, whether the measurement waits for a trigger event before measuring the segment,
		or not. For the first segment, the value OFF is always interpreted as ON. The values in curly brackets {} are specified
		for each active segment: {...}seg 1, {...}seg 2, ..., {...}seg n. The number of active segments n is determined by method
		RsCmwWlanMeas.Configure.MultiEval.ListPy.count. \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: re_trigger: OFF | ON OFF: measure the segment without retrigger ON: wait for a trigger event from the trigger source configured via method RsCmwWlanMeas.Trigger.MultiEval.source"""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:RTRigger?')
		return Conversions.str_to_bool(response)
