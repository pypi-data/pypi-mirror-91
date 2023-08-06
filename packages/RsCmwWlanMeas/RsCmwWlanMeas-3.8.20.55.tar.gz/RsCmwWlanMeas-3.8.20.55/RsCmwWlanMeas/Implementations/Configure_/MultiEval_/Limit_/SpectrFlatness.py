from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpectrFlatness:
	"""SpectrFlatness commands group definition. 15 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spectrFlatness", core, parent)

	@property
	def lofdm(self):
		"""lofdm commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_lofdm'):
			from .SpectrFlatness_.Lofdm import Lofdm
			self._lofdm = Lofdm(self._core, self._base)
		return self._lofdm

	@property
	def pofdm(self):
		"""pofdm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pofdm'):
			from .SpectrFlatness_.Pofdm import Pofdm
			self._pofdm = Pofdm(self._core, self._base)
		return self._pofdm

	@property
	def htOfdm(self):
		"""htOfdm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_htOfdm'):
			from .SpectrFlatness_.HtOfdm import HtOfdm
			self._htOfdm = HtOfdm(self._core, self._base)
		return self._htOfdm

	@property
	def vhtOfdm(self):
		"""vhtOfdm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_vhtOfdm'):
			from .SpectrFlatness_.VhtOfdm import VhtOfdm
			self._vhtOfdm = VhtOfdm(self._core, self._base)
		return self._vhtOfdm

	@property
	def heOfdm(self):
		"""heOfdm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_heOfdm'):
			from .SpectrFlatness_.HeOfdm import HeOfdm
			self._heOfdm = HeOfdm(self._core, self._base)
		return self._heOfdm

	def clone(self) -> 'SpectrFlatness':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpectrFlatness(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
