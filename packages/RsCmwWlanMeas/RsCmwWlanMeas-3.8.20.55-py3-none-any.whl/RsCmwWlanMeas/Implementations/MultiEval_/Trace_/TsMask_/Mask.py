from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mask:
	"""Mask commands group definition. 8 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mask", core, parent)

	@property
	def mimo(self):
		"""mimo commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_mimo'):
			from .Mask_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	@property
	def segment(self):
		"""segment commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_segment'):
			from .Mask_.Segment import Segment
			self._segment = Segment(self._core, self._base)
		return self._segment

	def read(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:MASK \n
		Snippet: value: List[float] = driver.multiEval.trace.tsMask.mask.read(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the power values (Y-values) of the transmit spectrum mask limit line trace, for SISO measurements and bandwidths
		with one segment. For the optional query parameters <start>, <count> and <decimation>, see 'Trace Sub-Arrays'. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: spec_trace_mask: float Comma-separated list of power values, trace from left to right Unit: dB"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:MASK? {param}'.rstrip(), suppressed)
		return response

	def fetch(self, start: float = None, count: float = None, decimation: float = None) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:MASK \n
		Snippet: value: List[float] = driver.multiEval.trace.tsMask.mask.fetch(start = 1.0, count = 1.0, decimation = 1.0) \n
		Return the power values (Y-values) of the transmit spectrum mask limit line trace, for SISO measurements and bandwidths
		with one segment. For the optional query parameters <start>, <count> and <decimation>, see 'Trace Sub-Arrays'. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param start: No help available
			:param count: No help available
			:param decimation: No help available
			:return: spec_trace_mask: float Comma-separated list of power values, trace from left to right Unit: dB"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Float, True), ArgSingle('count', count, DataType.Float, True), ArgSingle('decimation', decimation, DataType.Float, True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:TSMask:MASK? {param}'.rstrip(), suppressed)
		return response

	def clone(self) -> 'Mask':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mask(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
