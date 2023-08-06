from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Segment:
	"""Segment commands group definition. 18 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: SegmentB, default value after init: SegmentB.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("segment", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_segmentB_get', 'repcap_segmentB_set', repcap.SegmentB.Nr1)

	def repcap_segmentB_set(self, enum_value: repcap.SegmentB) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SegmentB.Default
		Default value after init: SegmentB.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_segmentB_get(self) -> repcap.SegmentB:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def modulation(self):
		"""modulation commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_modulation'):
			from .Segment_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def tsMask(self):
		"""tsMask commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsMask'):
			from .Segment_.TsMask import TsMask
			self._tsMask = TsMask(self._core, self._base)
		return self._tsMask

	def clone(self) -> 'Segment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Segment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
