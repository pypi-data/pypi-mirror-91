from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def get_save(self) -> str:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:TMODe:FILE:SAVE \n
		Snippet: value: str = driver.configure.tmode.file.get_save() \n
		Saves the current training data to a file or queries the file name of the last saved training data file. \n
			:return: file_name: string The name of the training data file - without path but including the file extension. Training data files are saved to the directory @USERDATA/MIMOData.
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:TMODe:FILE:SAVE?')
		return trim_str_response(response)

	def set_save(self, file_name: str) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:TMODe:FILE:SAVE \n
		Snippet: driver.configure.tmode.file.set_save(file_name = '1') \n
		Saves the current training data to a file or queries the file name of the last saved training data file. \n
			:param file_name: string The name of the training data file - without path but including the file extension. Training data files are saved to the directory @USERDATA/MIMOData.
		"""
		param = Conversions.value_to_quoted_str(file_name)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:TMODe:FILE:SAVE {param}')

	def get_date(self) -> str:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:TMODe:FILE:DATE \n
		Snippet: value: str = driver.configure.tmode.file.get_date() \n
		Returns the last modified date of the last saved training data file, if any. \n
			:return: file_date: string String with a formatted date or NAV
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:TMODe:FILE:DATE?')
		return trim_str_response(response)
