from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


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
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for spectrum emission measurements exceeding the specified transmit spectrum mask limits. Unit: %
			- Margin: List[float]: float Comma-separated list of margin values, one value per spectrum mask area The number of margin values depends on the selected standard, see Table 'Spectrum mask areas'. Range: -100 dB to 100 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct('Margin', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Margin: List[float] = None

	def read(self) -> ResultData:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TSMask:CURRent \n
		Snippet: value: ResultData = driver.multiEval.tsMask.current.read() \n
		Return the limit line margin values of the transmit spectrum mask for SISO measurements and bandwidths with one segment.
		Margins for the current, average, minimum and maximum traces are returned. A positive result indicates that the trace is
		located above the limit line. The limit is exceeded. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:WLAN:MEASurement<Instance>:MEValuation:TSMask:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TSMask:CURRent \n
		Snippet: value: ResultData = driver.multiEval.tsMask.current.fetch() \n
		Return the limit line margin values of the transmit spectrum mask for SISO measurements and bandwidths with one segment.
		Margins for the current, average, minimum and maximum traces are returned. A positive result indicates that the trace is
		located above the limit line. The limit is exceeded. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TSMask:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: enums.ResultStatus2: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for spectrum emission measurements exceeding the specified transmit spectrum mask limits. Unit: %
			- Margin: List[enums.ResultStatus2]: float Comma-separated list of margin values, one value per spectrum mask area The number of margin values depends on the selected standard, see Table 'Spectrum mask areas'. Range: -100 dB to 100 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Out_Of_Tol', enums.ResultStatus2),
			ArgStruct('Margin', DataType.EnumList, enums.ResultStatus2, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: enums.ResultStatus2 = None
			self.Margin: List[enums.ResultStatus2] = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:WLAN:MEASurement<Instance>:MEValuation:TSMask:CURRent \n
		Snippet: value: CalculateStruct = driver.multiEval.tsMask.current.calculate() \n
		Return the limit line margin values of the transmit spectrum mask for SISO measurements and bandwidths with one segment.
		Margins for the current, average, minimum and maximum traces are returned. A positive result indicates that the trace is
		located above the limit line. The limit is exceeded. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:WLAN:MEASurement<Instance>:MEValuation:TSMask:CURRent?', self.__class__.CalculateStruct())
