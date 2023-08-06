from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VhtSig:
	"""VhtSig commands group definition. 15 total commands, 15 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vhtSig", core, parent)

	@property
	def bw(self):
		"""bw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .VhtSig_.Bw import Bw
			self._bw = Bw(self._core, self._base)
		return self._bw

	@property
	def reserved(self):
		"""reserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reserved'):
			from .VhtSig_.Reserved import Reserved
			self._reserved = Reserved(self._core, self._base)
		return self._reserved

	@property
	def stbc(self):
		"""stbc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stbc'):
			from .VhtSig_.Stbc import Stbc
			self._stbc = Stbc(self._core, self._base)
		return self._stbc

	@property
	def gid(self):
		"""gid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gid'):
			from .VhtSig_.Gid import Gid
			self._gid = Gid(self._core, self._base)
		return self._gid

	@property
	def sunsts(self):
		"""sunsts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sunsts'):
			from .VhtSig_.Sunsts import Sunsts
			self._sunsts = Sunsts(self._core, self._base)
		return self._sunsts

	@property
	def paid(self):
		"""paid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paid'):
			from .VhtSig_.Paid import Paid
			self._paid = Paid(self._core, self._base)
		return self._paid

	@property
	def txOp(self):
		"""txOp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txOp'):
			from .VhtSig_.TxOp import TxOp
			self._txOp = TxOp(self._core, self._base)
		return self._txOp

	@property
	def sgi(self):
		"""sgi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgi'):
			from .VhtSig_.Sgi import Sgi
			self._sgi = Sgi(self._core, self._base)
		return self._sgi

	@property
	def sdisambiguity(self):
		"""sdisambiguity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sdisambiguity'):
			from .VhtSig_.Sdisambiguity import Sdisambiguity
			self._sdisambiguity = Sdisambiguity(self._core, self._base)
		return self._sdisambiguity

	@property
	def fecCoding(self):
		"""fecCoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fecCoding'):
			from .VhtSig_.FecCoding import FecCoding
			self._fecCoding = FecCoding(self._core, self._base)
		return self._fecCoding

	@property
	def ldpc(self):
		"""ldpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ldpc'):
			from .VhtSig_.Ldpc import Ldpc
			self._ldpc = Ldpc(self._core, self._base)
		return self._ldpc

	@property
	def smcs(self):
		"""smcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smcs'):
			from .VhtSig_.Smcs import Smcs
			self._smcs = Smcs(self._core, self._base)
		return self._smcs

	@property
	def beamformed(self):
		"""beamformed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_beamformed'):
			from .VhtSig_.Beamformed import Beamformed
			self._beamformed = Beamformed(self._core, self._base)
		return self._beamformed

	@property
	def crc(self):
		"""crc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .VhtSig_.Crc import Crc
			self._crc = Crc(self._core, self._base)
		return self._crc

	@property
	def tail(self):
		"""tail commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tail'):
			from .VhtSig_.Tail import Tail
			self._tail = Tail(self._core, self._base)
		return self._tail

	def clone(self) -> 'VhtSig':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = VhtSig(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
