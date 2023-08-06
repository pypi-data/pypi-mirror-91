from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Quadrature:
	"""Quadrature commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("quadrature", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:IQConst:QUADrature \n
		Snippet: value: List[float] = driver.multiEval.trace.iqConstant.quadrature.read() \n
		Return the results in the I/Q constellation diagram. The I (in phase) and Q (quadrature) components are retrieved via
		separate commands. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: iq_quadrature: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:TRACe:IQConst:QUADrature?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:IQConst:QUADrature \n
		Snippet: value: List[float] = driver.multiEval.trace.iqConstant.quadrature.fetch() \n
		Return the results in the I/Q constellation diagram. The I (in phase) and Q (quadrature) components are retrieved via
		separate commands. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: iq_quadrature: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:TRACe:IQConst:QUADrature?', suppressed)
		return response
