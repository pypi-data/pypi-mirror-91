from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 36 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	@property
	def dsss(self):
		"""dsss commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_dsss'):
			from .Modulation_.Dsss import Dsss
			self._dsss = Dsss(self._core, self._base)
		return self._dsss

	@property
	def lofdm(self):
		"""lofdm commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_lofdm'):
			from .Modulation_.Lofdm import Lofdm
			self._lofdm = Lofdm(self._core, self._base)
		return self._lofdm

	@property
	def pofdm(self):
		"""pofdm commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_pofdm'):
			from .Modulation_.Pofdm import Pofdm
			self._pofdm = Pofdm(self._core, self._base)
		return self._pofdm

	@property
	def htOfdm(self):
		"""htOfdm commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_htOfdm'):
			from .Modulation_.HtOfdm import HtOfdm
			self._htOfdm = HtOfdm(self._core, self._base)
		return self._htOfdm

	@property
	def vhtOfdm(self):
		"""vhtOfdm commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_vhtOfdm'):
			from .Modulation_.VhtOfdm import VhtOfdm
			self._vhtOfdm = VhtOfdm(self._core, self._base)
		return self._vhtOfdm

	@property
	def heOfdm(self):
		"""heOfdm commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_heOfdm'):
			from .Modulation_.HeOfdm import HeOfdm
			self._heOfdm = HeOfdm(self._core, self._base)
		return self._heOfdm

	def clone(self) -> 'Modulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Modulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
