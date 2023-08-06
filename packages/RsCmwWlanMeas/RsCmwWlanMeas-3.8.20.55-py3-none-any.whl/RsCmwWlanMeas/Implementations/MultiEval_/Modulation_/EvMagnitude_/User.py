from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 8 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: User, default value after init: User.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_user_get', 'repcap_user_set', repcap.User.Nr1)

	def repcap_user_set(self, enum_value: repcap.User) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to User.Default
		Default value after init: User.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_user_get(self) -> repcap.User:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_current'):
			from .User_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_average'):
			from .User_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_maximum'):
			from .User_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def standardDev(self):
		"""standardDev commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_standardDev'):
			from .User_.StandardDev import StandardDev
			self._standardDev = StandardDev(self._core, self._base)
		return self._standardDev

	@property
	def stream(self):
		"""stream commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_stream'):
			from .User_.Stream import Stream
			self._stream = Stream(self._core, self._base)
		return self._stream

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
