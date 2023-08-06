from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 10 total commands, 0 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("result", core, parent)

	def get_power_vs_time(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:PVTime \n
		Snippet: value: bool = driver.configure.multiEval.result.get_power_vs_time() \n
		Enables or disables the evaluation of results and shows or hides the power vs. time view. \n
			:return: pv_time_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:PVTime?')
		return Conversions.str_to_bool(response)

	def set_power_vs_time(self, pv_time_enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:PVTime \n
		Snippet: driver.configure.multiEval.result.set_power_vs_time(pv_time_enable = False) \n
		Enables or disables the evaluation of results and shows or hides the power vs. time view. \n
			:param pv_time_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(pv_time_enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:PVTime {param}')

	def get_spectr_flatness(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:SFLatness \n
		Snippet: value: bool = driver.configure.multiEval.result.get_spectr_flatness() \n
		Enables or disables the evaluation of results and shows or hides the spectrum flatness view. \n
			:return: spec_flatness: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:SFLatness?')
		return Conversions.str_to_bool(response)

	def set_spectr_flatness(self, spec_flatness: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:SFLatness \n
		Snippet: driver.configure.multiEval.result.set_spectr_flatness(spec_flatness = False) \n
		Enables or disables the evaluation of results and shows or hides the spectrum flatness view. \n
			:param spec_flatness: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(spec_flatness)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:SFLatness {param}')

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Mod_Scalar: bool: OFF | ON Modulation scalar overview OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
			- Pv_T: bool: OFF | ON Power vs. time
			- Evmvs_Chip: bool: OFF | ON EVM vs chip
			- Evmvs_Sym: bool: OFF | ON EVM vs symbol
			- Evmvs_Carr: bool: OFF | ON EVM vs carrier
			- Iq_Const: bool: OFF | ON I/Q constellation diagram
			- Spec_Flatness: bool: OFF | ON Spectrum flatness
			- Tran_Spec_Mask: bool: OFF | ON Transmit spectrum mask
			- Unused_Tone_Err: bool: OFF | ON Unused tone error"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Mod_Scalar'),
			ArgStruct.scalar_bool('Pv_T'),
			ArgStruct.scalar_bool('Evmvs_Chip'),
			ArgStruct.scalar_bool('Evmvs_Sym'),
			ArgStruct.scalar_bool('Evmvs_Carr'),
			ArgStruct.scalar_bool('Iq_Const'),
			ArgStruct.scalar_bool('Spec_Flatness'),
			ArgStruct.scalar_bool('Tran_Spec_Mask'),
			ArgStruct.scalar_bool('Unused_Tone_Err')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mod_Scalar: bool = None
			self.Pv_T: bool = None
			self.Evmvs_Chip: bool = None
			self.Evmvs_Sym: bool = None
			self.Evmvs_Carr: bool = None
			self.Iq_Const: bool = None
			self.Spec_Flatness: bool = None
			self.Tran_Spec_Mask: bool = None
			self.Unused_Tone_Err: bool = None

	def get_all(self) -> AllStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult[:ALL] \n
		Snippet: value: AllStruct = driver.configure.multiEval.result.get_all() \n
		Enables or disables the evaluation of results and shows or hides the views. This command combines all other
		CONFigure:WLAN:MEAS<i>:MEValuation:RESult... commands. Views can only be hidden for receive mode SISO. To check which
		views are relevant for which standard, see 'Measurement Results'. \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:ALL?', self.__class__.AllStruct())

	def set_all(self, value: AllStruct) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult[:ALL] \n
		Snippet: driver.configure.multiEval.result.set_all(value = AllStruct()) \n
		Enables or disables the evaluation of results and shows or hides the views. This command combines all other
		CONFigure:WLAN:MEAS<i>:MEValuation:RESult... commands. Views can only be hidden for receive mode SISO. To check which
		views are relevant for which standard, see 'Measurement Results'. \n
			:param value: see the help for AllStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:ALL', value)

	def get_evm(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVM \n
		Snippet: value: bool = driver.configure.multiEval.result.get_evm() \n
		Enables or disables the evaluation of results and shows or hides the EVM vs. chip view. \n
			:return: evm_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVM?')
		return Conversions.str_to_bool(response)

	def set_evm(self, evm_enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVM \n
		Snippet: driver.configure.multiEval.result.set_evm(evm_enable = False) \n
		Enables or disables the evaluation of results and shows or hides the EVM vs. chip view. \n
			:param evm_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(evm_enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVM {param}')

	def get_evm_carrier(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVMCarrier \n
		Snippet: value: bool = driver.configure.multiEval.result.get_evm_carrier() \n
		Enables or disables the evaluation of results and shows or hides the EVM vs. carrier view. \n
			:return: evm_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVMCarrier?')
		return Conversions.str_to_bool(response)

	def set_evm_carrier(self, evm_enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVMCarrier \n
		Snippet: driver.configure.multiEval.result.set_evm_carrier(evm_enable = False) \n
		Enables or disables the evaluation of results and shows or hides the EVM vs. carrier view. \n
			:param evm_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(evm_enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVMCarrier {param}')

	def get_iq_constant(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:IQConst \n
		Snippet: value: bool = driver.configure.multiEval.result.get_iq_constant() \n
		Enables or disables the evaluation of results and shows or hides the I/Q constellation diagram view. \n
			:return: iq_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:IQConst?')
		return Conversions.str_to_bool(response)

	def set_iq_constant(self, iq_enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:IQConst \n
		Snippet: driver.configure.multiEval.result.set_iq_constant(iq_enable = False) \n
		Enables or disables the evaluation of results and shows or hides the I/Q constellation diagram view. \n
			:param iq_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(iq_enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:IQConst {param}')

	def get_ut_error(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:UTERror \n
		Snippet: value: bool = driver.configure.multiEval.result.get_ut_error() \n
		Enables or disables the evaluation of results and shows or hides the unused tone error view. \n
			:return: ute_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:UTERror?')
		return Conversions.str_to_bool(response)

	def set_ut_error(self, ute_enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:UTERror \n
		Snippet: driver.configure.multiEval.result.set_ut_error(ute_enable = False) \n
		Enables or disables the evaluation of results and shows or hides the unused tone error view. \n
			:param ute_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(ute_enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:UTERror {param}')

	def get_evm_symbol(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVMSymbol \n
		Snippet: value: bool = driver.configure.multiEval.result.get_evm_symbol() \n
		Enables or disables the evaluation of results and shows or hides the EVM vs. symbol view. \n
			:return: evm_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVMSymbol?')
		return Conversions.str_to_bool(response)

	def set_evm_symbol(self, evm_enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVMSymbol \n
		Snippet: driver.configure.multiEval.result.set_evm_symbol(evm_enable = False) \n
		Enables or disables the evaluation of results and shows or hides the EVM vs. symbol view. \n
			:param evm_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(evm_enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:EVMSymbol {param}')

	def get_ts_mask(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:TSMask \n
		Snippet: value: bool = driver.configure.multiEval.result.get_ts_mask() \n
		Enables or disables the evaluation of results and shows or hides the transmit spectrum mask view. \n
			:return: spec_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:TSMask?')
		return Conversions.str_to_bool(response)

	def set_ts_mask(self, spec_enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:TSMask \n
		Snippet: driver.configure.multiEval.result.set_ts_mask(spec_enable = False) \n
		Enables or disables the evaluation of results and shows or hides the transmit spectrum mask view. \n
			:param spec_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(spec_enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:TSMask {param}')

	def get_mscalar(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:MSCalar \n
		Snippet: value: bool = driver.configure.multiEval.result.get_mscalar() \n
		Enables or disables the evaluation of results and shows or hides the modulation scalar view. \n
			:return: mod_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:MSCalar?')
		return Conversions.str_to_bool(response)

	def set_mscalar(self, mod_enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:MSCalar \n
		Snippet: driver.configure.multiEval.result.set_mscalar(mod_enable = False) \n
		Enables or disables the evaluation of results and shows or hides the modulation scalar view. \n
			:param mod_enable: OFF | ON OFF: Do not evaluate results, hide the view ON: Evaluate results and show the view
		"""
		param = Conversions.bool_to_str(mod_enable)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:RESult:MSCalar {param}')
