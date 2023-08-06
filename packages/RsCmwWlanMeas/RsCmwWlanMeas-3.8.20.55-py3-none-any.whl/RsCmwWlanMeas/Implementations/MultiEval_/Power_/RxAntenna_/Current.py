from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self, rxAntenna=repcap.RxAntenna.Default) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:POWer:RXANtenna<n>:CURRent \n
		Snippet: value: List[float] = driver.multiEval.power.rxAntenna.current.fetch(rxAntenna = repcap.RxAntenna.Default) \n
		Returns single power value measured at the specified antenna for all RUs (OFDMA) . \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param rxAntenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RxAntenna')
			:return: power_vs_antenna_all_rus: No help available"""
		rxAntenna_cmd_val = self._base.get_repcap_cmd_value(rxAntenna, repcap.RxAntenna)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:POWer:RXANtenna{rxAntenna_cmd_val}:CURRent?', suppressed)
		return response
