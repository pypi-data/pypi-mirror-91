from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("result", core, parent)

	# noinspection PyTypeChecker
	class ResultStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Enable_Mod: bool: OFF | ON
			- Enable_Sem: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Mod'),
			ArgStruct.scalar_bool('Enable_Sem')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Mod: bool = None
			self.Enable_Sem: bool = None

	def set(self, structure: ResultStruct, segmentB=repcap.SegmentB.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:RESult \n
		Snippet: driver.configure.multiEval.listPy.segment.result.set(value = [PROPERTY_STRUCT_NAME](), segmentB = repcap.SegmentB.Default) \n
		Enables or disables the evaluation of results for modulation and transmit spectrum mask measurements for segment <no> in
		list mode. \n
			:param structure: for set value, see the help for ResultStruct structure arguments.
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		self._core.io.write_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:RESult', structure)

	def get(self, segmentB=repcap.SegmentB.Default) -> ResultStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:RESult \n
		Snippet: value: ResultStruct = driver.configure.multiEval.listPy.segment.result.get(segmentB = repcap.SegmentB.Default) \n
		Enables or disables the evaluation of results for modulation and transmit spectrum mask measurements for segment <no> in
		list mode. \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for ResultStruct structure arguments."""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		return self._core.io.query_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:RESult?', self.__class__.ResultStruct())
