from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standardDev", core, parent)

	def fetch(self, resourceUnit=repcap.ResourceUnit.Default) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:POWer:RUNit<ru>:SDEViation \n
		Snippet: value: List[float] = driver.multiEval.power.runit.standardDev.fetch(resourceUnit = repcap.ResourceUnit.Default) \n
		Returns single power value measured for RU at all antennas (OFDMA) . \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param resourceUnit: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Runit')
			:return: power_vs_ru_all_antennas: No help available"""
		resourceUnit_cmd_val = self._base.get_repcap_cmd_value(resourceUnit, repcap.ResourceUnit)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:POWer:RUNit{resourceUnit_cmd_val}:SDEViation?', suppressed)
		return response
