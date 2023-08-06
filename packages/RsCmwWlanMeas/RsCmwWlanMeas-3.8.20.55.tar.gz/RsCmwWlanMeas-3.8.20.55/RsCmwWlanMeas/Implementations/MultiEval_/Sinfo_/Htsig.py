from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Htsig:
	"""Htsig commands group definition. 13 total commands, 13 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("htsig", core, parent)

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Htsig_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def cbw(self):
		"""cbw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbw'):
			from .Htsig_.Cbw import Cbw
			self._cbw = Cbw(self._core, self._base)
		return self._cbw

	@property
	def htLength(self):
		"""htLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_htLength'):
			from .Htsig_.HtLength import HtLength
			self._htLength = HtLength(self._core, self._base)
		return self._htLength

	@property
	def smoothing(self):
		"""smoothing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smoothing'):
			from .Htsig_.Smoothing import Smoothing
			self._smoothing = Smoothing(self._core, self._base)
		return self._smoothing

	@property
	def nsounding(self):
		"""nsounding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsounding'):
			from .Htsig_.Nsounding import Nsounding
			self._nsounding = Nsounding(self._core, self._base)
		return self._nsounding

	@property
	def reserved(self):
		"""reserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reserved'):
			from .Htsig_.Reserved import Reserved
			self._reserved = Reserved(self._core, self._base)
		return self._reserved

	@property
	def aggregation(self):
		"""aggregation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aggregation'):
			from .Htsig_.Aggregation import Aggregation
			self._aggregation = Aggregation(self._core, self._base)
		return self._aggregation

	@property
	def stbCoding(self):
		"""stbCoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stbCoding'):
			from .Htsig_.StbCoding import StbCoding
			self._stbCoding = StbCoding(self._core, self._base)
		return self._stbCoding

	@property
	def fecCoding(self):
		"""fecCoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fecCoding'):
			from .Htsig_.FecCoding import FecCoding
			self._fecCoding = FecCoding(self._core, self._base)
		return self._fecCoding

	@property
	def shortGi(self):
		"""shortGi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shortGi'):
			from .Htsig_.ShortGi import ShortGi
			self._shortGi = ShortGi(self._core, self._base)
		return self._shortGi

	@property
	def ness(self):
		"""ness commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ness'):
			from .Htsig_.Ness import Ness
			self._ness = Ness(self._core, self._base)
		return self._ness

	@property
	def crc(self):
		"""crc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .Htsig_.Crc import Crc
			self._crc = Crc(self._core, self._base)
		return self._crc

	@property
	def tail(self):
		"""tail commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tail'):
			from .Htsig_.Tail import Tail
			self._tail = Tail(self._core, self._base)
		return self._tail

	def clone(self) -> 'Htsig':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Htsig(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
