from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scenario:
	"""Scenario commands group definition. 6 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scenario", core, parent)

	@property
	def smi(self):
		"""smi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smi'):
			from .Scenario_.Smi import Smi
			self._smi = Smi(self._core, self._base)
		return self._smi

	@property
	def smimo(self):
		"""smimo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smimo'):
			from .Scenario_.Smimo import Smimo
			self._smimo = Smimo(self._core, self._base)
		return self._smimo

	@property
	def tmimo(self):
		"""tmimo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmimo'):
			from .Scenario_.Tmimo import Tmimo
			self._tmimo = Tmimo(self._core, self._base)
		return self._tmimo

	# noinspection PyTypeChecker
	class SaloneStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rx_Connector: enums.RxConnectorExt: RF connector for the input path
			- Rx_Converter: enums.RxConverter: RX module for the input path"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Rx_Connector', enums.RxConnectorExt),
			ArgStruct.scalar_enum('Rx_Converter', enums.RxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rx_Connector: enums.RxConnectorExt = None
			self.Rx_Converter: enums.RxConverter = None

	# noinspection PyTypeChecker
	def get_salone(self) -> SaloneStruct:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:SCENario:SALone \n
		Snippet: value: SaloneStruct = driver.route.scenario.get_salone() \n
		Activates the standalone scenario and selects the RF input path for the measured RF signal. For possible connector and
		converter values, see 'Values for RF Path Selection'. \n
			:return: structure: for return value, see the help for SaloneStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:WLAN:MEASurement<Instance>:SCENario:SALone?', self.__class__.SaloneStruct())

	def set_salone(self, value: SaloneStruct) -> None:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:SCENario:SALone \n
		Snippet: driver.route.scenario.set_salone(value = SaloneStruct()) \n
		Activates the standalone scenario and selects the RF input path for the measured RF signal. For possible connector and
		converter values, see 'Values for RF Path Selection'. \n
			:param value: see the help for SaloneStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:WLAN:MEASurement<Instance>:SCENario:SALone', value)

	def get_cspath(self) -> str:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:SCENario:CSPath \n
		Snippet: value: str = driver.route.scenario.get_cspath() \n
		Activates the combined signal path scenario and selects the master application. The master controls the signal routing
		and analyzer settings while the combined signal path scenario is active. \n
			:return: master: string String parameter selecting the master application, e.g., 'WLAN Sig1' or 'WLAN Sig2'
		"""
		response = self._core.io.query_str('ROUTe:WLAN:MEASurement<Instance>:SCENario:CSPath?')
		return trim_str_response(response)

	def set_cspath(self, master: str) -> None:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:SCENario:CSPath \n
		Snippet: driver.route.scenario.set_cspath(master = '1') \n
		Activates the combined signal path scenario and selects the master application. The master controls the signal routing
		and analyzer settings while the combined signal path scenario is active. \n
			:param master: string String parameter selecting the master application, e.g., 'WLAN Sig1' or 'WLAN Sig2'
		"""
		param = Conversions.value_to_quoted_str(master)
		self._core.io.write(f'ROUTe:WLAN:MEASurement<Instance>:SCENario:CSPath {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.GuiScenario:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:SCENario \n
		Snippet: value: enums.GuiScenario = driver.route.scenario.get_value() \n
		Returns the active scenario. \n
			:return: gui_scenario: SALone | CSPath | MIMO2x2 | MIMO4x4 | MIMO8x8 | TMIMo SALone: Standalone (non-signaling) CSPath: Combined signal path (with WLAN signaling) MIMO2x2: Switched MIMO 2x2 (R&S CMW100) MIMO4x4: Switched MIMO 4x4 (R&S CMW100) MIMO8x8: Switched MIMO 8x8 (R&S CMW100) TMIMo: True MIMO (R&S CMW with TRX160)
		"""
		response = self._core.io.query_str('ROUTe:WLAN:MEASurement<Instance>:SCENario?')
		return Conversions.str_to_scalar_enum(response, enums.GuiScenario)

	def clone(self) -> 'Scenario':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scenario(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
