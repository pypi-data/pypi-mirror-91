from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 144 total commands, 14 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	@property
	def cmimo(self):
		"""cmimo commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmimo'):
			from .Modulation_.Cmimo import Cmimo
			self._cmimo = Cmimo(self._core, self._base)
		return self._cmimo

	@property
	def evMagnitude(self):
		"""evMagnitude commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_evMagnitude'):
			from .Modulation_.EvMagnitude import EvMagnitude
			self._evMagnitude = EvMagnitude(self._core, self._base)
		return self._evMagnitude

	@property
	def cfoDistribution(self):
		"""cfoDistribution commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_cfoDistribution'):
			from .Modulation_.CfoDistribution import CfoDistribution
			self._cfoDistribution = CfoDistribution(self._core, self._base)
		return self._cfoDistribution

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .Modulation_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .Modulation_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_maximum'):
			from .Modulation_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def standardDev(self):
		"""standardDev commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_standardDev'):
			from .Modulation_.StandardDev import StandardDev
			self._standardDev = StandardDev(self._core, self._base)
		return self._standardDev

	@property
	def minimum(self):
		"""minimum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_minimum'):
			from .Modulation_.Minimum import Minimum
			self._minimum = Minimum(self._core, self._base)
		return self._minimum

	@property
	def segments(self):
		"""segments commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_segments'):
			from .Modulation_.Segments import Segments
			self._segments = Segments(self._core, self._base)
		return self._segments

	@property
	def dsss(self):
		"""dsss commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_dsss'):
			from .Modulation_.Dsss import Dsss
			self._dsss = Dsss(self._core, self._base)
		return self._dsss

	@property
	def mimo(self):
		"""mimo commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_mimo'):
			from .Modulation_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	@property
	def smimo(self):
		"""smimo commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_smimo'):
			from .Modulation_.Smimo import Smimo
			self._smimo = Smimo(self._core, self._base)
		return self._smimo

	@property
	def acsiso(self):
		"""acsiso commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_acsiso'):
			from .Modulation_.Acsiso import Acsiso
			self._acsiso = Acsiso(self._core, self._base)
		return self._acsiso

	@property
	def ofdm(self):
		"""ofdm commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ofdm'):
			from .Modulation_.Ofdm import Ofdm
			self._ofdm = Ofdm(self._core, self._base)
		return self._ofdm

	def clone(self) -> 'Modulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Modulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
