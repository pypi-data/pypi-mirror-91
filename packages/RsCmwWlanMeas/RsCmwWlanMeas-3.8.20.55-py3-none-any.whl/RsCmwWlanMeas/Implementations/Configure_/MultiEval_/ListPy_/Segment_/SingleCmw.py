from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SingleCmw:
	"""SingleCmw commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("singleCmw", core, parent)

	@property
	def connector(self):
		"""connector commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connector'):
			from .SingleCmw_.Connector import Connector
			self._connector = Connector(self._core, self._base)
		return self._connector

	def clone(self) -> 'SingleCmw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SingleCmw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
