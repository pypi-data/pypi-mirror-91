from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Staid:
	"""Staid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("staid", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Value_Bin: str: string
			- Value_Dec: int: decimal Range: 0 to 2047"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_str('Value_Bin'),
			ArgStruct.scalar_int('Value_Dec')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Value_Bin: str = None
			self.Value_Dec: int = None

	def fetch(self, channel=repcap.Channel.Default, userIx=repcap.UserIx.Default) -> FetchStruct:
		"""SCPI: FETCh:WLAN:MEASurement<instance>:MEValuation:SINFo:HEB:CHANnel<ch_index>:UFIeld<usr_index>:STAid \n
		Snippet: value: FetchStruct = driver.multiEval.sinfo.heb.channel.ufield.staid.fetch(channel = repcap.Channel.Default, userIx = repcap.UserIx.Default) \n
		Queries the value of STA-ID field signaled for the channel and user in HE-SIG-B user-specific field for MIMO. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ufield')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		userIx_cmd_val = self._base.get_repcap_cmd_value(userIx, repcap.UserIx)
		return self._core.io.query_struct(f'FETCh:WLAN:MEASurement<Instance>:MEValuation:SINFo:HEB:CHANnel{channel_cmd_val}:UFIeld{userIx_cmd_val}:STAid?', self.__class__.FetchStruct())
