from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Y:
	"""Y commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("y", core, parent)

	@property
	def a(self):
		"""a commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_a'):
			from .Y_.A import A
			self._a = A(self._core, self._base)
		return self._a

	@property
	def b(self):
		"""b commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_b'):
			from .Y_.B import B
			self._b = B(self._core, self._base)
		return self._b

	@property
	def c(self):
		"""c commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_c'):
			from .Y_.C import C
			self._c = C(self._core, self._base)
		return self._c

	@property
	def d(self):
		"""d commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_d'):
			from .Y_.D import D
			self._d = D(self._core, self._base)
		return self._d

	@property
	def e(self):
		"""e commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e'):
			from .Y_.E import E
			self._e = E(self._core, self._base)
		return self._e

	def clone(self) -> 'Y':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Y(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
