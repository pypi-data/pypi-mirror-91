from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Umargin:
	"""Umargin commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Connector, default value after init: Connector.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("umargin", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_connector_get', 'repcap_connector_set', repcap.Connector.Nr1)

	def repcap_connector_set(self, enum_value: repcap.Connector) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Connector.Default
		Default value after init: Connector.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_connector_get(self) -> repcap.Connector:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, user_margin: float, connector=repcap.Connector.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:UMARgin<connector> \n
		Snippet: driver.configure.rfSettings.umargin.set(user_margin = 1.0, connector = repcap.Connector.Default) \n
		Sets the margin that the measurement adds to the expected nominal power to determine the reference power. The reference
		power minus the external input attenuation must be within the power range of the selected input connector. Refer to the
		data sheet. \n
			:param user_margin: numeric Range: 0 dB to (34 dB + external attenuation - expected nominal power) , Unit: dB
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Umargin')"""
		param = Conversions.decimal_value_to_str(user_margin)
		connector_cmd_val = self._base.get_repcap_cmd_value(connector, repcap.Connector)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:UMARgin{connector_cmd_val} {param}')

	def get(self, connector=repcap.Connector.Default) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:UMARgin<connector> \n
		Snippet: value: float = driver.configure.rfSettings.umargin.get(connector = repcap.Connector.Default) \n
		Sets the margin that the measurement adds to the expected nominal power to determine the reference power. The reference
		power minus the external input attenuation must be within the power range of the selected input connector. Refer to the
		data sheet. \n
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Umargin')
			:return: user_margin: numeric Range: 0 dB to (34 dB + external attenuation - expected nominal power) , Unit: dB"""
		connector_cmd_val = self._base.get_repcap_cmd_value(connector, repcap.Connector)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:UMARgin{connector_cmd_val}?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Umargin':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Umargin(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
