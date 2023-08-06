from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standardDev", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Mcs_Index: int: No parameter help available
			- Pay_Load_Length: int: No parameter help available
			- Guard_Interval: enums.GuardInterval: No parameter help available
			- Burst_Power: float: No parameter help available
			- Evm_All_Carr: float: No parameter help available
			- Evm_Data_Carr: float: No parameter help available
			- Evm_Pilot_Carr: float: No parameter help available
			- Freq_Error: float: No parameter help available
			- Clock_Error: float: No parameter help available
			- Iq_Offset: float: No parameter help available
			- Out_Of_Tol: float: No parameter help available
			- Iq_Offset_8080: float: No parameter help available
			- Gain_Imbal: float: No parameter help available
			- Quad_Error: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Mcs_Index'),
			ArgStruct.scalar_int('Pay_Load_Length'),
			ArgStruct.scalar_enum('Guard_Interval', enums.GuardInterval),
			ArgStruct.scalar_float('Burst_Power'),
			ArgStruct.scalar_float('Evm_All_Carr'),
			ArgStruct.scalar_float('Evm_Data_Carr'),
			ArgStruct.scalar_float('Evm_Pilot_Carr'),
			ArgStruct.scalar_float('Freq_Error'),
			ArgStruct.scalar_float('Clock_Error'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Iq_Offset_8080'),
			ArgStruct.scalar_float('Gain_Imbal'),
			ArgStruct.scalar_float('Quad_Error')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Mcs_Index: int = None
			self.Pay_Load_Length: int = None
			self.Guard_Interval: enums.GuardInterval = None
			self.Burst_Power: float = None
			self.Evm_All_Carr: float = None
			self.Evm_Data_Carr: float = None
			self.Evm_Pilot_Carr: float = None
			self.Freq_Error: float = None
			self.Clock_Error: float = None
			self.Iq_Offset: float = None
			self.Out_Of_Tol: float = None
			self.Iq_Offset_8080: float = None
			self.Gain_Imbal: float = None
			self.Quad_Error: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:MODulation:ACSiso:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.modulation.acsiso.standardDev.read() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:WLAN:MEASurement<Instance>:MEValuation:MODulation:ACSiso:SDEViation?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:MODulation:ACSiso:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.modulation.acsiso.standardDev.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:MODulation:ACSiso:SDEViation?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Mcs_Index: enums.ResultStatus2: No parameter help available
			- Pay_Load_Length: enums.ResultStatus2: No parameter help available
			- Guard_Interval: enums.ResultStatus2: No parameter help available
			- Burst_Power: enums.ResultStatus2: No parameter help available
			- Evm_All_Carr: enums.ResultStatus2: No parameter help available
			- Evm_Data_Carr: enums.ResultStatus2: No parameter help available
			- Evm_Pilot_Carr: enums.ResultStatus2: No parameter help available
			- Freq_Error: enums.ResultStatus2: No parameter help available
			- Clock_Error: enums.ResultStatus2: No parameter help available
			- Iq_Offset: enums.ResultStatus2: No parameter help available
			- Out_Of_Tol: enums.ResultStatus2: No parameter help available
			- Iq_Offset_8080: enums.ResultStatus2: No parameter help available
			- Gain_Imbal: enums.ResultStatus2: No parameter help available
			- Quad_Error: enums.ResultStatus2: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Mcs_Index', enums.ResultStatus2),
			ArgStruct.scalar_enum('Pay_Load_Length', enums.ResultStatus2),
			ArgStruct.scalar_enum('Guard_Interval', enums.ResultStatus2),
			ArgStruct.scalar_enum('Burst_Power', enums.ResultStatus2),
			ArgStruct.scalar_enum('Evm_All_Carr', enums.ResultStatus2),
			ArgStruct.scalar_enum('Evm_Data_Carr', enums.ResultStatus2),
			ArgStruct.scalar_enum('Evm_Pilot_Carr', enums.ResultStatus2),
			ArgStruct.scalar_enum('Freq_Error', enums.ResultStatus2),
			ArgStruct.scalar_enum('Clock_Error', enums.ResultStatus2),
			ArgStruct.scalar_enum('Iq_Offset', enums.ResultStatus2),
			ArgStruct.scalar_enum('Out_Of_Tol', enums.ResultStatus2),
			ArgStruct.scalar_enum('Iq_Offset_8080', enums.ResultStatus2),
			ArgStruct.scalar_enum('Gain_Imbal', enums.ResultStatus2),
			ArgStruct.scalar_enum('Quad_Error', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Mcs_Index: enums.ResultStatus2 = None
			self.Pay_Load_Length: enums.ResultStatus2 = None
			self.Guard_Interval: enums.ResultStatus2 = None
			self.Burst_Power: enums.ResultStatus2 = None
			self.Evm_All_Carr: enums.ResultStatus2 = None
			self.Evm_Data_Carr: enums.ResultStatus2 = None
			self.Evm_Pilot_Carr: enums.ResultStatus2 = None
			self.Freq_Error: enums.ResultStatus2 = None
			self.Clock_Error: enums.ResultStatus2 = None
			self.Iq_Offset: enums.ResultStatus2 = None
			self.Out_Of_Tol: enums.ResultStatus2 = None
			self.Iq_Offset_8080: enums.ResultStatus2 = None
			self.Gain_Imbal: enums.ResultStatus2 = None
			self.Quad_Error: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:WLAN:MEASurement<Instance>:MEValuation:MODulation:ACSiso:SDEViation \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.acsiso.standardDev.calculate() \n
		No command help available \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:WLAN:MEASurement<Instance>:MEValuation:MODulation:ACSiso:SDEViation?', self.__class__.CalculateStruct())
