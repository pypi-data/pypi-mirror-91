from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dsss:
	"""Dsss commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dsss", core, parent)

	# noinspection PyTypeChecker
	class ElengthStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Evaluation_Length_Chips: int: No parameter help available
			- Skip_Ph: bool: OFF | ON OFF: measure also preamble and header ON: skip preamble and header"""
		__meta_args_list = [
			ArgStruct.scalar_int('Evaluation_Length_Chips'),
			ArgStruct.scalar_bool('Skip_Ph')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Evaluation_Length_Chips: int = None
			self.Skip_Ph: bool = None

	def get_elength(self) -> ElengthStruct:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:ISIGnal:DSSS:ELENgth \n
		Snippet: value: ElengthStruct = driver.configure.isignal.dsss.get_elength() \n
		Specifies the evaluation length of the burst for DSSS signals. \n
			:return: structure: for return value, see the help for ElengthStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:MEASurement<Instance>:ISIGnal:DSSS:ELENgth?', self.__class__.ElengthStruct())

	def set_elength(self, value: ElengthStruct) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:ISIGnal:DSSS:ELENgth \n
		Snippet: driver.configure.isignal.dsss.set_elength(value = ElengthStruct()) \n
		Specifies the evaluation length of the burst for DSSS signals. \n
			:param value: see the help for ElengthStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:MEASurement<Instance>:ISIGnal:DSSS:ELENgth', value)
