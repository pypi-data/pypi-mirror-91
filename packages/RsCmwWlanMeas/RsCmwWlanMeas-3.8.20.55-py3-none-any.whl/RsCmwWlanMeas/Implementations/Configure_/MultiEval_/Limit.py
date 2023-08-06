from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 105 total commands, 4 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("limit", core, parent)

	@property
	def spectrFlatness(self):
		"""spectrFlatness commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_spectrFlatness'):
			from .Limit_.SpectrFlatness import SpectrFlatness
			self._spectrFlatness = SpectrFlatness(self._core, self._base)
		return self._spectrFlatness

	@property
	def tsMask(self):
		"""tsMask commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsMask'):
			from .Limit_.TsMask import TsMask
			self._tsMask = TsMask(self._core, self._base)
		return self._tsMask

	@property
	def modulation(self):
		"""modulation commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_modulation'):
			from .Limit_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def powerVsTime(self):
		"""powerVsTime commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_powerVsTime'):
			from .Limit_.PowerVsTime import PowerVsTime
			self._powerVsTime = PowerVsTime(self._core, self._base)
		return self._powerVsTime

	# noinspection PyTypeChecker
	def get_ute_power(self) -> enums.LowHigh:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:MEValuation:LIMit:UTEPower \n
		Snippet: value: enums.LowHigh = driver.configure.multiEval.limit.get_ute_power() \n
		Sets the type of limits to be applied for the unused tone error of HE TB PPDU. \n
			:return: ute_power: HIGH | LOW HIGH: used limits are according to the transmit power larger than the maximum power of MCS 7 LOW: used limits are according to the transmit power less than or equal to the maximum power of MCS 7
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:UTEPower?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_ute_power(self, ute_power: enums.LowHigh) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:MEValuation:LIMit:UTEPower \n
		Snippet: driver.configure.multiEval.limit.set_ute_power(ute_power = enums.LowHigh.HIGH) \n
		Sets the type of limits to be applied for the unused tone error of HE TB PPDU. \n
			:param ute_power: HIGH | LOW HIGH: used limits are according to the transmit power larger than the maximum power of MCS 7 LOW: used limits are according to the transmit power less than or equal to the maximum power of MCS 7
		"""
		param = Conversions.enum_scalar_to_str(ute_power, enums.LowHigh)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:UTEPower {param}')

	def get_ut_error(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:MEValuation:LIMit:UTERror \n
		Snippet: value: bool = driver.configure.multiEval.limit.get_ut_error() \n
		Enables/ disables an upper limit for the unused tone error of HE TB PPDU. \n
			:return: ute_limits: ON | OFF
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:UTERror?')
		return Conversions.str_to_bool(response)

	def set_ut_error(self, ute_limits: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:MEValuation:LIMit:UTERror \n
		Snippet: driver.configure.multiEval.limit.set_ut_error(ute_limits = False) \n
		Enables/ disables an upper limit for the unused tone error of HE TB PPDU. \n
			:param ute_limits: ON | OFF
		"""
		param = Conversions.bool_to_str(ute_limits)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:UTERror {param}')

	def clone(self) -> 'Limit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Limit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
