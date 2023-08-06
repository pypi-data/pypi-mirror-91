from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sinfo:
	"""Sinfo commands group definition. 95 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sinfo", core, parent)

	@property
	def lsig(self):
		"""lsig commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_lsig'):
			from .Sinfo_.Lsig import Lsig
			self._lsig = Lsig(self._core, self._base)
		return self._lsig

	@property
	def htsig(self):
		"""htsig commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_htsig'):
			from .Sinfo_.Htsig import Htsig
			self._htsig = Htsig(self._core, self._base)
		return self._htsig

	@property
	def vhtSig(self):
		"""vhtSig commands group. 15 Sub-classes, 0 commands."""
		if not hasattr(self, '_vhtSig'):
			from .Sinfo_.VhtSig import VhtSig
			self._vhtSig = VhtSig(self._core, self._base)
		return self._vhtSig

	@property
	def hesu(self):
		"""hesu commands group. 21 Sub-classes, 0 commands."""
		if not hasattr(self, '_hesu'):
			from .Sinfo_.Hesu import Hesu
			self._hesu = Hesu(self._core, self._base)
		return self._hesu

	@property
	def hemu(self):
		"""hemu commands group. 19 Sub-classes, 0 commands."""
		if not hasattr(self, '_hemu'):
			from .Sinfo_.Hemu import Hemu
			self._hemu = Hemu(self._core, self._base)
		return self._hemu

	@property
	def hetb(self):
		"""hetb commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_hetb'):
			from .Sinfo_.Hetb import Hetb
			self._hetb = Hetb(self._core, self._base)
		return self._hetb

	@property
	def heb(self):
		"""heb commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_heb'):
			from .Sinfo_.Heb import Heb
			self._heb = Heb(self._core, self._base)
		return self._heb

	def clone(self) -> 'Sinfo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sinfo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
