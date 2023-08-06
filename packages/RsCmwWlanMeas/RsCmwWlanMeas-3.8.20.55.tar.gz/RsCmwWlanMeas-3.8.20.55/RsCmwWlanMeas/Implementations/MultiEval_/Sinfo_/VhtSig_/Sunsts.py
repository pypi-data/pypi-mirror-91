from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sunsts:
	"""Sunsts commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sunsts", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: float: float 'Reliability Indicator'
			- Value_Bin: str: string
			- Value_Dec: int: decimal Range: 0 to 511"""
		__meta_args_list = [
			ArgStruct.scalar_float('Reliability'),
			ArgStruct.scalar_str('Value_Bin'),
			ArgStruct.scalar_int('Value_Dec')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: float = None
			self.Value_Bin: str = None
			self.Value_Dec: int = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:SINFo:VHTSig:SUNSts \n
		Snippet: value: FetchStruct = driver.multiEval.sinfo.vhtSig.sunsts.fetch() \n
		Queries the value of NSTS field signaled in very high throughput signal field for 802.11ac signal (VHT-SIG) . For the
		filed Partial AID refer to: method RsCmwWlanMeas.MultiEval.Sinfo.VhtSig.Paid.fetch \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:SINFo:VHTSig:SUNSts?', self.__class__.FetchStruct())
