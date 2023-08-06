from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:LIST:MODulation:DSSS:EVMRms:CURRent \n
		Snippet: value: List[float] = driver.multiEval.listPy.modulation.dsss.evmEms.current.fetch() \n
		Return the current, average, minimum, maximum and standard deviation EVM results for DSSS signals in list mode. Commands
		for EVM peak and EVM RMS values are available. The values in curly brackets {} are specified for each active segment: {...
		}seg 1, {...}seg 2, ..., {...}seg n. The number of active segments n is determined by method RsCmwWlanMeas.Configure.
		MultiEval.ListPy.count. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: evm_rms: float Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:LIST:MODulation:DSSS:EVMRms:CURRent?', suppressed)
		return response
