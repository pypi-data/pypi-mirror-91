from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 203 total commands, 6 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	@property
	def smimo(self):
		"""smimo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smimo'):
			from .Configure_.Smimo import Smimo
			self._smimo = Smimo(self._core, self._base)
		return self._smimo

	@property
	def mimo(self):
		"""mimo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mimo'):
			from .Configure_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	@property
	def isignal(self):
		"""isignal commands group. 3 Sub-classes, 9 commands."""
		if not hasattr(self, '_isignal'):
			from .Configure_.Isignal import Isignal
			self._isignal = Isignal(self._core, self._base)
		return self._isignal

	@property
	def tmode(self):
		"""tmode commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmode'):
			from .Configure_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	@property
	def rfSettings(self):
		"""rfSettings commands group. 5 Sub-classes, 3 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Configure_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def multiEval(self):
		"""multiEval commands group. 9 Sub-classes, 7 commands."""
		if not hasattr(self, '_multiEval'):
			from .Configure_.MultiEval import MultiEval
			self._multiEval = MultiEval(self._core, self._base)
		return self._multiEval

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.TrainingMode:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MODE \n
		Snippet: value: enums.TrainingMode = driver.configure.get_mode() \n
		Switches between the measurement mode and the training mode. \n
			:return: training_mode: TMODe | MMODe TMODe: Activate the training mode MMODe: Activate the measurement mode
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TrainingMode)

	def set_mode(self, training_mode: enums.TrainingMode) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MODE \n
		Snippet: driver.configure.set_mode(training_mode = enums.TrainingMode.MMODe) \n
		Switches between the measurement mode and the training mode. \n
			:param training_mode: TMODe | MMODe TMODe: Activate the training mode MMODe: Activate the measurement mode
		"""
		param = Conversions.enum_scalar_to_str(training_mode, enums.TrainingMode)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MODE {param}')

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
