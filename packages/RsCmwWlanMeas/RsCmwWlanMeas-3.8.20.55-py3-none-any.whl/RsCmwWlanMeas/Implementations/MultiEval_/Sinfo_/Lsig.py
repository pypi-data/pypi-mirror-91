from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lsig:
	"""Lsig commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lsig", core, parent)

	@property
	def rate(self):
		"""rate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rate'):
			from .Lsig_.Rate import Rate
			self._rate = Rate(self._core, self._base)
		return self._rate

	@property
	def reserved(self):
		"""reserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reserved'):
			from .Lsig_.Reserved import Reserved
			self._reserved = Reserved(self._core, self._base)
		return self._reserved

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Lsig_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	@property
	def parity(self):
		"""parity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_parity'):
			from .Lsig_.Parity import Parity
			self._parity = Parity(self._core, self._base)
		return self._parity

	@property
	def tail(self):
		"""tail commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tail'):
			from .Lsig_.Tail import Tail
			self._tail = Tail(self._core, self._base)
		return self._tail

	def clone(self) -> 'Lsig':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Lsig(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
