from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cfield:
	"""Cfield commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfield", core, parent)

	@property
	def ruAllocation(self):
		"""ruAllocation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ruAllocation'):
			from .Cfield_.RuAllocation import RuAllocation
			self._ruAllocation = RuAllocation(self._core, self._base)
		return self._ruAllocation

	@property
	def cru(self):
		"""cru commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cru'):
			from .Cfield_.Cru import Cru
			self._cru = Cru(self._core, self._base)
		return self._cru

	@property
	def crc(self):
		"""crc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .Cfield_.Crc import Crc
			self._crc = Crc(self._core, self._base)
		return self._crc

	@property
	def tail(self):
		"""tail commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tail'):
			from .Cfield_.Tail import Tail
			self._tail = Tail(self._core, self._base)
		return self._tail

	def clone(self) -> 'Cfield':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cfield(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
