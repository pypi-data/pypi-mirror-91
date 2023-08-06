from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	def get(self, full_list: bool = None) -> List[str]:
		"""SCPI: TRIGger:WLAN:MEASurement<Instance>:MEValuation:CATalog:SOURce \n
		Snippet: value: List[str] = driver.trigger.multiEval.catalog.source.get(full_list = False) \n
		Lists all trigger source values that can be set using method RsCmwWlanMeas.Trigger.MultiEval.source. \n
			:param full_list: OFF | ON Disables/ enables full list including also invalid trigger sources.
			:return: trig_source: string Comma-separated list of all supported values. Each value is represented as a string."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('full_list', full_list, DataType.Boolean, True))
		response = self._core.io.query_str(f'TRIGger:WLAN:MEASurement<Instance>:MEValuation:CATalog:SOURce? {param}'.rstrip())
		return Conversions.str_to_str_list(response)
