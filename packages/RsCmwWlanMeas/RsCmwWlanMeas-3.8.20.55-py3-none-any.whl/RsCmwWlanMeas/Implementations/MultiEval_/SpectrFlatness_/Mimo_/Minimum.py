from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Minimum:
	"""Minimum commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("minimum", core, parent)

	def read(self, mimo=repcap.Mimo.Default) -> List[float]:
		"""SCPI: READ:WLAN:MEASurement<instance>:MEValuation:SFLatness:MIMO<n>:MINimum \n
		Snippet: value: List[float] = driver.multiEval.spectrFlatness.mimo.minimum.read(mimo = repcap.Mimo.Default) \n
		Return the single value margins for switched MIMO measurements, antenna/stream number <n>. There are current, average,
		minimum, and maximum results. For the queries of subcarrier indices for spectrum flatness margins, see: method
		RsCmwWlanMeas.MultiEval.SpectrFlatness.Mimo.X.Current.fetch etc. The values described below are returned by FETCh and
		READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param mimo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mimo')
			:return: spec_flat_margins_tx: float Up to 10 comma-separated list of margins (one value per subcarrier range from left to right) Value 1: trace margin to the upper spectrum flatness limit Value 2 to 5: for the trace margins to the lower spectrum flatness limit Value 6: trace margin to the upper spectrum flatness limit for segment 2 (80+80 MHz) Value 7 to 10: trace margins to the lower spectrum flatness limit for segment 2 (80+80 MHz) Unit: dB"""
		mimo_cmd_val = self._base.get_repcap_cmd_value(mimo, repcap.Mimo)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WLAN:MEASurement<Instance>:MEValuation:SFLatness:MIMO{mimo_cmd_val}:MINimum?', suppressed)
		return response

	def fetch(self, mimo=repcap.Mimo.Default) -> List[float]:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:SFLatness:MIMO<n>:MINimum \n
		Snippet: value: List[float] = driver.multiEval.spectrFlatness.mimo.minimum.fetch(mimo = repcap.Mimo.Default) \n
		Return the single value margins for switched MIMO measurements, antenna/stream number <n>. There are current, average,
		minimum, and maximum results. For the queries of subcarrier indices for spectrum flatness margins, see: method
		RsCmwWlanMeas.MultiEval.SpectrFlatness.Mimo.X.Current.fetch etc. The values described below are returned by FETCh and
		READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param mimo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mimo')
			:return: spec_flat_margins_tx: float Up to 10 comma-separated list of margins (one value per subcarrier range from left to right) Value 1: trace margin to the upper spectrum flatness limit Value 2 to 5: for the trace margins to the lower spectrum flatness limit Value 6: trace margin to the upper spectrum flatness limit for segment 2 (80+80 MHz) Value 7 to 10: trace margins to the lower spectrum flatness limit for segment 2 (80+80 MHz) Unit: dB"""
		mimo_cmd_val = self._base.get_repcap_cmd_value(mimo, repcap.Mimo)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:SFLatness:MIMO{mimo_cmd_val}:MINimum?', suppressed)
		return response

	# noinspection PyTypeChecker
	def calculate(self, mimo=repcap.Mimo.Default) -> List[enums.ResultStatus2]:
		"""SCPI: CALCulate:WLAN:MEASurement<instance>:MEValuation:SFLatness:MIMO<n>:MINimum \n
		Snippet: value: List[enums.ResultStatus2] = driver.multiEval.spectrFlatness.mimo.minimum.calculate(mimo = repcap.Mimo.Default) \n
		Return the single value margins for switched MIMO measurements, antenna/stream number <n>. There are current, average,
		minimum, and maximum results. For the queries of subcarrier indices for spectrum flatness margins, see: method
		RsCmwWlanMeas.MultiEval.SpectrFlatness.Mimo.X.Current.fetch etc. The values described below are returned by FETCh and
		READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwWlanMeas.reliability.last_value to read the updated reliability indicator. \n
			:param mimo: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mimo')
			:return: spec_flat_margins_tx: float Up to 10 comma-separated list of margins (one value per subcarrier range from left to right) Value 1: trace margin to the upper spectrum flatness limit Value 2 to 5: for the trace margins to the lower spectrum flatness limit Value 6: trace margin to the upper spectrum flatness limit for segment 2 (80+80 MHz) Value 7 to 10: trace margins to the lower spectrum flatness limit for segment 2 (80+80 MHz) Unit: dB"""
		mimo_cmd_val = self._base.get_repcap_cmd_value(mimo, repcap.Mimo)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:WLAN:MEASurement<Instance>:MEValuation:SFLatness:MIMO{mimo_cmd_val}:MINimum?', suppressed)
		return Conversions.str_to_list_enum(response, enums.ResultStatus2)
