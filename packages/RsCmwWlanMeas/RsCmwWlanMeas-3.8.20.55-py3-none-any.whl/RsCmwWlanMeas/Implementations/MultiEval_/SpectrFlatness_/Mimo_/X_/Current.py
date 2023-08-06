from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def read(self, mimo=repcap.Mimo.Default) -> List[int]:
		"""SCPI: READ:WLAN:MEASurement<instance>:MEValuation:SFLatness:MIMO<n>:X:CURRent \n
		Snippet: value: List[int] = driver.multiEval.spectrFlatness.mimo.x.current.read(mimo = repcap.Mimo.Default) \n
		Return the subcarrier indices for the current, average, minimum and maximum margin values for switched MIMO,
		antenna/stream number <n>. For the queries of spectrum flatness margins, see: method RsCmwWlanMeas.MultiEval.
		SpectrFlatness.Mimo.Current.fetch etc. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param mimo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mimo')
			:return: spec_flat_margins_segments_tx: No help available"""
		mimo_cmd_val = self._base.get_repcap_cmd_value(mimo, repcap.Mimo)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:SFLatness:MIMO{mimo_cmd_val}:X:CURRent?', suppressed)
		return response

	def fetch(self, mimo=repcap.Mimo.Default) -> List[int]:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:SFLatness:MIMO<n>:X:CURRent \n
		Snippet: value: List[int] = driver.multiEval.spectrFlatness.mimo.x.current.fetch(mimo = repcap.Mimo.Default) \n
		Return the subcarrier indices for the current, average, minimum and maximum margin values for switched MIMO,
		antenna/stream number <n>. For the queries of spectrum flatness margins, see: method RsCmwWlanMeas.MultiEval.
		SpectrFlatness.Mimo.Current.fetch etc. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param mimo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mimo')
			:return: spec_flat_margins_segments_tx: No help available"""
		mimo_cmd_val = self._base.get_repcap_cmd_value(mimo, repcap.Mimo)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:SFLatness:MIMO{mimo_cmd_val}:X:CURRent?', suppressed)
		return response
