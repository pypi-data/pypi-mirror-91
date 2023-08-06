from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Obw:
	"""Obw commands group definition. 8 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("obw", core, parent)

	@property
	def segments(self):
		"""segments commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_segments'):
			from .Obw_.Segments import Segments
			self._segments = Segments(self._core, self._base)
		return self._segments

	@property
	def mimo(self):
		"""mimo commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_mimo'):
			from .Obw_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Obw_Values: List[float]: No parameter help available
			- Obw_Lr: List[float]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Obw_Values', DataType.FloatList, None, False, False, 4),
			ArgStruct('Obw_Lr', DataType.FloatList, None, False, False, 2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Obw_Values: List[float] = None
			self.Obw_Lr: List[float] = None

	def read(self) -> ResultData:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TSMask:OBW \n
		Snippet: value: ResultData = driver.multiEval.tsMask.obw.read() \n
		Return the OBW results for SISO measurements and bandwidths with one segment. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:WLAN:MEASurement<Instance>:MEValuation:TSMask:OBW?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TSMask:OBW \n
		Snippet: value: ResultData = driver.multiEval.tsMask.obw.fetch() \n
		Return the OBW results for SISO measurements and bandwidths with one segment. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TSMask:OBW?', self.__class__.ResultData())

	def clone(self) -> 'Obw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Obw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
