from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerVsTime:
	"""PowerVsTime commands group definition. 36 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("powerVsTime", core, parent)

	@property
	def terror(self):
		"""terror commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_terror'):
			from .PowerVsTime_.Terror import Terror
			self._terror = Terror(self._core, self._base)
		return self._terror

	@property
	def risingEdge(self):
		"""risingEdge commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_risingEdge'):
			from .PowerVsTime_.RisingEdge import RisingEdge
			self._risingEdge = RisingEdge(self._core, self._base)
		return self._risingEdge

	@property
	def fallingEdge(self):
		"""fallingEdge commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_fallingEdge'):
			from .PowerVsTime_.FallingEdge import FallingEdge
			self._fallingEdge = FallingEdge(self._core, self._base)
		return self._fallingEdge

	@property
	def teDistribution(self):
		"""teDistribution commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_teDistribution'):
			from .PowerVsTime_.TeDistribution import TeDistribution
			self._teDistribution = TeDistribution(self._core, self._base)
		return self._teDistribution

	def clone(self) -> 'PowerVsTime':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PowerVsTime(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
