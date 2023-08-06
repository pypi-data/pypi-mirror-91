from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standardDev", core, parent)

	def fetch(self, resourceUnit=repcap.ResourceUnit.Default, rxAntenna=repcap.RxAntenna.Default) -> float:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:POWer:RUNit<ru>:RXANtenna<n>:SDEViation \n
		Snippet: value: float = driver.multiEval.power.runit.rxAntenna.standardDev.fetch(resourceUnit = repcap.ResourceUnit.Default, rxAntenna = repcap.RxAntenna.Default) \n
		Returns single power value measured for RU at the specified antenna (OFDMA) . \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param resourceUnit: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Runit')
			:param rxAntenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RxAntenna')
			:return: power_vs_antenna_vs_ru: No help available"""
		resourceUnit_cmd_val = self._base.get_repcap_cmd_value(resourceUnit, repcap.ResourceUnit)
		rxAntenna_cmd_val = self._base.get_repcap_cmd_value(rxAntenna, repcap.RxAntenna)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:POWer:RUNit{resourceUnit_cmd_val}:RXANtenna{rxAntenna_cmd_val}:SDEViation?', suppressed)
		return Conversions.str_to_float(response)
