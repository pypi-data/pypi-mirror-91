from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RisingEdge:
	"""RisingEdge commands group definition. 40 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("risingEdge", core, parent)

	@property
	def mimo(self):
		"""mimo commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_mimo'):
			from .RisingEdge_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_current'):
			from .RisingEdge_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_average'):
			from .RisingEdge_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_maximum'):
			from .RisingEdge_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def minimum(self):
		"""minimum commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_minimum'):
			from .RisingEdge_.Minimum import Minimum
			self._minimum = Minimum(self._core, self._base)
		return self._minimum

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_time'):
			from .RisingEdge_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time

	@property
	def segment(self):
		"""segment commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_segment'):
			from .RisingEdge_.Segment import Segment
			self._segment = Segment(self._core, self._base)
		return self._segment

	def clone(self) -> 'RisingEdge':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RisingEdge(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
