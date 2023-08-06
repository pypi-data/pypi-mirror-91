from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TsMask:
	"""TsMask commands group definition. 140 total commands, 12 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tsMask", core, parent)

	@property
	def obw(self):
		"""obw commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_obw'):
			from .TsMask_.Obw import Obw
			self._obw = Obw(self._core, self._base)
		return self._obw

	@property
	def ofdm(self):
		"""ofdm commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_ofdm'):
			from .TsMask_.Ofdm import Ofdm
			self._ofdm = Ofdm(self._core, self._base)
		return self._ofdm

	@property
	def dsss(self):
		"""dsss commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_dsss'):
			from .TsMask_.Dsss import Dsss
			self._dsss = Dsss(self._core, self._base)
		return self._dsss

	@property
	def nsiso(self):
		"""nsiso commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_nsiso'):
			from .TsMask_.Nsiso import Nsiso
			self._nsiso = Nsiso(self._core, self._base)
		return self._nsiso

	@property
	def acsiso(self):
		"""acsiso commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_acsiso'):
			from .TsMask_.Acsiso import Acsiso
			self._acsiso = Acsiso(self._core, self._base)
		return self._acsiso

	@property
	def mimo(self):
		"""mimo commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_mimo'):
			from .TsMask_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .TsMask_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .TsMask_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_maximum'):
			from .TsMask_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def minimum(self):
		"""minimum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_minimum'):
			from .TsMask_.Minimum import Minimum
			self._minimum = Minimum(self._core, self._base)
		return self._minimum

	@property
	def segments(self):
		"""segments commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_segments'):
			from .TsMask_.Segments import Segments
			self._segments = Segments(self._core, self._base)
		return self._segments

	@property
	def frequency(self):
		"""frequency commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .TsMask_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	def clone(self) -> 'TsMask':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TsMask(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
