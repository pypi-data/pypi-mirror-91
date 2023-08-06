from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Evmvs_User_All: float: No parameter help available
			- Evmvs_User_Data: float: No parameter help available
			- Evmvs_User_Pilot: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Evmvs_User_All'),
			ArgStruct.scalar_float('Evmvs_User_Data'),
			ArgStruct.scalar_float('Evmvs_User_Pilot')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Evmvs_User_All: float = None
			self.Evmvs_User_Data: float = None
			self.Evmvs_User_Pilot: float = None

	def fetch(self, user=repcap.User.Default) -> FetchStruct:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:MODulation:EVMagnitude:USER<user>:AVERage \n
		Snippet: value: FetchStruct = driver.multiEval.modulation.evMagnitude.user.average.fetch(user = repcap.User.Default) \n
		Return the single value results for OFDMA SISO measurements for the specified user. For MIMO measurements,
		the stream/antenna-independent values are returned. There are current, average, minimum, maximum and standard deviation
		results. \n
			:param user: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		user_cmd_val = self._base.get_repcap_cmd_value(user, repcap.User)
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:MODulation:EVMagnitude:USER{user_cmd_val}:AVERage?', self.__class__.FetchStruct())
