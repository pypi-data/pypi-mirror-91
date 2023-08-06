from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal.StructBase import StructBase
from ..Internal.ArgStruct import ArgStruct
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Route:
	"""Route commands group definition. 9 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("route", core, parent)

	@property
	def scenario(self):
		"""scenario commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_scenario'):
			from .Route_.Scenario import Scenario
			self._scenario = Scenario(self._core, self._base)
		return self._scenario

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Route_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	# noinspection PyTypeChecker
	class SmimoStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Gui_Scenario: enums.GuiScenario: MIMO2x2 | MIMO4x4 | MIMO8x8 MIMO2x2: Switched MIMO 2x2 MIMO4x4: Switched MIMO 4x4 MIMO8x8: Switched MIMO 8x8
			- Controller: str: string For future use
			- Rx_Connector_1: enums.RxConnectorExt: RF connector for the input path 1
			- Rx_Converter_1: enums.RxConverter: RX module for the input path 1
			- Rx_Connector_2: enums.RxConnectorExt: RF connector for the input path 2
			- Rx_Converter_2: enums.RxConverter: RX module for the input path 2
			- Rx_Connector_3: enums.RxConnectorExt: RF connector for the input path 3
			- Rx_Converter_3: enums.RxConverter: RX module for the input path 3
			- Rx_Connector_4: enums.RxConnectorExt: RF connector for the input path 4
			- Rx_Converter_4: enums.RxConverter: RX module for the input path 4"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Gui_Scenario', enums.GuiScenario),
			ArgStruct.scalar_str('Controller'),
			ArgStruct.scalar_enum('Rx_Connector_1', enums.RxConnectorExt),
			ArgStruct.scalar_enum('Rx_Converter_1', enums.RxConverter),
			ArgStruct.scalar_enum('Rx_Connector_2', enums.RxConnectorExt),
			ArgStruct.scalar_enum('Rx_Converter_2', enums.RxConverter),
			ArgStruct.scalar_enum('Rx_Connector_3', enums.RxConnectorExt),
			ArgStruct.scalar_enum('Rx_Converter_3', enums.RxConverter),
			ArgStruct.scalar_enum('Rx_Connector_4', enums.RxConnectorExt),
			ArgStruct.scalar_enum('Rx_Converter_4', enums.RxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Gui_Scenario: enums.GuiScenario = None
			self.Controller: str = None
			self.Rx_Connector_1: enums.RxConnectorExt = None
			self.Rx_Converter_1: enums.RxConverter = None
			self.Rx_Connector_2: enums.RxConnectorExt = None
			self.Rx_Converter_2: enums.RxConverter = None
			self.Rx_Connector_3: enums.RxConnectorExt = None
			self.Rx_Converter_3: enums.RxConverter = None
			self.Rx_Connector_4: enums.RxConnectorExt = None
			self.Rx_Converter_4: enums.RxConverter = None

	# noinspection PyTypeChecker
	def get_smimo(self) -> SmimoStruct:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance>:SMIMo \n
		Snippet: value: SmimoStruct = driver.route.get_smimo() \n
		Returns the configured routing settings for the switched MIMO scenario. Switched MIMO is only supported with an R&S
		CMW100. For connector and converter values, see 'Values for RF Path Selection'. \n
			:return: structure: for return value, see the help for SmimoStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:WLAN:MEASurement<Instance>:SMIMo?', self.__class__.SmimoStruct())

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Scenario: enums.MimoScenario: SALone | CSPath SALone: Standalone (non-signaling) CSPath: Combined signal path (with WLAN signaling)
			- Controller: str: string Controlling application for scenario CSPath
			- Rx_Connector_1: enums.RxConnectorExt: RF connector for the input path
			- Rx_Converter_1: enums.RxConverter: RX module for the input path"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Scenario', enums.MimoScenario),
			ArgStruct.scalar_str('Controller'),
			ArgStruct.scalar_enum('Rx_Connector_1', enums.RxConnectorExt),
			ArgStruct.scalar_enum('Rx_Converter_1', enums.RxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Scenario: enums.MimoScenario = None
			self.Controller: str = None
			self.Rx_Connector_1: enums.RxConnectorExt = None
			self.Rx_Converter_1: enums.RxConverter = None

	# noinspection PyTypeChecker
	def get_value(self) -> ValueStruct:
		"""SCPI: ROUTe:WLAN:MEASurement<Instance> \n
		Snippet: value: ValueStruct = driver.route.get_value() \n
		Returns the configured routing settings for SISO scenarios. For possible connector and converter values, see 'Values for
		RF Path Selection'. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:WLAN:MEASurement<Instance>?', self.__class__.ValueStruct())

	def clone(self) -> 'Route':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Route(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
