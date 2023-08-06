from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A:
	"""A commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("a", core, parent)

	def set(self, tsm_lim_yrel_lev_a: float, bandwidthE=repcap.BandwidthE.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:VHTofdm:BW<bandwidth>:Y:A \n
		Snippet: driver.configure.multiEval.limit.tsMask.vhtOfdm.bw.y.a.set(tsm_lim_yrel_lev_a = 1.0, bandwidthE = repcap.BandwidthE.Default) \n
		Defines the relative spectral density limit for point A (frequency offset: 2*bandwidth) on the transmit spectrum mask for
		802.11ac signals with the specified <bandwidth>. See 'Transmit Spectrum Mask OFDM, Default Masks' for background
		information. \n
			:param tsm_lim_yrel_lev_a: numeric Range: -90 dB to 10 dB , Unit: dB
			:param bandwidthE: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')"""
		param = Conversions.decimal_value_to_str(tsm_lim_yrel_lev_a)
		bandwidthE_cmd_val = self._base.get_repcap_cmd_value(bandwidthE, repcap.BandwidthE)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:VHTofdm:BW{bandwidthE_cmd_val}:Y:A {param}')

	def get(self, bandwidthE=repcap.BandwidthE.Default) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:VHTofdm:BW<bandwidth>:Y:A \n
		Snippet: value: float = driver.configure.multiEval.limit.tsMask.vhtOfdm.bw.y.a.get(bandwidthE = repcap.BandwidthE.Default) \n
		Defines the relative spectral density limit for point A (frequency offset: 2*bandwidth) on the transmit spectrum mask for
		802.11ac signals with the specified <bandwidth>. See 'Transmit Spectrum Mask OFDM, Default Masks' for background
		information. \n
			:param bandwidthE: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')
			:return: tsm_lim_yrel_lev_a: numeric Range: -90 dB to 10 dB , Unit: dB"""
		bandwidthE_cmd_val = self._base.get_repcap_cmd_value(bandwidthE, repcap.BandwidthE)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:VHTofdm:BW{bandwidthE_cmd_val}:Y:A?')
		return Conversions.str_to_float(response)
