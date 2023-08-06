from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dsss:
	"""Dsss commands group definition. 40 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dsss", core, parent)

	@property
	def bpower(self):
		"""bpower commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_bpower'):
			from .Dsss_.Bpower import Bpower
			self._bpower = Bpower(self._core, self._base)
		return self._bpower

	@property
	def evmPeak(self):
		"""evmPeak commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_evmPeak'):
			from .Dsss_.EvmPeak import EvmPeak
			self._evmPeak = EvmPeak(self._core, self._base)
		return self._evmPeak

	@property
	def evmEms(self):
		"""evmEms commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_evmEms'):
			from .Dsss_.EvmEms import EvmEms
			self._evmEms = EvmEms(self._core, self._base)
		return self._evmEms

	@property
	def cfError(self):
		"""cfError commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_cfError'):
			from .Dsss_.CfError import CfError
			self._cfError = CfError(self._core, self._base)
		return self._cfError

	@property
	def ccError(self):
		"""ccError commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccError'):
			from .Dsss_.CcError import CcError
			self._ccError = CcError(self._core, self._base)
		return self._ccError

	@property
	def iqOffset(self):
		"""iqOffset commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqOffset'):
			from .Dsss_.IqOffset import IqOffset
			self._iqOffset = IqOffset(self._core, self._base)
		return self._iqOffset

	@property
	def gimbalance(self):
		"""gimbalance commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_gimbalance'):
			from .Dsss_.Gimbalance import Gimbalance
			self._gimbalance = Gimbalance(self._core, self._base)
		return self._gimbalance

	@property
	def qerror(self):
		"""qerror commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_qerror'):
			from .Dsss_.Qerror import Qerror
			self._qerror = Qerror(self._core, self._base)
		return self._qerror

	def clone(self) -> 'Dsss':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dsss(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
