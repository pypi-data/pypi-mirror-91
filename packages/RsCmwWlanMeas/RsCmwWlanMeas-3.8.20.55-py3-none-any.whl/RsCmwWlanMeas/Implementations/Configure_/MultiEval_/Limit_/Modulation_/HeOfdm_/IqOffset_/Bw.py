from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bw:
	"""Bw commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: BandwidthE, default value after init: BandwidthE.Bw5"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bw", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_bandwidthE_get', 'repcap_bandwidthE_set', repcap.BandwidthE.Bw5)

	def repcap_bandwidthE_set(self, enum_value: repcap.BandwidthE) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to BandwidthE.Default
		Default value after init: BandwidthE.Bw5"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_bandwidthE_get(self) -> repcap.BandwidthE:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class BwStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- Offset_Value_Rel: float or bool: numeric | ON | OFF Relative limit Range: -100 dB to 0 dB, Unit: dB Additional parameters: OFF | ON (disables | enables the limit check)
			- Offset_Value_Abs: float or bool: Optional setting parameter. numeric | ON | OFF Absolute limit Range: -100 dBm to 0 dBm, Unit: dBm Additional parameters: OFF | ON (disables | enables the limit check)"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Offset_Value_Rel'),
			ArgStruct.scalar_float_ext('Offset_Value_Abs')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Offset_Value_Rel: float or bool = None
			self.Offset_Value_Abs: float or bool = None

	def set(self, structure: BwStruct, bandwidthE=repcap.BandwidthE.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:IQOFfset:BW<BW> \n
		Snippet: driver.configure.multiEval.limit.modulation.heOfdm.iqOffset.bw.set(value = [PROPERTY_STRUCT_NAME](), bandwidthE = repcap.BandwidthE.Default) \n
		Defines and activates upper limits for the I/Q origin offset, for 802.11ax and channel bandwidth <BW>. \n
			:param structure: for set value, see the help for BwStruct structure arguments.
			:param bandwidthE: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')"""
		bandwidthE_cmd_val = self._base.get_repcap_cmd_value(bandwidthE, repcap.BandwidthE)
		self._core.io.write_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:IQOFfset:BW{bandwidthE_cmd_val}', structure)

	def get(self, bandwidthE=repcap.BandwidthE.Default) -> BwStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:IQOFfset:BW<BW> \n
		Snippet: value: BwStruct = driver.configure.multiEval.limit.modulation.heOfdm.iqOffset.bw.get(bandwidthE = repcap.BandwidthE.Default) \n
		Defines and activates upper limits for the I/Q origin offset, for 802.11ax and channel bandwidth <BW>. \n
			:param bandwidthE: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Bw')
			:return: structure: for return value, see the help for BwStruct structure arguments."""
		bandwidthE_cmd_val = self._base.get_repcap_cmd_value(bandwidthE, repcap.BandwidthE)
		return self._core.io.query_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:IQOFfset:BW{bandwidthE_cmd_val}?', self.__class__.BwStruct())

	def clone(self) -> 'Bw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
