from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Y:
	"""Y commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("y", core, parent)

	def get_ab(self) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:DSSS:Y:AB \n
		Snippet: value: float = driver.configure.multiEval.limit.tsMask.dsss.y.get_ab() \n
		Defines the power level of the horizontal spectrum mask line connecting point A and B, see 'Transmit Spectrum Mask DSSS'. \n
			:return: yrel_level_ab: numeric Range: -90 dB to 10 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:DSSS:Y:AB?')
		return Conversions.str_to_float(response)

	def set_ab(self, yrel_level_ab: float) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:DSSS:Y:AB \n
		Snippet: driver.configure.multiEval.limit.tsMask.dsss.y.set_ab(yrel_level_ab = 1.0) \n
		Defines the power level of the horizontal spectrum mask line connecting point A and B, see 'Transmit Spectrum Mask DSSS'. \n
			:param yrel_level_ab: numeric Range: -90 dB to 10 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(yrel_level_ab)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:DSSS:Y:AB {param}')

	def get_cd(self) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:DSSS:Y:CD \n
		Snippet: value: float = driver.configure.multiEval.limit.tsMask.dsss.y.get_cd() \n
		Defines the power level of the horizontal spectrum mask line connecting point C and D, see 'Transmit Spectrum Mask DSSS'. \n
			:return: yrel_level_cd: numeric Range: -90 dB to 10 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:DSSS:Y:CD?')
		return Conversions.str_to_float(response)

	def set_cd(self, yrel_level_cd: float) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:DSSS:Y:CD \n
		Snippet: driver.configure.multiEval.limit.tsMask.dsss.y.set_cd(yrel_level_cd = 1.0) \n
		Defines the power level of the horizontal spectrum mask line connecting point C and D, see 'Transmit Spectrum Mask DSSS'. \n
			:param yrel_level_cd: numeric Range: -90 dB to 10 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(yrel_level_cd)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:MEValuation:LIMit:TSMask:DSSS:Y:CD {param}')
