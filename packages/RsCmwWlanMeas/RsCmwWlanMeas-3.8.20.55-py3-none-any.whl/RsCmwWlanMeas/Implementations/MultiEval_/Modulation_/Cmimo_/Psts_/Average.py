from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<instance>:MEValuation:MODulation:CMIMo:PSTS:AVERage \n
		Snippet: value: List[float] = driver.multiEval.modulation.cmimo.psts.average.read() \n
		Return the single value RMS power results for the individual space-time streams. The current, average, minimum, maximum,
		and standard deviation results can be retrieved. For a meaningful result, set the spatial mapping matrix in the DUT to
		direct mapping. It causes a one-to-one mapping of space time streams to TX antennas. Thus a broken TX chain (no power) is
		detected and a damaged chain is identified by its bad EVM. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: power_sts_tx: float Eight values, one value per space-time stream Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:MODulation:CMIMo:PSTS:AVERage?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:MODulation:CMIMo:PSTS:AVERage \n
		Snippet: value: List[float] = driver.multiEval.modulation.cmimo.psts.average.fetch() \n
		Return the single value RMS power results for the individual space-time streams. The current, average, minimum, maximum,
		and standard deviation results can be retrieved. For a meaningful result, set the spatial mapping matrix in the DUT to
		direct mapping. It causes a one-to-one mapping of space time streams to TX antennas. Thus a broken TX chain (no power) is
		detected and a damaged chain is identified by its bad EVM. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: power_sts_tx: float Eight values, one value per space-time stream Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:MODulation:CMIMo:PSTS:AVERage?', suppressed)
		return response
