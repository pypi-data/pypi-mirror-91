from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scount:
	"""Scount commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scount", core, parent)

	# noinspection PyTypeChecker
	class ScountStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Stat_Count_Mod: int: numeric No. of burst to be measured during modulation measurements Range: 1 to 2000
			- Stat_Count_Sem: int: numeric No. of burst to be measured during spectrum measurements Range: 1 to 1000"""
		__meta_args_list = [
			ArgStruct.scalar_int('Stat_Count_Mod'),
			ArgStruct.scalar_int('Stat_Count_Sem')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Stat_Count_Mod: int = None
			self.Stat_Count_Sem: int = None

	def set(self, structure: ScountStruct, segmentB=repcap.SegmentB.Default) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:SCOunt \n
		Snippet: driver.configure.multiEval.listPy.segment.scount.set(value = [PROPERTY_STRUCT_NAME](), segmentB = repcap.SegmentB.Default) \n
		Specifies the modulation and spectrum statistical length for segment <no> in list mode. \n
			:param structure: for set value, see the help for ScountStruct structure arguments.
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		self._core.io.write_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:SCOunt', structure)

	def get(self, segmentB=repcap.SegmentB.Default) -> ScountStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent<segment>:SCOunt \n
		Snippet: value: ScountStruct = driver.configure.multiEval.listPy.segment.scount.get(segmentB = repcap.SegmentB.Default) \n
		Specifies the modulation and spectrum statistical length for segment <no> in list mode. \n
			:param segmentB: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for ScountStruct structure arguments."""
		segmentB_cmd_val = self._base.get_repcap_cmd_value(segmentB, repcap.SegmentB)
		return self._core.io.query_struct(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIST:SEGMent{segmentB_cmd_val}:SCOunt?', self.__class__.ScountStruct())
