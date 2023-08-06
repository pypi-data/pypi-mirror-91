from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lofdm:
	"""Lofdm commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lofdm", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:ENABle \n
		Snippet: value: bool = driver.configure.multiEval.limit.spectrFlatness.lofdm.get_enable() \n
		Enables or disables the spectrum flatness limit check for 802.11a/g OFDM signals. \n
			:return: enable: ON | OFF
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:ENABle \n
		Snippet: driver.configure.multiEval.limit.spectrFlatness.lofdm.set_enable(enable = False) \n
		Enables or disables the spectrum flatness limit check for 802.11a/g OFDM signals. \n
			:param enable: ON | OFF
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:ENABle {param}')

	def get_upper(self) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:UPPer \n
		Snippet: value: float = driver.configure.multiEval.limit.spectrFlatness.lofdm.get_upper() \n
		Defines an upper limit for the spectrum flatness of 802.11a/g OFDM signals. The upper limit must be larger than the lower
		limits. \n
			:return: upper: numeric Range: -4 dB to 20 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:UPPer?')
		return Conversions.str_to_float(response)

	def set_upper(self, upper: float) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:UPPer \n
		Snippet: driver.configure.multiEval.limit.spectrFlatness.lofdm.set_upper(upper = 1.0) \n
		Defines an upper limit for the spectrum flatness of 802.11a/g OFDM signals. The upper limit must be larger than the lower
		limits. \n
			:param upper: numeric Range: -4 dB to 20 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(upper)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:UPPer {param}')

	# noinspection PyTypeChecker
	class LowerStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Center: float: numeric Range: -20 dB to 4 dB, Unit: dB
			- Side: float: numeric Range: -20 dB to 4 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Center'),
			ArgStruct.scalar_float('Side')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Center: float = None
			self.Side: float = None

	def get_lower(self) -> LowerStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:LOWer \n
		Snippet: value: LowerStruct = driver.configure.multiEval.limit.spectrFlatness.lofdm.get_lower() \n
		Defines lower limits for the spectrum flatness of the center subcarriers and the side subcarriers of 802.
		11a/g OFDM signals. The lower limits must be smaller than the upper limit. \n
			:return: structure: for return value, see the help for LowerStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:LOWer?', self.__class__.LowerStruct())

	def set_lower(self, value: LowerStruct) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:LOWer \n
		Snippet: driver.configure.multiEval.limit.spectrFlatness.lofdm.set_lower(value = LowerStruct()) \n
		Defines lower limits for the spectrum flatness of the center subcarriers and the side subcarriers of 802.
		11a/g OFDM signals. The lower limits must be smaller than the upper limit. \n
			:param value: see the help for LowerStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:SFLatness:LOFDm:LOWer', value)
