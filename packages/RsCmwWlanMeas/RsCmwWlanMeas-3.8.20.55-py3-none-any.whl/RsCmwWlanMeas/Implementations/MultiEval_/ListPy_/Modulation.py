from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 112 total commands, 17 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	@property
	def scount(self):
		"""scount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scount'):
			from .Modulation_.Scount import Scount
			self._scount = Scount(self._core, self._base)
		return self._scount

	@property
	def pbackoff(self):
		"""pbackoff commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pbackoff'):
			from .Modulation_.Pbackoff import Pbackoff
			self._pbackoff = Pbackoff(self._core, self._base)
		return self._pbackoff

	@property
	def bpower(self):
		"""bpower commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_bpower'):
			from .Modulation_.Bpower import Bpower
			self._bpower = Bpower(self._core, self._base)
		return self._bpower

	@property
	def ppower(self):
		"""ppower commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_ppower'):
			from .Modulation_.Ppower import Ppower
			self._ppower = Ppower(self._core, self._base)
		return self._ppower

	@property
	def cfactor(self):
		"""cfactor commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_cfactor'):
			from .Modulation_.Cfactor import Cfactor
			self._cfactor = Cfactor(self._core, self._base)
		return self._cfactor

	@property
	def evmAll(self):
		"""evmAll commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_evmAll'):
			from .Modulation_.EvmAll import EvmAll
			self._evmAll = EvmAll(self._core, self._base)
		return self._evmAll

	@property
	def evmData(self):
		"""evmData commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_evmData'):
			from .Modulation_.EvmData import EvmData
			self._evmData = EvmData(self._core, self._base)
		return self._evmData

	@property
	def evmPilot(self):
		"""evmPilot commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_evmPilot'):
			from .Modulation_.EvmPilot import EvmPilot
			self._evmPilot = EvmPilot(self._core, self._base)
		return self._evmPilot

	@property
	def cfError(self):
		"""cfError commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_cfError'):
			from .Modulation_.CfError import CfError
			self._cfError = CfError(self._core, self._base)
		return self._cfError

	@property
	def scError(self):
		"""scError commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_scError'):
			from .Modulation_.ScError import ScError
			self._scError = ScError(self._core, self._base)
		return self._scError

	@property
	def iqOffset(self):
		"""iqOffset commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqOffset'):
			from .Modulation_.IqOffset import IqOffset
			self._iqOffset = IqOffset(self._core, self._base)
		return self._iqOffset

	@property
	def dcPower(self):
		"""dcPower commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcPower'):
			from .Modulation_.DcPower import DcPower
			self._dcPower = DcPower(self._core, self._base)
		return self._dcPower

	@property
	def gimbalance(self):
		"""gimbalance commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_gimbalance'):
			from .Modulation_.Gimbalance import Gimbalance
			self._gimbalance = Gimbalance(self._core, self._base)
		return self._gimbalance

	@property
	def qerror(self):
		"""qerror commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_qerror'):
			from .Modulation_.Qerror import Qerror
			self._qerror = Qerror(self._core, self._base)
		return self._qerror

	@property
	def ltfPower(self):
		"""ltfPower commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_ltfPower'):
			from .Modulation_.LtfPower import LtfPower
			self._ltfPower = LtfPower(self._core, self._base)
		return self._ltfPower

	@property
	def dpower(self):
		"""dpower commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpower'):
			from .Modulation_.Dpower import Dpower
			self._dpower = Dpower(self._core, self._base)
		return self._dpower

	@property
	def dsss(self):
		"""dsss commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_dsss'):
			from .Modulation_.Dsss import Dsss
			self._dsss = Dsss(self._core, self._base)
		return self._dsss

	def clone(self) -> 'Modulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Modulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
