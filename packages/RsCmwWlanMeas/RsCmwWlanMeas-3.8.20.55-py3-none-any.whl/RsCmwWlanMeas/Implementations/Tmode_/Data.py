from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def clear(self) -> None:
		"""SCPI: CLEar:WLAN:MEASurement<instance>:TMODe:DATA \n
		Snippet: driver.tmode.data.clear() \n
		Clears the current training results and resets the internal data of the training mode. \n
		"""
		self._core.io.write(f'CLEar:WLAN:MEASurement<Instance>:TMODe:DATA')

	def clear_with_opc(self) -> None:
		"""SCPI: CLEar:WLAN:MEASurement<instance>:TMODe:DATA \n
		Snippet: driver.tmode.data.clear_with_opc() \n
		Clears the current training results and resets the internal data of the training mode. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsCmwWlanMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CLEar:WLAN:MEASurement<Instance>:TMODe:DATA')
