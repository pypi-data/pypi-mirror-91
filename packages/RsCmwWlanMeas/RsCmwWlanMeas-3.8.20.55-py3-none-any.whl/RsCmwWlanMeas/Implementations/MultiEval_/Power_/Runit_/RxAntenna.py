from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxAntenna:
	"""RxAntenna commands group definition. 4 total commands, 4 Sub-groups, 0 group commands
	Repeated Capability: RxAntenna, default value after init: RxAntenna.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxAntenna", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_rxAntenna_get', 'repcap_rxAntenna_set', repcap.RxAntenna.Nr1)

	def repcap_rxAntenna_set(self, enum_value: repcap.RxAntenna) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to RxAntenna.Default
		Default value after init: RxAntenna.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_rxAntenna_get(self) -> repcap.RxAntenna:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_current'):
			from .RxAntenna_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_average'):
			from .RxAntenna_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_maximum'):
			from .RxAntenna_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def standardDev(self):
		"""standardDev commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_standardDev'):
			from .RxAntenna_.StandardDev import StandardDev
			self._standardDev = StandardDev(self._core, self._base)
		return self._standardDev

	def clone(self) -> 'RxAntenna':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxAntenna(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
