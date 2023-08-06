from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HeOfdm:
	"""HeOfdm commands group definition. 11 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("heOfdm", core, parent)

	@property
	def evmAll(self):
		"""evmAll commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_evmAll'):
			from .HeOfdm_.EvmAll import EvmAll
			self._evmAll = EvmAll(self._core, self._base)
		return self._evmAll

	@property
	def evmPilot(self):
		"""evmPilot commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_evmPilot'):
			from .HeOfdm_.EvmPilot import EvmPilot
			self._evmPilot = EvmPilot(self._core, self._base)
		return self._evmPilot

	@property
	def iqOffset(self):
		"""iqOffset commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqOffset'):
			from .HeOfdm_.IqOffset import IqOffset
			self._iqOffset = IqOffset(self._core, self._base)
		return self._iqOffset

	def get_cf_error(self) -> float or bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:CFERror \n
		Snippet: value: float or bool = driver.configure.multiEval.limit.modulation.heOfdm.get_cf_error() \n
		Defines and activates an upper limit for the center frequency error in 802.11ax signals. \n
			:return: center_freq_error: numeric | ON | OFF Range: 0 Hz to 100 MHz, Unit: Hz Additional parameters: OFF | ON (disables | enables the limit check)
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:CFERror?')
		return Conversions.str_to_float_or_bool(response)

	def set_cf_error(self, center_freq_error: float or bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:CFERror \n
		Snippet: driver.configure.multiEval.limit.modulation.heOfdm.set_cf_error(center_freq_error = 1.0) \n
		Defines and activates an upper limit for the center frequency error in 802.11ax signals. \n
			:param center_freq_error: numeric | ON | OFF Range: 0 Hz to 100 MHz, Unit: Hz Additional parameters: OFF | ON (disables | enables the limit check)
		"""
		param = Conversions.decimal_or_bool_value_to_str(center_freq_error)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:CFERror {param}')

	def get_sc_error(self) -> float or bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:SCERror \n
		Snippet: value: float or bool = driver.configure.multiEval.limit.modulation.heOfdm.get_sc_error() \n
		Defines and activates an upper limit for the symbol clock error in 802.11ax signals. \n
			:return: clock_error: numeric | ON | OFF Range: 0 ppm to 100 ppm, Unit: ppm Additional parameters: OFF | ON (disables | enables the limit check)
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:SCERror?')
		return Conversions.str_to_float_or_bool(response)

	def set_sc_error(self, clock_error: float or bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:SCERror \n
		Snippet: driver.configure.multiEval.limit.modulation.heOfdm.set_sc_error(clock_error = 1.0) \n
		Defines and activates an upper limit for the symbol clock error in 802.11ax signals. \n
			:param clock_error: numeric | ON | OFF Range: 0 ppm to 100 ppm, Unit: ppm Additional parameters: OFF | ON (disables | enables the limit check)
		"""
		param = Conversions.decimal_or_bool_value_to_str(clock_error)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:SCERror {param}')

	# noinspection PyTypeChecker
	class CfoDistributionStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Cfo_Percentage: float or bool: numeric | ON | OFF Upper limit for the tolerated CFO errors (CFO exceeding the specified CFO_Frequency) Unit: % Additional parameters: OFF | ON (disables | enables the limit check)
			- Cfo_Frequency: float: numeric Border value defining CFO error Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Cfo_Percentage'),
			ArgStruct.scalar_float('Cfo_Frequency')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cfo_Percentage: float or bool = None
			self.Cfo_Frequency: float = None

	def get_cfo_distribution(self) -> CfoDistributionStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:CFDistrib \n
		Snippet: value: CfoDistributionStruct = driver.configure.multiEval.limit.modulation.heOfdm.get_cfo_distribution() \n
		Configure the limit of carrier frequency offset (CFO) error distribution for HE modulation measurements. Exceeding the
		limit has no impact on the stop 'On Limit Failure' condition or out-of-tolerance counter. \n
			:return: structure: for return value, see the help for CfoDistributionStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:CFDistrib?', self.__class__.CfoDistributionStruct())

	def set_cfo_distribution(self, value: CfoDistributionStruct) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:CFDistrib \n
		Snippet: driver.configure.multiEval.limit.modulation.heOfdm.set_cfo_distribution(value = CfoDistributionStruct()) \n
		Configure the limit of carrier frequency offset (CFO) error distribution for HE modulation measurements. Exceeding the
		limit has no impact on the stop 'On Limit Failure' condition or out-of-tolerance counter. \n
			:param value: see the help for CfoDistributionStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:MODulation:HEOFdm:CFDistrib', value)

	def clone(self) -> 'HeOfdm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HeOfdm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
