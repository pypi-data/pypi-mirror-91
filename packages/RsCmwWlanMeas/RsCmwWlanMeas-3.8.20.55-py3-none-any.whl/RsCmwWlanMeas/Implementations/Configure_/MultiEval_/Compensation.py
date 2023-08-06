from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Compensation:
	"""Compensation commands group definition. 6 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("compensation", core, parent)

	@property
	def tracking(self):
		"""tracking commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_tracking'):
			from .Compensation_.Tracking import Tracking
			self._tracking = Tracking(self._core, self._base)
		return self._tracking

	# noinspection PyTypeChecker
	def get_cestimation(self) -> enums.ChannelEstimation:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:CESTimation \n
		Snippet: value: enums.ChannelEstimation = driver.configure.multiEval.compensation.get_cestimation() \n
		Specifies whether channel estimation is done in payload or preamble. \n
			:return: channel_est: PAYLoad | PREamble PAYLoad: Channel estimation in payload and preamble PREamble: Channel estimation in preamble only
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:CESTimation?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelEstimation)

	def set_cestimation(self, channel_est: enums.ChannelEstimation) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:CESTimation \n
		Snippet: driver.configure.multiEval.compensation.set_cestimation(channel_est = enums.ChannelEstimation.PAYLoad) \n
		Specifies whether channel estimation is done in payload or preamble. \n
			:param channel_est: PAYLoad | PREamble PAYLoad: Channel estimation in payload and preamble PREamble: Channel estimation in preamble only
		"""
		param = Conversions.enum_scalar_to_str(channel_est, enums.ChannelEstimation)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:CESTimation {param}')

	# noinspection PyTypeChecker
	class EfTapsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Equalizer_Filter_Taps_Enable: bool: No parameter help available
			- Equalizer_Filter_Taps_Value: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Equalizer_Filter_Taps_Enable'),
			ArgStruct.scalar_int('Equalizer_Filter_Taps_Value')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Equalizer_Filter_Taps_Enable: bool = None
			self.Equalizer_Filter_Taps_Value: int = None

	def get_ef_taps(self) -> EfTapsStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:EFTaps \n
		Snippet: value: EfTapsStruct = driver.configure.multiEval.compensation.get_ef_taps() \n
		This command is relevant for DSSS signals only. It determines if and how accurate the transmit filter is estimated. \n
			:return: structure: for return value, see the help for EfTapsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:EFTaps?', self.__class__.EfTapsStruct())

	def set_ef_taps(self, value: EfTapsStruct) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:EFTaps \n
		Snippet: driver.configure.multiEval.compensation.set_ef_taps(value = EfTapsStruct()) \n
		This command is relevant for DSSS signals only. It determines if and how accurate the transmit filter is estimated. \n
			:param value: see the help for EfTapsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:EFTaps', value)

	# noinspection PyTypeChecker
	class SkipSymbolsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Skip_Symbols_Head: int: decimal Number of heading symbols to be skipped Range: 0 Sym to 100 Sym, Unit: symbol
			- Skip_Symbols_Tail: int: decimal Number of tailing symbols to be skipped Range: 0 Sym to 100 Sym, Unit: symbol"""
		__meta_args_list = [
			ArgStruct.scalar_int('Skip_Symbols_Head'),
			ArgStruct.scalar_int('Skip_Symbols_Tail')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Skip_Symbols_Head: int = None
			self.Skip_Symbols_Tail: int = None

	def get_skip_symbols(self) -> SkipSymbolsStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:SKIPsymbols \n
		Snippet: value: SkipSymbolsStruct = driver.configure.multiEval.compensation.get_skip_symbols() \n
		Defines how many head and tail symbols are excluded from OFDM modulation measurements. \n
			:return: structure: for return value, see the help for SkipSymbolsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:SKIPsymbols?', self.__class__.SkipSymbolsStruct())

	def set_skip_symbols(self, value: SkipSymbolsStruct) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:SKIPsymbols \n
		Snippet: driver.configure.multiEval.compensation.set_skip_symbols(value = SkipSymbolsStruct()) \n
		Defines how many head and tail symbols are excluded from OFDM modulation measurements. \n
			:param value: see the help for SkipSymbolsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:COMPensation:SKIPsymbols', value)

	def clone(self) -> 'Compensation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Compensation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
