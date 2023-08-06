from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Segment:
	"""Segment commands group definition. 13 total commands, 13 Sub-groups, 0 group commands
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
	def setup(self):
		"""setup commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_setup'):
			from .Segment_.Setup import Setup
			self._setup = Setup(self._core, self._base)
		return self._setup

	@property
	def stime(self):
		"""stime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stime'):
			from .Segment_.Stime import Stime
			self._stime = Stime(self._core, self._base)
		return self._stime

	@property
	def mtime(self):
		"""mtime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtime'):
			from .Segment_.Mtime import Mtime
			self._mtime = Mtime(self._core, self._base)
		return self._mtime

	@property
	def moffset(self):
		"""moffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_moffset'):
			from .Segment_.Moffset import Moffset
			self._moffset = Moffset(self._core, self._base)
		return self._moffset

	@property
	def envelopePower(self):
		"""envelopePower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_envelopePower'):
			from .Segment_.EnvelopePower import EnvelopePower
			self._envelopePower = EnvelopePower(self._core, self._base)
		return self._envelopePower

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Segment_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def standard(self):
		"""standard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_standard'):
			from .Segment_.Standard import Standard
			self._standard = Standard(self._core, self._base)
		return self._standard

	@property
	def bandwidth(self):
		"""bandwidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bandwidth'):
			from .Segment_.Bandwidth import Bandwidth
			self._bandwidth = Bandwidth(self._core, self._base)
		return self._bandwidth

	@property
	def btype(self):
		"""btype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_btype'):
			from .Segment_.Btype import Btype
			self._btype = Btype(self._core, self._base)
		return self._btype

	@property
	def rtrigger(self):
		"""rtrigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rtrigger'):
			from .Segment_.Rtrigger import Rtrigger
			self._rtrigger = Rtrigger(self._core, self._base)
		return self._rtrigger

	@property
	def singleCmw(self):
		"""singleCmw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_singleCmw'):
			from .Segment_.SingleCmw import SingleCmw
			self._singleCmw = SingleCmw(self._core, self._base)
		return self._singleCmw

	@property
	def scount(self):
		"""scount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scount'):
			from .Segment_.Scount import Scount
			self._scount = Scount(self._core, self._base)
		return self._scount

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_result'):
			from .Segment_.Result import Result
			self._result = Result(self._core, self._base)
		return self._result

	def clone(self) -> 'Segment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Segment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
