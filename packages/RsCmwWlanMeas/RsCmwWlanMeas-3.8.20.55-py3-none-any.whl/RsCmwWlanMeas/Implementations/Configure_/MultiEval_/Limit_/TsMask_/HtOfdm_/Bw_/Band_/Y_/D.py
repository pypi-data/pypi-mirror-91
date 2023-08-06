from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class D:
	"""D commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("d", core, parent)

	def set(self, tsm_lim_yrel_lev_d: float, bandwidthC=repcap.BandwidthC.Default, band=repcap.Band.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:HTOFdm:BW<bandwidth>:BAND<band>:Y:D \n
		Snippet: driver.configure.multiEval.limit.tsMask.htOfdm.bw.band.y.d.set(tsm_lim_yrel_lev_d = 1.0, bandwidthC = repcap.BandwidthC.Default, band = repcap.Band.Default) \n
		Defines the relative spectral density limit for point D (frequency offset: 1/2*bandwidth + 1 MHz) on the transmit
		spectrum mask for 802.11n signals with the specified <bandwidth> and the selected <band>. See 'Transmit Spectrum Mask
		OFDM, Default Masks' for background information. \n
			:param tsm_lim_yrel_lev_d: numeric Range: -90 dB to 10 dB , Unit: dB
			:param bandwidthC: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')
			:param band: optional repeated capability selector. Default value: Nr2 (settable in the interface 'Band')"""
		param = Conversions.decimal_value_to_str(tsm_lim_yrel_lev_d)
		bandwidthC_cmd_val = self._base.get_repcap_cmd_value(bandwidthC, repcap.BandwidthC)
		band_cmd_val = self._base.get_repcap_cmd_value(band, repcap.Band)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:HTOFdm:BW{bandwidthC_cmd_val}:BAND{band_cmd_val}:Y:D {param}')

	def get(self, bandwidthC=repcap.BandwidthC.Default, band=repcap.Band.Default) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:HTOFdm:BW<bandwidth>:BAND<band>:Y:D \n
		Snippet: value: float = driver.configure.multiEval.limit.tsMask.htOfdm.bw.band.y.d.get(bandwidthC = repcap.BandwidthC.Default, band = repcap.Band.Default) \n
		Defines the relative spectral density limit for point D (frequency offset: 1/2*bandwidth + 1 MHz) on the transmit
		spectrum mask for 802.11n signals with the specified <bandwidth> and the selected <band>. See 'Transmit Spectrum Mask
		OFDM, Default Masks' for background information. \n
			:param bandwidthC: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')
			:param band: optional repeated capability selector. Default value: Nr2 (settable in the interface 'Band')
			:return: tsm_lim_yrel_lev_d: numeric Range: -90 dB to 10 dB , Unit: dB"""
		bandwidthC_cmd_val = self._base.get_repcap_cmd_value(bandwidthC, repcap.BandwidthC)
		band_cmd_val = self._base.get_repcap_cmd_value(band, repcap.Band)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:HTOFdm:BW{bandwidthC_cmd_val}:BAND{band_cmd_val}:Y:D?')
		return Conversions.str_to_float(response)
