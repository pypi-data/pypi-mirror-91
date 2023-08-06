from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ofdma:
	"""Ofdma commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ofdma", core, parent)

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Ofdma_.Info import Info
			self._info = Info(self._core, self._base)
		return self._info

	@property
	def uinfo(self):
		"""uinfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uinfo'):
			from .Ofdma_.Uinfo import Uinfo
			self._uinfo = Uinfo(self._core, self._base)
		return self._uinfo

	def clone(self) -> 'Ofdma':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ofdma(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
