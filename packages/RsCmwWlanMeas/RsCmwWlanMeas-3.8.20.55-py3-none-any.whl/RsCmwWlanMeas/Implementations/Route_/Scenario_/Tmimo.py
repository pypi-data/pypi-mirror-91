from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmimo:
	"""Tmimo commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: TrueMimoPath, default value after init: TrueMimoPath.Count1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmimo", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_trueMimoPath_get', 'repcap_trueMimoPath_set', repcap.TrueMimoPath.Count1)

	def repcap_trueMimoPath_set(self, enum_value: repcap.TrueMimoPath) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TrueMimoPath.Default
		Default value after init: TrueMimoPath.Count1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_trueMimoPath_get(self) -> repcap.TrueMimoPath:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, trueMimoPath=repcap.TrueMimoPath.Default) -> None:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:SCENario:TMIMo<PathCount> \n
		Snippet: driver.route.scenario.tmimo.set(trueMimoPath = repcap.TrueMimoPath.Default) \n
		Selects the number of paths for the true MIMO scenario via <PathCount>. The connectors are configurable via
		CONFigure:WLAN:MEAS<i>:RFSettings:ANTenna<n>. This command is available on an R&S CMW with TRX160 only. \n
			:param trueMimoPath: optional repeated capability selector. Default value: Count1 (settable in the interface 'Tmimo')"""
		trueMimoPath_cmd_val = self._base.get_repcap_cmd_value(trueMimoPath, repcap.TrueMimoPath)
		self._core.io.write(f'ROUTe:WLAN:MEASurement<Instance>:SCENario:TMIMo{trueMimoPath_cmd_val}')

	def set_with_opc(self, trueMimoPath=repcap.TrueMimoPath.Default) -> None:
		trueMimoPath_cmd_val = self._base.get_repcap_cmd_value(trueMimoPath, repcap.TrueMimoPath)
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:SCENario:TMIMo<PathCount> \n
		Snippet: driver.route.scenario.tmimo.set_with_opc(trueMimoPath = repcap.TrueMimoPath.Default) \n
		Selects the number of paths for the true MIMO scenario via <PathCount>. The connectors are configurable via
		CONFigure:WLAN:MEAS<i>:RFSettings:ANTenna<n>. This command is available on an R&S CMW with TRX160 only. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwWlanMeas.utilities.opc_timeout_set() to set the timeout value. \n
			:param trueMimoPath: optional repeated capability selector. Default value: Count1 (settable in the interface 'Tmimo')"""
		self._core.io.write_with_opc(f'ROUTe:WLAN:MEASurement<Instance>:SCENario:TMIMo{trueMimoPath_cmd_val}')

	# noinspection PyTypeChecker
	def get(self, trueMimoPath=repcap.TrueMimoPath.Default) -> enums.GuiScenario:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:SCENario:TMIMo<PathCount> \n
		Snippet: value: enums.GuiScenario = driver.route.scenario.tmimo.get(trueMimoPath = repcap.TrueMimoPath.Default) \n
		Selects the number of paths for the true MIMO scenario via <PathCount>. The connectors are configurable via
		CONFigure:WLAN:MEAS<i>:RFSettings:ANTenna<n>. This command is available on an R&S CMW with TRX160 only. \n
			:param trueMimoPath: optional repeated capability selector. Default value: Count1 (settable in the interface 'Tmimo')
			:return: gui_scenario: TMIMo Returns the active scenario (true MIMO) ."""
		trueMimoPath_cmd_val = self._base.get_repcap_cmd_value(trueMimoPath, repcap.TrueMimoPath)
		response = self._core.io.query_str(f'ROUTe:WLAN:MEASurement<Instance>:SCENario:TMIMo{trueMimoPath_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.GuiScenario)

	def clone(self) -> 'Tmimo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tmimo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
