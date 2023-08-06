from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setup:
	"""Setup commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setup", core, parent)

	# noinspection PyTypeChecker
	class SetupStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Segment_Time: float: numeric Duration of the segment Range: 4E-5 s to 1 s
			- Meas_Time: float: numeric Duration of measurement for the segment Range: 1E-5 s to 1 s
			- Meas_Offset: float: numeric Measurement offset for the segment Range: 1E-5 s to 1 s
			- Level: float: numeric Expected nominal power of the measured RF signal within the segment The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin Range: -47 dBm to 34 dBm for the input power at RF 1 COM and RF 2 COM (please notice also the ranges quoted in the data sheet) . , Unit: dBm
			- Frequency: float: numeric Configures the center frequency of the RF analyzer. Set it to the center frequency of the received WLAN channel. Range: 70 MHz to 6 GHz
			- Standard: enums.IeeeStandard: DSSS | LOFDm | POFDm | HTOFdm | VHTofdm | HEOFdm DSSS: 802.11b/g (DSSS) LOFDm: 802.11a/g (OFDM) LOFDm: 802.11p (requires R&S CMW-KM655) HTOFdm: 802.11n (requires R&S CMW-KM651) VHTofdm: 802.11ac (requires R&S CMW-KM656) HEOFdm: 802.11ax (requires R&S CMW-KM657)
			- Band_Width: enums.Bandwidth: BW05mhz | BW10mhz | BW20mhz | BW40mhz | BW80mhz | BW16mhz BW05mhz: 5 MHz (802.11p, n, ac) BW10mhz: 10 MHz (802.11p, n, ac) BW20mhz: 20 MHz (all standards) BW40mhz: 40 MHz (802.11n, ac, ax) BW80mhz: 80 MHz (802.11ac, ax) BW16mhz: 160 MHz (802.11ac, ax)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Segment_Time'),
			ArgStruct.scalar_float('Meas_Time'),
			ArgStruct.scalar_float('Meas_Offset'),
			ArgStruct.scalar_float('Level'),
			ArgStruct.scalar_float('Frequency'),
			ArgStruct.scalar_enum('Standard', enums.IeeeStandard),
			ArgStruct.scalar_enum('Band_Width', enums.Bandwidth)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Segment_Time: float = None
			self.Meas_Time: float = None
			self.Meas_Offset: float = None
			self.Level: float = None
			self.Frequency: float = None
			self.Standard: enums.IeeeStandard = None
			self.Band_Width: enums.Bandwidth = None

	def set(self, structure: SetupStruct, segmentB=repcap.SegmentB.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:SETup \n
		Snippet: driver.configure.multiEval.listPy.segment.setup.set(value = [PROPERTY_STRUCT_NAME](), segmentB = repcap.SegmentB.Default) \n
		Specifies burst parameter settings for segment <no> in list mode. Send this command for all segments to be measured. \n
			:param structure: for set value, see the help for SetupStruct structure arguments.
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		self._core.io.write_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:SETup', structure)

	def get(self, segmentB=repcap.SegmentB.Default) -> SetupStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:SETup \n
		Snippet: value: SetupStruct = driver.configure.multiEval.listPy.segment.setup.get(segmentB = repcap.SegmentB.Default) \n
		Specifies burst parameter settings for segment <no> in list mode. Send this command for all segments to be measured. \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for SetupStruct structure arguments."""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		return self._core.io.query_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:SETup?', self.__class__.SetupStruct())
