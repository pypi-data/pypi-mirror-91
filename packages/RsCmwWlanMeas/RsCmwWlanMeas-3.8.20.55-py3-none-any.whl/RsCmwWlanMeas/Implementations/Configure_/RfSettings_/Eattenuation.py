from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eattenuation:
	"""Eattenuation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Connector, default value after init: Connector.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eattenuation", core, parent)
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

	def set(self, rf_input_ext_att: float, connector=repcap.Connector.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:EATTenuation<connector> \n
		Snippet: driver.configure.rfSettings.eattenuation.set(rf_input_ext_att = 1.0, connector = repcap.Connector.Default) \n
		Defines an external attenuation (or gain, if the value is negative) , to be applied to all RF input connectors (global
		external attenuation) .
		For the combined signal path scenario, use CONFigure:WLAN:SIGN<i>:RFSettings:ANTenna<n>:EATTenuation:INPut . \n
			:param rf_input_ext_att: Range: -50 dB to 90 dB, Unit: dB
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eattenuation')"""
		param = Conversions.decimal_value_to_str(rf_input_ext_att)
		connector_cmd_val = self._base.get_repcap_cmd_value(connector, repcap.Connector)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:EATTenuation{connector_cmd_val} {param}')

	def get(self, connector=repcap.Connector.Default) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:EATTenuation<connector> \n
		Snippet: value: float = driver.configure.rfSettings.eattenuation.get(connector = repcap.Connector.Default) \n
		Defines an external attenuation (or gain, if the value is negative) , to be applied to all RF input connectors (global
		external attenuation) .
		For the combined signal path scenario, use CONFigure:WLAN:SIGN<i>:RFSettings:ANTenna<n>:EATTenuation:INPut . \n
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eattenuation')
			:return: rf_input_ext_att: Range: -50 dB to 90 dB, Unit: dB"""
		connector_cmd_val = self._base.get_repcap_cmd_value(connector, repcap.Connector)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:EATTenuation{connector_cmd_val}?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Eattenuation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Eattenuation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
