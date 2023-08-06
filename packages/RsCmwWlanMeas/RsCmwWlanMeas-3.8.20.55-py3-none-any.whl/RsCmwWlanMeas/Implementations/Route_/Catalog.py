from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	# noinspection PyTypeChecker
	def get_scenario(self) -> List[enums.GuiScenario]:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:CATalog:SCENario \n
		Snippet: value: List[enums.GuiScenario] = driver.route.catalog.get_scenario() \n
		Returns all scenarios possible for the instrument. \n
			:return: valid_gui_scenarios: SALone | CSPath | MIMO2x2 | MIMO4x4 | MIMO8x8 | TMIMo SALone: Standalone (non-signaling) CSPath: Combined signal path (with WLAN signaling) MIMO2x2: Switched MIMO 2x2 (R&S CMW100) MIMO4x4: Switched MIMO 4x4 (R&S CMW100) MIMO8x8: Switched MIMO 8x8 (R&S CMW100) TMIMo: True MIMO (R&S CMW with TRX160)
		"""
		response = self._core.io.query_str('ROUTe:WLAN:MEASurement<Instance>:CATalog:SCENario?')
		return Conversions.str_to_list_enum(response, enums.GuiScenario)
