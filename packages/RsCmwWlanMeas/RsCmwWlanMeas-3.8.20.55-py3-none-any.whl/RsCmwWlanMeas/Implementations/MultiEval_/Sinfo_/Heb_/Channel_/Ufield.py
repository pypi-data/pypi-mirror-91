from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ufield:
	"""Ufield commands group definition. 10 total commands, 10 Sub-groups, 0 group commands
	Repeated Capability: UserIx, default value after init: UserIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ufield", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_userIx_get', 'repcap_userIx_set', repcap.UserIx.Nr1)

	def repcap_userIx_set(self, enum_value: repcap.UserIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UserIx.Default
		Default value after init: UserIx.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_userIx_get(self) -> repcap.UserIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def staid(self):
		"""staid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_staid'):
			from .Ufield_.Staid import Staid
			self._staid = Staid(self._core, self._base)
		return self._staid

	@property
	def nsts(self):
		"""nsts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsts'):
			from .Ufield_.Nsts import Nsts
			self._nsts = Nsts(self._core, self._base)
		return self._nsts

	@property
	def txBeamforming(self):
		"""txBeamforming commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txBeamforming'):
			from .Ufield_.TxBeamforming import TxBeamforming
			self._txBeamforming = TxBeamforming(self._core, self._base)
		return self._txBeamforming

	@property
	def spaConfig(self):
		"""spaConfig commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spaConfig'):
			from .Ufield_.SpaConfig import SpaConfig
			self._spaConfig = SpaConfig(self._core, self._base)
		return self._spaConfig

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Ufield_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def dcm(self):
		"""dcm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcm'):
			from .Ufield_.Dcm import Dcm
			self._dcm = Dcm(self._core, self._base)
		return self._dcm

	@property
	def reserved(self):
		"""reserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reserved'):
			from .Ufield_.Reserved import Reserved
			self._reserved = Reserved(self._core, self._base)
		return self._reserved

	@property
	def coding(self):
		"""coding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coding'):
			from .Ufield_.Coding import Coding
			self._coding = Coding(self._core, self._base)
		return self._coding

	@property
	def crc(self):
		"""crc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .Ufield_.Crc import Crc
			self._crc = Crc(self._core, self._base)
		return self._crc

	@property
	def tail(self):
		"""tail commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tail'):
			from .Ufield_.Tail import Tail
			self._tail = Tail(self._core, self._base)
		return self._tail

	def clone(self) -> 'Ufield':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ufield(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
