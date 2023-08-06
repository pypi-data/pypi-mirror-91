from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hemu:
	"""Hemu commands group definition. 19 total commands, 19 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hemu", core, parent)

	@property
	def ulDl(self):
		"""ulDl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulDl'):
			from .Hemu_.UlDl import UlDl
			self._ulDl = UlDl(self._core, self._base)
		return self._ulDl

	@property
	def bmcs(self):
		"""bmcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmcs'):
			from .Hemu_.Bmcs import Bmcs
			self._bmcs = Bmcs(self._core, self._base)
		return self._bmcs

	@property
	def bdcm(self):
		"""bdcm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bdcm'):
			from .Hemu_.Bdcm import Bdcm
			self._bdcm = Bdcm(self._core, self._base)
		return self._bdcm

	@property
	def bssColor(self):
		"""bssColor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bssColor'):
			from .Hemu_.BssColor import BssColor
			self._bssColor = BssColor(self._core, self._base)
		return self._bssColor

	@property
	def spatialReuse(self):
		"""spatialReuse commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spatialReuse'):
			from .Hemu_.SpatialReuse import SpatialReuse
			self._spatialReuse = SpatialReuse(self._core, self._base)
		return self._spatialReuse

	@property
	def bw(self):
		"""bw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .Hemu_.Bw import Bw
			self._bw = Bw(self._core, self._base)
		return self._bw

	@property
	def nsbSymbols(self):
		"""nsbSymbols commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsbSymbols'):
			from .Hemu_.NsbSymbols import NsbSymbols
			self._nsbSymbols = NsbSymbols(self._core, self._base)
		return self._nsbSymbols

	@property
	def sbCompress(self):
		"""sbCompress commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sbCompress'):
			from .Hemu_.SbCompress import SbCompress
			self._sbCompress = SbCompress(self._core, self._base)
		return self._sbCompress

	@property
	def giltfSize(self):
		"""giltfSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_giltfSize'):
			from .Hemu_.GiltfSize import GiltfSize
			self._giltfSize = GiltfSize(self._core, self._base)
		return self._giltfSize

	@property
	def doppler(self):
		"""doppler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_doppler'):
			from .Hemu_.Doppler import Doppler
			self._doppler = Doppler(self._core, self._base)
		return self._doppler

	@property
	def txOp(self):
		"""txOp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txOp'):
			from .Hemu_.TxOp import TxOp
			self._txOp = TxOp(self._core, self._base)
		return self._txOp

	@property
	def reserved(self):
		"""reserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reserved'):
			from .Hemu_.Reserved import Reserved
			self._reserved = Reserved(self._core, self._base)
		return self._reserved

	@property
	def nltfSymbols(self):
		"""nltfSymbols commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nltfSymbols'):
			from .Hemu_.NltfSymbols import NltfSymbols
			self._nltfSymbols = NltfSymbols(self._core, self._base)
		return self._nltfSymbols

	@property
	def ldpc(self):
		"""ldpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ldpc'):
			from .Hemu_.Ldpc import Ldpc
			self._ldpc = Ldpc(self._core, self._base)
		return self._ldpc

	@property
	def stbc(self):
		"""stbc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stbc'):
			from .Hemu_.Stbc import Stbc
			self._stbc = Stbc(self._core, self._base)
		return self._stbc

	@property
	def pfecPadding(self):
		"""pfecPadding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfecPadding'):
			from .Hemu_.PfecPadding import PfecPadding
			self._pfecPadding = PfecPadding(self._core, self._base)
		return self._pfecPadding

	@property
	def peDisambiguity(self):
		"""peDisambiguity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_peDisambiguity'):
			from .Hemu_.PeDisambiguity import PeDisambiguity
			self._peDisambiguity = PeDisambiguity(self._core, self._base)
		return self._peDisambiguity

	@property
	def crc(self):
		"""crc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .Hemu_.Crc import Crc
			self._crc = Crc(self._core, self._base)
		return self._crc

	@property
	def tail(self):
		"""tail commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tail'):
			from .Hemu_.Tail import Tail
			self._tail = Tail(self._core, self._base)
		return self._tail

	def clone(self) -> 'Hemu':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hemu(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
