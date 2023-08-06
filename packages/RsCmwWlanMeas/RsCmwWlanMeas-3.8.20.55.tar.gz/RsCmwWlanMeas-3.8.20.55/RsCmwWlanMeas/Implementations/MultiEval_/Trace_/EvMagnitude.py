from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EvMagnitude:
	"""EvMagnitude commands group definition. 76 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("evMagnitude", core, parent)

	@property
	def dsss(self):
		"""dsss commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_dsss'):
			from .EvMagnitude_.Dsss import Dsss
			self._dsss = Dsss(self._core, self._base)
		return self._dsss

	@property
	def carrier(self):
		"""carrier commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_carrier'):
			from .EvMagnitude_.Carrier import Carrier
			self._carrier = Carrier(self._core, self._base)
		return self._carrier

	@property
	def symbol(self):
		"""symbol commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_symbol'):
			from .EvMagnitude_.Symbol import Symbol
			self._symbol = Symbol(self._core, self._base)
		return self._symbol

	@property
	def ofdm(self):
		"""ofdm commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ofdm'):
			from .EvMagnitude_.Ofdm import Ofdm
			self._ofdm = Ofdm(self._core, self._base)
		return self._ofdm

	@property
	def nsiso(self):
		"""nsiso commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_nsiso'):
			from .EvMagnitude_.Nsiso import Nsiso
			self._nsiso = Nsiso(self._core, self._base)
		return self._nsiso

	@property
	def acsiso(self):
		"""acsiso commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_acsiso'):
			from .EvMagnitude_.Acsiso import Acsiso
			self._acsiso = Acsiso(self._core, self._base)
		return self._acsiso

	def clone(self) -> 'EvMagnitude':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EvMagnitude(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
