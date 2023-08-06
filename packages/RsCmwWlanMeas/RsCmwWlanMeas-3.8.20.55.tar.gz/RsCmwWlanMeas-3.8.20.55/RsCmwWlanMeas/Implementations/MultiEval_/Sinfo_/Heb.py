from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Heb:
	"""Heb commands group definition. 14 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("heb", core, parent)

	@property
	def channel(self):
		"""channel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Heb_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	def clone(self) -> 'Heb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Heb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
