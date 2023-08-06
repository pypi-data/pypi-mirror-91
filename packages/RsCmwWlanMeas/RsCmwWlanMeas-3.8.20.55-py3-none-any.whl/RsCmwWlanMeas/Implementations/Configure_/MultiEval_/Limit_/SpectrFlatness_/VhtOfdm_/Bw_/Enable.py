from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enable", core, parent)

	def set(self, enable: bool, bandwidthE=repcap.BandwidthE.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:VHTofdm:BW<bandwidth>:ENABle \n
		Snippet: driver.configure.multiEval.limit.spectrFlatness.vhtOfdm.bw.enable.set(enable = False, bandwidthE = repcap.BandwidthE.Default) \n
		Enables or disables the spectrum flatness limit check for 802.11ac signals with the specified <bandwidth>. \n
			:param enable: ON | OFF
			:param bandwidthE: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')"""
		param = Conversions.bool_to_str(enable)
		bandwidthE_cmd_val = self._base.get_repcap_cmd_value(bandwidthE, repcap.BandwidthE)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:VHTofdm:BW{bandwidthE_cmd_val}:ENABle {param}')

	def get(self, bandwidthE=repcap.BandwidthE.Default) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:VHTofdm:BW<bandwidth>:ENABle \n
		Snippet: value: bool = driver.configure.multiEval.limit.spectrFlatness.vhtOfdm.bw.enable.get(bandwidthE = repcap.BandwidthE.Default) \n
		Enables or disables the spectrum flatness limit check for 802.11ac signals with the specified <bandwidth>. \n
			:param bandwidthE: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')
			:return: enable: ON | OFF"""
		bandwidthE_cmd_val = self._base.get_repcap_cmd_value(bandwidthE, repcap.BandwidthE)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:VHTofdm:BW{bandwidthE_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
