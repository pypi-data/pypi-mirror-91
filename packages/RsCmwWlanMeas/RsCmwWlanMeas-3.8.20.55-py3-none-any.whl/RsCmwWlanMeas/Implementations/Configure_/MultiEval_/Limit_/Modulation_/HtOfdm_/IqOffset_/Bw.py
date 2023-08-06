from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bw:
	"""Bw commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: BandwidthC, default value after init: BandwidthC.Bw5"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bw", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_bandwidthC_get', 'repcap_bandwidthC_set', repcap.BandwidthC.Bw5)

	def repcap_bandwidthC_set(self, enum_value: repcap.BandwidthC) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to BandwidthC.Default
		Default value after init: BandwidthC.Bw5"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_bandwidthC_get(self) -> repcap.BandwidthC:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, offset_value: float or bool, bandwidthC=repcap.BandwidthC.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HTOFdm:IQOFfset:BW<BW> \n
		Snippet: driver.configure.multiEval.limit.modulation.htOfdm.iqOffset.bw.set(offset_value = 1.0, bandwidthC = repcap.BandwidthC.Default) \n
		Defines and activates an upper limit for the I/Q origin offset, for 802.11n and channel bandwidth <BW>. \n
			:param offset_value: numeric | ON | OFF Range: -100 dB to 0 dB, Unit: dB Additional parameters: OFF | ON (disables | enables the limit check)
			:param bandwidthC: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')"""
		param = Conversions.decimal_or_bool_value_to_str(offset_value)
		bandwidthC_cmd_val = self._base.get_repcap_cmd_value(bandwidthC, repcap.BandwidthC)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HTOFdm:IQOFfset:BW{bandwidthC_cmd_val} {param}')

	def get(self, bandwidthC=repcap.BandwidthC.Default) -> float or bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HTOFdm:IQOFfset:BW<BW> \n
		Snippet: value: float or bool = driver.configure.multiEval.limit.modulation.htOfdm.iqOffset.bw.get(bandwidthC = repcap.BandwidthC.Default) \n
		Defines and activates an upper limit for the I/Q origin offset, for 802.11n and channel bandwidth <BW>. \n
			:param bandwidthC: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')
			:return: offset_value: numeric | ON | OFF Range: -100 dB to 0 dB, Unit: dB Additional parameters: OFF | ON (disables | enables the limit check)"""
		bandwidthC_cmd_val = self._base.get_repcap_cmd_value(bandwidthC, repcap.BandwidthC)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HTOFdm:IQOFfset:BW{bandwidthC_cmd_val}?')
		return Conversions.str_to_float_or_bool(response)

	def clone(self) -> 'Bw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
