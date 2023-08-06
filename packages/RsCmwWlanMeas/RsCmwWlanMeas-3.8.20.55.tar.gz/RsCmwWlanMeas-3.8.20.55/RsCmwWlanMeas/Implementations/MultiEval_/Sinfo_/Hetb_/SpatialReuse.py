from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpatialReuse:
	"""SpatialReuse commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Spatial, default value after init: Spatial.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spatialReuse", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_spatial_get', 'repcap_spatial_set', repcap.Spatial.Nr1)

	def repcap_spatial_set(self, enum_value: repcap.Spatial) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Spatial.Default
		Default value after init: Spatial.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_spatial_get(self) -> repcap.Spatial:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Value_Bin: str: string
			- Value_Dec: int: decimal Range: 0 to 63"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_str('Value_Bin'),
			ArgStruct.scalar_int('Value_Dec')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Value_Bin: str = None
			self.Value_Dec: int = None

	def fetch(self, spatial=repcap.Spatial.Default) -> FetchStruct:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:SINFo:HETB:SPATialreuse<index> \n
		Snippet: value: FetchStruct = driver.multiEval.sinfo.hetb.spatialReuse.fetch(spatial = repcap.Spatial.Default) \n
		Queries the value of Spatial Reuse field signaled in HE signal field for trigger based uplink single user MIMO (HE-SIG-A)
		. \n
			:param spatial: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SpatialReuse')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		spatial_cmd_val = self._base.get_repcap_cmd_value(spatial, repcap.Spatial)
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:SINFo:HETB:SPATialreuse{spatial_cmd_val}?', self.__class__.FetchStruct())

	def clone(self) -> 'SpatialReuse':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpatialReuse(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
