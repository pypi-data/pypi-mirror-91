from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Antenna:
	"""Antenna commands group definition. 3 total commands, 0 Sub-groups, 3 group commands
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

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Decode_Status: enums.DecodeStatus: NAV | INV | OK The decode status of the received signal is not available (NAV) until all involved TX antenna signals were recorded. Then it changes to OK if the HT-SIG (high throughput signaling) fields of individual antenna signals are consistent, or to INValid otherwise.
			- Mcs: int: decimal Modulation and coding scheme of the recorded antenna signal, obtained from the HT-SIG field
			- Power: float: float Absolute power of the measured antenna signal Unit: dBm
			- Pilot_Evm: float: float Error vector magnitude of the pilot subcarriers Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Decode_Status', enums.DecodeStatus),
			ArgStruct.scalar_int('Mcs'),
			ArgStruct.scalar_float('Power'),
			ArgStruct.scalar_float('Pilot_Evm')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Decode_Status: enums.DecodeStatus = None
			self.Mcs: int = None
			self.Power: float = None
			self.Pilot_Evm: float = None

	def read(self, antenna=repcap.Antenna.Default) -> ResultData:
		"""SCPI: READ:WLAN:MEASurement<Instance>:TMODe:ANTenna<Antennas> \n
		Snippet: value: ResultData = driver.tmode.antenna.read(antenna = repcap.Antenna.Default) \n
		Return information about the training data acquired on the designated antenna and the decode status of the received
		signal. \n
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Antenna')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		return self._core.io.query_struct(f'READ:WLAN:MEASurement<Instance>:TMODe:ANTenna{antenna_cmd_val}?', self.__class__.ResultData())

	def fetch(self, antenna=repcap.Antenna.Default) -> ResultData:
		"""SCPI: FETCh:WLAN:MEASurement<Instance>:TMODe:ANTenna<Antennas> \n
		Snippet: value: ResultData = driver.tmode.antenna.fetch(antenna = repcap.Antenna.Default) \n
		Return information about the training data acquired on the designated antenna and the decode status of the received
		signal. \n
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Antenna')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:TMODe:ANTenna{antenna_cmd_val}?', self.__class__.ResultData())

	def initiate(self, antenna=repcap.Antenna.Default) -> None:
		"""SCPI: INITiate:WLAN:MEASurement<Instance>:TMODe:ANTenna<Antennas> \n
		Snippet: driver.tmode.antenna.initiate(antenna = repcap.Antenna.Default) \n
		Starts the training data acquisition for the designated antenna. \n
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Antenna')"""
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		self._core.io.write(f'INITiate:WLAN:MEASurement<Instance>:TMODe:ANTenna{antenna_cmd_val}')

	def initiate_with_opc(self, antenna=repcap.Antenna.Default) -> None:
		antenna_cmd_val = self._base.get_repcap_cmd_value(antenna, repcap.Antenna)
		"""SCPI: INITiate:WLAN:MEASurement<Instance>:TMODe:ANTenna<Antennas> \n
		Snippet: driver.tmode.antenna.initiate_with_opc(antenna = repcap.Antenna.Default) \n
		Starts the training data acquisition for the designated antenna. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCmwWlanMeas.utilities.opc_timeout_set() to set the timeout value. \n
			:param antenna: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Antenna')"""
		self._core.io.write_with_opc(f'INITiate:WLAN:MEASurement<Instance>:TMODe:ANTenna{antenna_cmd_val}')

	def clone(self) -> 'Antenna':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Antenna(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
