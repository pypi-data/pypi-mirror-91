from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Antenna:
	"""Antenna commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Antenna, default value after init: Antenna.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("antenna", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_antenna_get', 'repcap_antenna_set', repcap.Antenna.Nr1)

	def repcap_antenna_set(self, enum_value: repcap.Antenna) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Antenna.Default
		Default value after init: Antenna.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_antenna_get(self) -> repcap.Antenna:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, connector_all: str, ext_att: float = None, enp: float = None, antenna=repcap.Antenna.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:ANTenna<n> \n
		Snippet: driver.configure.rfSettings.antenna.set(connector_all = r1, ext_att = 1.0, enp = 1.0, antenna = repcap.Antenna.Default) \n
		Assigns an RF input connector and optionally an external attenuation and expected nominal power to antenna <n>.
		The command is relevant for switched MIMO, true MIMO, and for 80+80 MHz signals with a separate antenna per segment. For
		80+80 MHz signals, the antenna numbering continues for the second segment. Example: Two antennas per segment. Segment 0
		uses antenna 1 and 2. Segment 1 uses antenna 3 and 4. \n
			:param connector_all: 1..8 (1..2 for true MIMO with R&S CMW500/2xx)
			:param ext_att: numeric External attenuation component for antenna n Range: 50 dB to 90 dB , Unit: dB
			:param enp: numeric Expected nominal power for antenna n for true MIMO. It can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the data sheet. Unit: dBm
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Antenna')"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('connector_all', connector_all, DataType.RawString), ArgSingle('ext_att', ext_att, DataType.Float, True), ArgSingle('enp', enp, DataType.Float, True))
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:ANTenna{antenna_cmd_val} {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Connector_Smimo: enums.ConnectorSwitch: No parameter help available
			- Connector_Tmimo: enums.RxConnectorExt: No parameter help available
			- Ext_Att: float: numeric External attenuation component for antenna n Range: 50 dB to 90 dB , Unit: dB
			- Enp: float: numeric Expected nominal power for antenna n for true MIMO. It can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the data sheet. Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Connector_Smimo', enums.ConnectorSwitch),
			ArgStruct.scalar_enum('Connector_Tmimo', enums.RxConnectorExt),
			ArgStruct.scalar_float('Ext_Att'),
			ArgStruct.scalar_float('Enp')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Connector_Smimo: enums.ConnectorSwitch = None
			self.Connector_Tmimo: enums.RxConnectorExt = None
			self.Ext_Att: float = None
			self.Enp: float = None

	def get(self, antenna=repcap.Antenna.Default) -> GetStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:ANTenna<n> \n
		Snippet: value: GetStruct = driver.configure.rfSettings.antenna.get(antenna = repcap.Antenna.Default) \n
		Assigns an RF input connector and optionally an external attenuation and expected nominal power to antenna <n>.
		The command is relevant for switched MIMO, true MIMO, and for 80+80 MHz signals with a separate antenna per segment. For
		80+80 MHz signals, the antenna numbering continues for the second segment. Example: Two antennas per segment. Segment 0
		uses antenna 1 and 2. Segment 1 uses antenna 3 and 4. \n
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Antenna')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		return self._core.io.query_struct(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:ANTenna{antenna_cmd_val}?', self.__class__.GetStruct())

	def clone(self) -> 'Antenna':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Antenna(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
