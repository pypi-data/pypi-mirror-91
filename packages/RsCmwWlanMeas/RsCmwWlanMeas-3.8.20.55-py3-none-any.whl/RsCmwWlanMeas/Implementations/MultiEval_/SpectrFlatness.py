from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpectrFlatness:
	"""SpectrFlatness commands group definition. 40 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spectrFlatness", core, parent)

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .SpectrFlatness_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .SpectrFlatness_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_maximum'):
			from .SpectrFlatness_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def minimum(self):
		"""minimum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_minimum'):
			from .SpectrFlatness_.Minimum import Minimum
			self._minimum = Minimum(self._core, self._base)
		return self._minimum

	@property
	def x(self):
		"""x commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_x'):
			from .SpectrFlatness_.X import X
			self._x = X(self._core, self._base)
		return self._x

	@property
	def mimo(self):
		"""mimo commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_mimo'):
			from .SpectrFlatness_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	def clone(self) -> 'SpectrFlatness':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpectrFlatness(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
