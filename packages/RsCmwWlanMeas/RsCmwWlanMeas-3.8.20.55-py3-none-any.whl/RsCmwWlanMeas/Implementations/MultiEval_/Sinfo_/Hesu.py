from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hesu:
	"""Hesu commands group definition. 21 total commands, 21 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hesu", core, parent)

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .Hesu_.FormatPy import FormatPy
			self._formatPy = FormatPy(self._core, self._base)
		return self._formatPy

	@property
	def beamChange(self):
		"""beamChange commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_beamChange'):
			from .Hesu_.BeamChange import BeamChange
			self._beamChange = BeamChange(self._core, self._base)
		return self._beamChange

	@property
	def ulDl(self):
		"""ulDl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulDl'):
			from .Hesu_.UlDl import UlDl
			self._ulDl = UlDl(self._core, self._base)
		return self._ulDl

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Hesu_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def dcm(self):
		"""dcm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcm'):
			from .Hesu_.Dcm import Dcm
			self._dcm = Dcm(self._core, self._base)
		return self._dcm

	@property
	def bssColor(self):
		"""bssColor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bssColor'):
			from .Hesu_.BssColor import BssColor
			self._bssColor = BssColor(self._core, self._base)
		return self._bssColor

	@property
	def reserved(self):
		"""reserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reserved'):
			from .Hesu_.Reserved import Reserved
			self._reserved = Reserved(self._core, self._base)
		return self._reserved

	@property
	def spatialReuse(self):
		"""spatialReuse commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spatialReuse'):
			from .Hesu_.SpatialReuse import SpatialReuse
			self._spatialReuse = SpatialReuse(self._core, self._base)
		return self._spatialReuse

	@property
	def bw(self):
		"""bw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .Hesu_.Bw import Bw
			self._bw = Bw(self._core, self._base)
		return self._bw

	@property
	def giltfSize(self):
		"""giltfSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_giltfSize'):
			from .Hesu_.GiltfSize import GiltfSize
			self._giltfSize = GiltfSize(self._core, self._base)
		return self._giltfSize

	@property
	def nsts(self):
		"""nsts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsts'):
			from .Hesu_.Nsts import Nsts
			self._nsts = Nsts(self._core, self._base)
		return self._nsts

	@property
	def txOp(self):
		"""txOp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txOp'):
			from .Hesu_.TxOp import TxOp
			self._txOp = TxOp(self._core, self._base)
		return self._txOp

	@property
	def coding(self):
		"""coding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coding'):
			from .Hesu_.Coding import Coding
			self._coding = Coding(self._core, self._base)
		return self._coding

	@property
	def ldpc(self):
		"""ldpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ldpc'):
			from .Hesu_.Ldpc import Ldpc
			self._ldpc = Ldpc(self._core, self._base)
		return self._ldpc

	@property
	def stbc(self):
		"""stbc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stbc'):
			from .Hesu_.Stbc import Stbc
			self._stbc = Stbc(self._core, self._base)
		return self._stbc

	@property
	def txBf(self):
		"""txBf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txBf'):
			from .Hesu_.TxBf import TxBf
			self._txBf = TxBf(self._core, self._base)
		return self._txBf

	@property
	def pfecPadding(self):
		"""pfecPadding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfecPadding'):
			from .Hesu_.PfecPadding import PfecPadding
			self._pfecPadding = PfecPadding(self._core, self._base)
		return self._pfecPadding

	@property
	def peDisambiguity(self):
		"""peDisambiguity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_peDisambiguity'):
			from .Hesu_.PeDisambiguity import PeDisambiguity
			self._peDisambiguity = PeDisambiguity(self._core, self._base)
		return self._peDisambiguity

	@property
	def doppler(self):
		"""doppler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_doppler'):
			from .Hesu_.Doppler import Doppler
			self._doppler = Doppler(self._core, self._base)
		return self._doppler

	@property
	def crc(self):
		"""crc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .Hesu_.Crc import Crc
			self._crc = Crc(self._core, self._base)
		return self._crc

	@property
	def tail(self):
		"""tail commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tail'):
			from .Hesu_.Tail import Tail
			self._tail = Tail(self._core, self._base)
		return self._tail

	def clone(self) -> 'Hesu':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hesu(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
