from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnvelopePower:
	"""EnvelopePower commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("envelopePower", core, parent)

	def set(self, level: float, segmentB=repcap.SegmentB.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:ENPower \n
		Snippet: driver.configure.multiEval.listPy.segment.envelopePower.set(level = 1.0, segmentB = repcap.SegmentB.Default) \n
		Specifies the expected nominal power of the measured RF signal for segment <no> in list mode. \n
			:param level: numeric The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin Range: -47 dBm to 34 dBm for the input power at RF 1 COM and RF 2 COM (please notice also the ranges quoted in the data sheet) . , Unit: dBm
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		param = Conversions.decimal_value_to_str(level)
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:ENPower {param}')

	def get(self, segmentB=repcap.SegmentB.Default) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:ENPower \n
		Snippet: value: float = driver.configure.multiEval.listPy.segment.envelopePower.get(segmentB = repcap.SegmentB.Default) \n
		Specifies the expected nominal power of the measured RF signal for segment <no> in list mode. \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: level: numeric The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin Range: -47 dBm to 34 dBm for the input power at RF 1 COM and RF 2 COM (please notice also the ranges quoted in the data sheet) . , Unit: dBm"""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:ENPower?')
		return Conversions.str_to_float(response)
