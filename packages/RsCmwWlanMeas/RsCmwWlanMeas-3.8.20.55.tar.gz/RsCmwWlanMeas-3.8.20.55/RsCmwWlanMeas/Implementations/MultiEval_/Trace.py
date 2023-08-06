from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trace:
	"""Trace commands group definition. 302 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trace", core, parent)

	@property
	def tsMask(self):
		"""tsMask commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsMask'):
			from .Trace_.TsMask import TsMask
			self._tsMask = TsMask(self._core, self._base)
		return self._tsMask

	@property
	def cfError(self):
		"""cfError commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_cfError'):
			from .Trace_.CfError import CfError
			self._cfError = CfError(self._core, self._base)
		return self._cfError

	@property
	def terror(self):
		"""terror commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_terror'):
			from .Trace_.Terror import Terror
			self._terror = Terror(self._core, self._base)
		return self._terror

	@property
	def spectrFlatness(self):
		"""spectrFlatness commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_spectrFlatness'):
			from .Trace_.SpectrFlatness import SpectrFlatness
			self._spectrFlatness = SpectrFlatness(self._core, self._base)
		return self._spectrFlatness

	@property
	def iqConstant(self):
		"""iqConstant commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqConstant'):
			from .Trace_.IqConstant import IqConstant
			self._iqConstant = IqConstant(self._core, self._base)
		return self._iqConstant

	@property
	def evMagnitude(self):
		"""evMagnitude commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_evMagnitude'):
			from .Trace_.EvMagnitude import EvMagnitude
			self._evMagnitude = EvMagnitude(self._core, self._base)
		return self._evMagnitude

	@property
	def powerVsTime(self):
		"""powerVsTime commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_powerVsTime'):
			from .Trace_.PowerVsTime import PowerVsTime
			self._powerVsTime = PowerVsTime(self._core, self._base)
		return self._powerVsTime

	def clone(self) -> 'Trace':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trace(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
