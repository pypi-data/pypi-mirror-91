from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lower:
	"""Lower commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lower", core, parent)

	# noinspection PyTypeChecker
	class LowerStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Center: float: numeric Range: -20 dB to 4 dB, Unit: dB
			- Side: float: numeric Range: -20 dB to 4 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Center'),
			ArgStruct.scalar_float('Side')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Center: float = None
			self.Side: float = None

	def set(self, structure: LowerStruct, bandwidthD=repcap.BandwidthD.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:HEOFdm:BW<bandwidth>:LOWer \n
		Snippet: driver.configure.multiEval.limit.spectrFlatness.heOfdm.bw.lower.set(value = [PROPERTY_STRUCT_NAME](), bandwidthD = repcap.BandwidthD.Default) \n
		Defines the lower limits for the spectrum flatness of the center subcarriers and the side subcarriers for 802.
		11ax signals with the specified <bandwidth>. The lower limits must be smaller than the upper limit. \n
			:param structure: for set value, see the help for LowerStruct structure arguments.
			:param bandwidthD: optional repeated capability selector. Default value: Bw20 (settable in the interface 'Bw')"""
		bandwidthD_cmd_val = self._base.get_repcap_cmd_value(bandwidthD, repcap.BandwidthD)
		self._core.io.write_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:HEOFdm:BW{bandwidthD_cmd_val}:LOWer', structure)

	def get(self, bandwidthD=repcap.BandwidthD.Default) -> LowerStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:HEOFdm:BW<bandwidth>:LOWer \n
		Snippet: value: LowerStruct = driver.configure.multiEval.limit.spectrFlatness.heOfdm.bw.lower.get(bandwidthD = repcap.BandwidthD.Default) \n
		Defines the lower limits for the spectrum flatness of the center subcarriers and the side subcarriers for 802.
		11ax signals with the specified <bandwidth>. The lower limits must be smaller than the upper limit. \n
			:param bandwidthD: optional repeated capability selector. Default value: Bw20 (settable in the interface 'Bw')
			:return: structure: for return value, see the help for LowerStruct structure arguments."""
		bandwidthD_cmd_val = self._base.get_repcap_cmd_value(bandwidthD, repcap.BandwidthD)
		return self._core.io.query_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:HEOFdm:BW{bandwidthD_cmd_val}:LOWer?', self.__class__.LowerStruct())
