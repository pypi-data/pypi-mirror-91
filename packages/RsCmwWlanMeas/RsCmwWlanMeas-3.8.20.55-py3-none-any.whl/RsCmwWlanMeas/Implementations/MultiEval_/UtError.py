from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UtError:
	"""UtError commands group definition. 27 total commands, 6 Sub-groups, 0 group commands
	Repeated Capability: UtError, default value after init: UtError.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("utError", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_utError_get', 'repcap_utError_set', repcap.UtError.Nr1)

	def repcap_utError_set(self, enum_value: repcap.UtError) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UtError.Default
		Default value after init: UtError.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_utError_get(self) -> repcap.UtError:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .UtError_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .UtError_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_maximum'):
			from .UtError_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def minimum(self):
		"""minimum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_minimum'):
			from .UtError_.Minimum import Minimum
			self._minimum = Minimum(self._core, self._base)
		return self._minimum

	@property
	def limit(self):
		"""limit commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_limit'):
			from .UtError_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	@property
	def margin(self):
		"""margin commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_margin'):
			from .UtError_.Margin import Margin
			self._margin = Margin(self._core, self._base)
		return self._margin

	def clone(self) -> 'UtError':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UtError(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
