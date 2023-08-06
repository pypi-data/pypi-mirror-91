from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Upper:
	"""Upper commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("upper", core, parent)

	def set(self, upper: float, bandwidthE=repcap.BandwidthE.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:VHTofdm:BW<bandwidth>:UPPer \n
		Snippet: driver.configure.multiEval.limit.spectrFlatness.vhtOfdm.bw.upper.set(upper = 1.0, bandwidthE = repcap.BandwidthE.Default) \n
		Defines an upper limit for the spectrum flatness of 802.11ac signals with the specified <bandwidth>. The upper limit must
		be larger than the lower limits. \n
			:param upper: numeric Range: -4 dB to 20 dB, Unit: dB
			:param bandwidthE: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')"""
		param = Conversions.decimal_value_to_str(upper)
		bandwidthE_cmd_val = self._base.get_repcap_cmd_value(bandwidthE, repcap.BandwidthE)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:VHTofdm:BW{bandwidthE_cmd_val}:UPPer {param}')

	def get(self, bandwidthE=repcap.BandwidthE.Default) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:VHTofdm:BW<bandwidth>:UPPer \n
		Snippet: value: float = driver.configure.multiEval.limit.spectrFlatness.vhtOfdm.bw.upper.get(bandwidthE = repcap.BandwidthE.Default) \n
		Defines an upper limit for the spectrum flatness of 802.11ac signals with the specified <bandwidth>. The upper limit must
		be larger than the lower limits. \n
			:param bandwidthE: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')
			:return: upper: numeric Range: -4 dB to 20 dB, Unit: dB"""
		bandwidthE_cmd_val = self._base.get_repcap_cmd_value(bandwidthE, repcap.BandwidthE)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:VHTofdm:BW{bandwidthE_cmd_val}:UPPer?')
		return Conversions.str_to_float(response)
