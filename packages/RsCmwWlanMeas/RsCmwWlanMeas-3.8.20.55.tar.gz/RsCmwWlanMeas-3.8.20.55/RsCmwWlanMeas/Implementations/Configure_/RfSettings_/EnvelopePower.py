from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnvelopePower:
	"""EnvelopePower commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Connector, default value after init: Connector.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("envelopePower", core, parent)
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

	def set(self, exp_nom_pwr: float, connector=repcap.Connector.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:ENPower<connector> \n
		Snippet: driver.configure.rfSettings.envelopePower.set(exp_nom_pwr = 1.0, connector = repcap.Connector.Default) \n
		Sets the expected nominal power of the measured RF signal. For the combined signal path scenario,
		useCONFigure:WLAN:SIGN<i>:RFSettings:ANTenna<n>:EPEPower. \n
			:param exp_nom_pwr: numeric The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin Range: -47 dBm to 34 dBm for the input power at RF 1 COM and RF 2 COM (please notice also the ranges quoted in the data sheet) . , Unit: dBm
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'EnvelopePower')"""
		param = Conversions.decimal_value_to_str(exp_nom_pwr)
		connector_cmd_val = self._base.get_repcap_cmd_value(connector, repcap.Connector)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:ENPower{connector_cmd_val} {param}')

	def get(self, connector=repcap.Connector.Default) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:ENPower<connector> \n
		Snippet: value: float = driver.configure.rfSettings.envelopePower.get(connector = repcap.Connector.Default) \n
		Sets the expected nominal power of the measured RF signal. For the combined signal path scenario,
		useCONFigure:WLAN:SIGN<i>:RFSettings:ANTenna<n>:EPEPower. \n
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'EnvelopePower')
			:return: exp_nom_pwr: numeric The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin Range: -47 dBm to 34 dBm for the input power at RF 1 COM and RF 2 COM (please notice also the ranges quoted in the data sheet) . , Unit: dBm"""
		connector_cmd_val = self._base.get_repcap_cmd_value(connector, repcap.Connector)
		response = self._core.io.query_str(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:ENPower{connector_cmd_val}?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'EnvelopePower':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EnvelopePower(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
