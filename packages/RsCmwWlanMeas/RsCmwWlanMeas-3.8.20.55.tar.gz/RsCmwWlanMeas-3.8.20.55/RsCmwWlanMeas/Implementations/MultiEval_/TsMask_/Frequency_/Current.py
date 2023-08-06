from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for spectrum emission measurements exceeding the specified transmit spectrum mask limits. Range: 0 % to 100 % , Unit: %
			- Margin_Xvals: List[float]: float Comma-separated list of frequencies, one value per margin The number of margins equals the number of spectrum mask areas and depends on the selected standard, see Table 'Spectrum mask areas'. Range: -40 MHz to 40 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct('Margin_Xvals', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Margin_Xvals: List[float] = None

	def read(self) -> ResultData:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TSMask:FREQuency:CURRent \n
		Snippet: value: ResultData = driver.multiEval.tsMask.frequency.current.read() \n
		Return the X-positions of the limit line margins of the transmit spectrum mask, for MIMO measurements, antenna/stream
		number <n>, bandwidths with one segment. Positions for the current, average, minimum and maximum traces are returned. The
		values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:WLAN:MEASurement<Instance>:MEValuation:TSMask:FREQuency:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TSMask:FREQuency:CURRent \n
		Snippet: value: ResultData = driver.multiEval.tsMask.frequency.current.fetch() \n
		Return the X-positions of the limit line margins of the transmit spectrum mask, for MIMO measurements, antenna/stream
		number <n>, bandwidths with one segment. Positions for the current, average, minimum and maximum traces are returned. The
		values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TSMask:FREQuency:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: enums.ResultStatus2: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for spectrum emission measurements exceeding the specified transmit spectrum mask limits. Range: 0 % to 100 % , Unit: %
			- Margin_Xvals: List[enums.ResultStatus2]: float Comma-separated list of frequencies, one value per margin The number of margins equals the number of spectrum mask areas and depends on the selected standard, see Table 'Spectrum mask areas'. Range: -40 MHz to 40 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Out_Of_Tol', enums.ResultStatus2),
			ArgStruct('Margin_Xvals', DataType.EnumList, enums.ResultStatus2, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: enums.ResultStatus2 = None
			self.Margin_Xvals: List[enums.ResultStatus2] = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:WLAN:MEASurement<Instance>:MEValuation:TSMask:FREQuency:CURRent \n
		Snippet: value: CalculateStruct = driver.multiEval.tsMask.frequency.current.calculate() \n
		Return the X-positions of the limit line margins of the transmit spectrum mask, for MIMO measurements, antenna/stream
		number <n>, bandwidths with one segment. Positions for the current, average, minimum and maximum traces are returned. The
		values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:WLAN:MEASurement<Instance>:MEValuation:TSMask:FREQuency:CURRent?', self.__class__.CalculateStruct())
