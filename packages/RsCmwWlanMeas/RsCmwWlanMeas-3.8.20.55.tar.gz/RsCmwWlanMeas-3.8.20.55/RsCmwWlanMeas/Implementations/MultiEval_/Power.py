from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 12 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	@property
	def rxAntenna(self):
		"""rxAntenna commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_rxAntenna'):
			from .Power_.RxAntenna import RxAntenna
			self._rxAntenna = RxAntenna(self._core, self._base)
		return self._rxAntenna

	@property
	def runit(self):
		"""runit commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_runit'):
			from .Power_.Runit import Runit
			self._runit = Runit(self._core, self._base)
		return self._runit

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
