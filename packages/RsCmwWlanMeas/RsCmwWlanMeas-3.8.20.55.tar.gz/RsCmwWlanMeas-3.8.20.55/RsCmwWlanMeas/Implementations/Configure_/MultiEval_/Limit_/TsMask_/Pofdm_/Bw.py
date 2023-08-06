from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bw:
	"""Bw commands group definition. 22 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bw", core, parent)
		
		self._base.multi_repcap_types = "BandwidthB,BandwidthA"

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Bw_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def ca(self):
		"""ca commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ca'):
			from .Bw_.Ca import Ca
			self._ca = Ca(self._core, self._base)
		return self._ca

	@property
	def cb(self):
		"""cb commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cb'):
			from .Bw_.Cb import Cb
			self._cb = Cb(self._core, self._base)
		return self._cb

	@property
	def userDefined(self):
		"""userDefined commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_userDefined'):
			from .Bw_.UserDefined import UserDefined
			self._userDefined = UserDefined(self._core, self._base)
		return self._userDefined

	@property
	def absolute(self):
		"""absolute commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_absolute'):
			from .Bw_.Absolute import Absolute
			self._absolute = Absolute(self._core, self._base)
		return self._absolute

	def clone(self) -> 'Bw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
