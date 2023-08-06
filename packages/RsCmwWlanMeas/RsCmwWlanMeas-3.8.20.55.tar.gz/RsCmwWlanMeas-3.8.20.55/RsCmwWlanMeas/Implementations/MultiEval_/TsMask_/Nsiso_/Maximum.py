from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	# noinspection PyTypeChecker
	class ReadStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: bool: No parameter help available
			- Ab_Max: float: No parameter help available
			- Bc_Max: float: No parameter help available
			- Cd_Max: float: No parameter help available
			- De_Max: float: No parameter help available
			- Ed_Max: float: No parameter help available
			- Dc_Max: float: No parameter help available
			- Cb_Max: float: No parameter help available
			- Ba_Max: float: No parameter help available
			- Out_Of_Tol: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Reliability'),
			ArgStruct.scalar_float('Ab_Max'),
			ArgStruct.scalar_float('Bc_Max'),
			ArgStruct.scalar_float('Cd_Max'),
			ArgStruct.scalar_float('De_Max'),
			ArgStruct.scalar_float('Ed_Max'),
			ArgStruct.scalar_float('Dc_Max'),
			ArgStruct.scalar_float('Cb_Max'),
			ArgStruct.scalar_float('Ba_Max'),
			ArgStruct.scalar_float('Out_Of_Tol')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: bool = None
			self.Ab_Max: float = None
			self.Bc_Max: float = None
			self.Cd_Max: float = None
			self.De_Max: float = None
			self.Ed_Max: float = None
			self.Dc_Max: float = None
			self.Cb_Max: float = None
			self.Ba_Max: float = None
			self.Out_Of_Tol: float = None

	def read(self) -> ReadStruct:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TSMask:NSISo:MAXimum \n
		Snippet: value: ReadStruct = driver.multiEval.tsMask.nsiso.maximum.read() \n
		No command help available \n
			:return: structure: for return value, see the help for ReadStruct structure arguments."""
		return self._core.io.query_struct(f'READ:WLAN:MEASurement<Instance>:MEValuation:TSMask:NSISo:MAXimum?', self.__class__.ReadStruct())

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Ab_Max: float: No parameter help available
			- Bc_Max: float: No parameter help available
			- Cd_Max: float: No parameter help available
			- De_Max: float: No parameter help available
			- Ed_Max: float: No parameter help available
			- Dc_Max: float: No parameter help available
			- Cb_Max: float: No parameter help available
			- Ba_Max: float: No parameter help available
			- Out_Of_Tol: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Ab_Max'),
			ArgStruct.scalar_float('Bc_Max'),
			ArgStruct.scalar_float('Cd_Max'),
			ArgStruct.scalar_float('De_Max'),
			ArgStruct.scalar_float('Ed_Max'),
			ArgStruct.scalar_float('Dc_Max'),
			ArgStruct.scalar_float('Cb_Max'),
			ArgStruct.scalar_float('Ba_Max'),
			ArgStruct.scalar_float('Out_Of_Tol')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Ab_Max: float = None
			self.Bc_Max: float = None
			self.Cd_Max: float = None
			self.De_Max: float = None
			self.Ed_Max: float = None
			self.Dc_Max: float = None
			self.Cb_Max: float = None
			self.Ba_Max: float = None
			self.Out_Of_Tol: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TSMask:NSISo:MAXimum \n
		Snippet: value: FetchStruct = driver.multiEval.tsMask.nsiso.maximum.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TSMask:NSISo:MAXimum?', self.__class__.FetchStruct())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Ab_Max: enums.ResultStatus2: No parameter help available
			- Bc_Max: enums.ResultStatus2: No parameter help available
			- Cd_Max: enums.ResultStatus2: No parameter help available
			- De_Max: enums.ResultStatus2: No parameter help available
			- Ed_Max: enums.ResultStatus2: No parameter help available
			- Dc_Max: enums.ResultStatus2: No parameter help available
			- Cb_Max: enums.ResultStatus2: No parameter help available
			- Ba_Max: enums.ResultStatus2: No parameter help available
			- Out_Of_Tol: enums.ResultStatus2: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Ab_Max', enums.ResultStatus2),
			ArgStruct.scalar_enum('Bc_Max', enums.ResultStatus2),
			ArgStruct.scalar_enum('Cd_Max', enums.ResultStatus2),
			ArgStruct.scalar_enum('De_Max', enums.ResultStatus2),
			ArgStruct.scalar_enum('Ed_Max', enums.ResultStatus2),
			ArgStruct.scalar_enum('Dc_Max', enums.ResultStatus2),
			ArgStruct.scalar_enum('Cb_Max', enums.ResultStatus2),
			ArgStruct.scalar_enum('Ba_Max', enums.ResultStatus2),
			ArgStruct.scalar_enum('Out_Of_Tol', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Ab_Max: enums.ResultStatus2 = None
			self.Bc_Max: enums.ResultStatus2 = None
			self.Cd_Max: enums.ResultStatus2 = None
			self.De_Max: enums.ResultStatus2 = None
			self.Ed_Max: enums.ResultStatus2 = None
			self.Dc_Max: enums.ResultStatus2 = None
			self.Cb_Max: enums.ResultStatus2 = None
			self.Ba_Max: enums.ResultStatus2 = None
			self.Out_Of_Tol: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:WLAN:MEASurement<Instance>:MEValuation:TSMask:NSISo:MAXimum \n
		Snippet: value: CalculateStruct = driver.multiEval.tsMask.nsiso.maximum.calculate() \n
		No command help available \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:WLAN:MEASurement<Instance>:MEValuation:TSMask:NSISo:MAXimum?', self.__class__.CalculateStruct())
