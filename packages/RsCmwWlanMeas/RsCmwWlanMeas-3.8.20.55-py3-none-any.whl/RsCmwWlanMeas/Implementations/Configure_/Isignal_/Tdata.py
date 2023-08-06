from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdata:
	"""Tdata commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdata", core, parent)

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .Tdata_.File import File
			self._file = File(self._core, self._base)
		return self._file

	def get_value(self) -> str:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:ISIGnal:TDATa \n
		Snippet: value: str = driver.configure.isignal.tdata.get_value() \n
		Specifies the training data source to be used as the reference signal for CMIMO measurements. \n
			:return: file_name: 'no data' | 'Internal' | 'file name' 'no data': Use no training data. 'Internal': Use in-memory data, acquired during preceding training mode runs. In-memory data must be available. 'file name': Use the training data file with the specified name, in the directory @USERDATA/MIMOData.
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:ISIGnal:TDATa?')
		return trim_str_response(response)

	def set_value(self, file_name: str) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:ISIGnal:TDATa \n
		Snippet: driver.configure.isignal.tdata.set_value(file_name = '1') \n
		Specifies the training data source to be used as the reference signal for CMIMO measurements. \n
			:param file_name: 'no data' | 'Internal' | 'file name' 'no data': Use no training data. 'Internal': Use in-memory data, acquired during preceding training mode runs. In-memory data must be available. 'file name': Use the training data file with the specified name, in the directory @USERDATA/MIMOData.
		"""
		param = Conversions.value_to_quoted_str(file_name)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:ISIGnal:TDATa {param}')

	def clone(self) -> 'Tdata':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tdata(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
