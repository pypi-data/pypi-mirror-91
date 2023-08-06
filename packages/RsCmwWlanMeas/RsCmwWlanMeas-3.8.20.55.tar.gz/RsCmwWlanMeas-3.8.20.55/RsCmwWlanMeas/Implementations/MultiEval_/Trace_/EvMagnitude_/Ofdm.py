from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ofdm:
	"""Ofdm commands group definition. 12 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ofdm", core, parent)

	@property
	def carrier(self):
		"""carrier commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_carrier'):
			from .Ofdm_.Carrier import Carrier
			self._carrier = Carrier(self._core, self._base)
		return self._carrier

	@property
	def symbol(self):
		"""symbol commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_symbol'):
			from .Ofdm_.Symbol import Symbol
			self._symbol = Symbol(self._core, self._base)
		return self._symbol

	def clone(self) -> 'Ofdm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ofdm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
