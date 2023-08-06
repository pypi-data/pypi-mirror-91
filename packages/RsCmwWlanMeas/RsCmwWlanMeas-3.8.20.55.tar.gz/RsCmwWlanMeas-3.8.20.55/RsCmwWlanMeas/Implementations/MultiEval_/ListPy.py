from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 132 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	@property
	def sreliability(self):
		"""sreliability commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sreliability'):
			from .ListPy_.Sreliability import Sreliability
			self._sreliability = Sreliability(self._core, self._base)
		return self._sreliability

	@property
	def modulation(self):
		"""modulation commands group. 17 Sub-classes, 0 commands."""
		if not hasattr(self, '_modulation'):
			from .ListPy_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def segment(self):
		"""segment commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_segment'):
			from .ListPy_.Segment import Segment
			self._segment = Segment(self._core, self._base)
		return self._segment

	@property
	def tsMask(self):
		"""tsMask commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsMask'):
			from .ListPy_.TsMask import TsMask
			self._tsMask = TsMask(self._core, self._base)
		return self._tsMask

	def clone(self) -> 'ListPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ListPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
