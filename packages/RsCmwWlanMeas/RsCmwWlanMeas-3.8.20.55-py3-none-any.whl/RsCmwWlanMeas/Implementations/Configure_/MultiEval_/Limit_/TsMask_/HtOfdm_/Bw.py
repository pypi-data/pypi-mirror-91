from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bw:
	"""Bw commands group definition. 6 total commands, 3 Sub-groups, 0 group commands
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

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Bw_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def band(self):
		"""band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_band'):
			from .Bw_.Band import Band
			self._band = Band(self._core, self._base)
		return self._band

	@property
	def absLimit(self):
		"""absLimit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_absLimit'):
			from .Bw_.AbsLimit import AbsLimit
			self._absLimit = AbsLimit(self._core, self._base)
		return self._absLimit

	def clone(self) -> 'Bw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
