from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqConstant:
	"""IqConstant commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iqConstant", core, parent)

	@property
	def inphase(self):
		"""inphase commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_inphase'):
			from .IqConstant_.Inphase import Inphase
			self._inphase = Inphase(self._core, self._base)
		return self._inphase

	@property
	def quadrature(self):
		"""quadrature commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_quadrature'):
			from .IqConstant_.Quadrature import Quadrature
			self._quadrature = Quadrature(self._core, self._base)
		return self._quadrature

	def clone(self) -> 'IqConstant':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqConstant(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
