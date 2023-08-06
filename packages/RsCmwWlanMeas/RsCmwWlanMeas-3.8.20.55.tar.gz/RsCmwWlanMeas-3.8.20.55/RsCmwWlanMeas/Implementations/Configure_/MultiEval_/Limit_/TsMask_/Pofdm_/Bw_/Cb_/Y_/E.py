from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class E:
	"""E commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("e", core, parent)

	def set(self, tsm_lim_yrel_lev_e: float, bandwidthB=repcap.BandwidthB.Bw5) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:POFDm:BW<bandwidth>:CB:Y:E \n
		Snippet: driver.configure.multiEval.limit.tsMask.pofdm.bw.cb.y.e.set(tsm_lim_yrel_lev_e = 1.0, bandwidthB = repcap.BandwidthB.Bw5) \n
		Defines the Y-value of point E (Δf = 0.5 <bandwidth>) on the 802.11p spectrum mask for power class B and the specified
		<bandwidth>. For background information, see 'Transmit Spectrum Mask OFDM, by Regulation'. \n
			:param tsm_lim_yrel_lev_e: numeric Range: -90 dB to 10 dB, Unit: dB
			:param bandwidthB: optional repeated capability selector. Default value: Bw5"""
		param = Conversions.decimal_value_to_str(tsm_lim_yrel_lev_e)
		bandwidthB_cmd_val = self._base.get_repcap_cmd_value(bandwidthB, repcap.BandwidthB)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:POFDm:BW{bandwidthB_cmd_val}:CB:Y:E {param}')

	def get(self, bandwidthB=repcap.BandwidthB.Bw5) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:POFDm:BW<bandwidth>:CB:Y:E \n
		Snippet: value: float = driver.configure.multiEval.limit.tsMask.pofdm.bw.cb.y.e.get(bandwidthB = repcap.BandwidthB.Bw5) \n
		Defines the Y-value of point E (Δf = 0.5 <bandwidth>) on the 802.11p spectrum mask for power class B and the specified
		<bandwidth>. For background information, see 'Transmit Spectrum Mask OFDM, by Regulation'. \n
			:param bandwidthB: optional repeated capability selector. Default value: Bw5
			:return: tsm_lim_yrel_lev_e: numeric Range: -90 dB to 10 dB, Unit: dB"""
		bandwidthB_cmd_val = self._base.get_repcap_cmd_value(bandwidthB, repcap.BandwidthB)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:POFDm:BW{bandwidthB_cmd_val}:CB:Y:E?')
		return Conversions.str_to_float(response)
