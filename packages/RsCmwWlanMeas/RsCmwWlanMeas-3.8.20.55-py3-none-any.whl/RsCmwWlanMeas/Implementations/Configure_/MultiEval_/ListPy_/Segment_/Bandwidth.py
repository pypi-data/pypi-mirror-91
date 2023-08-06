from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bandwidth", core, parent)

	def set(self, band_width: enums.Bandwidth, segmentB=repcap.SegmentB.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:BWIDth \n
		Snippet: driver.configure.multiEval.listPy.segment.bandwidth.set(band_width = enums.Bandwidth.BW05mhz, segmentB = repcap.SegmentB.Default) \n
		Specifies the channel bandwidth for segment <no> in list mode. \n
			:param band_width: BW05mhz | BW10mhz | BW20mhz | BW40mhz | BW80mhz | BW16mhz BW05mhz: 5 MHz (802.11p, n, ac) BW10mhz: 10 MHz (802.11p, n, ac) BW20mhz: 20 MHz (all standards) BW40mhz: 40 MHz (802.11n, ac, ax) BW80mhz: 80 MHz (802.11ac, ax) BW16mhz: 160 MHz (802.11ac, ax)
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		param = Conversions.enum_scalar_to_str(band_width, enums.Bandwidth)
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:BWIDth {param}')

	# noinspection PyTypeChecker
	def get(self, segmentB=repcap.SegmentB.Default) -> enums.Bandwidth:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:BWIDth \n
		Snippet: value: enums.Bandwidth = driver.configure.multiEval.listPy.segment.bandwidth.get(segmentB = repcap.SegmentB.Default) \n
		Specifies the channel bandwidth for segment <no> in list mode. \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: band_width: BW05mhz | BW10mhz | BW20mhz | BW40mhz | BW80mhz | BW16mhz BW05mhz: 5 MHz (802.11p, n, ac) BW10mhz: 10 MHz (802.11p, n, ac) BW20mhz: 20 MHz (all standards) BW40mhz: 40 MHz (802.11n, ac, ax) BW80mhz: 80 MHz (802.11ac, ax) BW16mhz: 160 MHz (802.11ac, ax)"""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:BWIDth?')
		return Conversions.str_to_scalar_enum(response, enums.Bandwidth)
