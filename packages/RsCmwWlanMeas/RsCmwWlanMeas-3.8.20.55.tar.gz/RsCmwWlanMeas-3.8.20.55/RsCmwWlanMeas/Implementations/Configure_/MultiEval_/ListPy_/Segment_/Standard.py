from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Standard:
	"""Standard commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standard", core, parent)

	def set(self, standard: enums.IeeeStandard, segmentB=repcap.SegmentB.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:STANdard \n
		Snippet: driver.configure.multiEval.listPy.segment.standard.set(standard = enums.IeeeStandard.DSSS, segmentB = repcap.SegmentB.Default) \n
		Specifies the standard for segment <no> in list mode. \n
			:param standard: DSSS | LOFDm | POFDm | HTOFdm | VHTofdm | HEOFdm DSSS: 802.11b/g (DSSS) LOFDm: 802.11a/g (OFDM) LOFDm: 802.11p HTOFdm: 802.11n VHTofdm: 802.11ac HEOFdm: 802.11ax (R&S CMW with TRX160 only)
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		param = Conversions.enum_scalar_to_str(standard, enums.IeeeStandard)
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:STANdard {param}')

	# noinspection PyTypeChecker
	def get(self, segmentB=repcap.SegmentB.Default) -> enums.IeeeStandard:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:STANdard \n
		Snippet: value: enums.IeeeStandard = driver.configure.multiEval.listPy.segment.standard.get(segmentB = repcap.SegmentB.Default) \n
		Specifies the standard for segment <no> in list mode. \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: standard: DSSS | LOFDm | POFDm | HTOFdm | VHTofdm | HEOFdm DSSS: 802.11b/g (DSSS) LOFDm: 802.11a/g (OFDM) LOFDm: 802.11p HTOFdm: 802.11n VHTofdm: 802.11ac HEOFdm: 802.11ax (R&S CMW with TRX160 only)"""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.IeeeStandard)
