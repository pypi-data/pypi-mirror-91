from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Runit:
	"""Runit commands group definition. 8 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: ResourceUnit, default value after init: ResourceUnit.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("runit", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_resourceUnit_get', 'repcap_resourceUnit_set', repcap.ResourceUnit.Nr1)

	def repcap_resourceUnit_set(self, enum_value: repcap.ResourceUnit) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ResourceUnit.Default
		Default value after init: ResourceUnit.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_resourceUnit_get(self) -> repcap.ResourceUnit:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_current'):
			from .Runit_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_average'):
			from .Runit_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_maximum'):
			from .Runit_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def standardDev(self):
		"""standardDev commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_standardDev'):
			from .Runit_.StandardDev import StandardDev
			self._standardDev = StandardDev(self._core, self._base)
		return self._standardDev

	@property
	def rxAntenna(self):
		"""rxAntenna commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_rxAntenna'):
			from .Runit_.RxAntenna import RxAntenna
			self._rxAntenna = RxAntenna(self._core, self._base)
		return self._rxAntenna

	def clone(self) -> 'Runit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Runit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
