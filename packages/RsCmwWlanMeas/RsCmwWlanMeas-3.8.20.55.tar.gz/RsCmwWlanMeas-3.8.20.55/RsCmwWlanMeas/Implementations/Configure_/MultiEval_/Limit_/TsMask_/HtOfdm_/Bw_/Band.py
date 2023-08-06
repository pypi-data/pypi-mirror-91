from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Band:
	"""Band commands group definition. 4 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Band, default value after init: Band.Nr2"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("band", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_band_get', 'repcap_band_set', repcap.Band.Nr2)

	def repcap_band_set(self, enum_value: repcap.Band) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Band.Default
		Default value after init: Band.Nr2"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_band_get(self) -> repcap.Band:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def y(self):
		"""y commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_y'):
			from .Band_.Y import Y
			self._y = Y(self._core, self._base)
		return self._y

	def clone(self) -> 'Band':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Band(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
