from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmode:
	"""Tmode commands group definition. 5 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmode", core, parent)

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Tmode_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def antenna(self):
		"""antenna commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_antenna'):
			from .Tmode_.Antenna import Antenna
			self._antenna = Antenna(self._core, self._base)
		return self._antenna

	def abort(self) -> None:
		"""SCPI: ABORt:WLAN:MEASurement<Instance>:TMODe \n
		Snippet: driver.tmode.abort() \n
		Aborts the current MIMO training data acquisition. \n
		"""
		self._core.io.write(f'ABORt:WLAN:MEASurement<Instance>:TMODe')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:WLAN:MEASurement<Instance>:TMODe \n
		Snippet: driver.tmode.abort_with_opc() \n
		Aborts the current MIMO training data acquisition. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCmwWlanMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:WLAN:MEASurement<Instance>:TMODe')

	def clone(self) -> 'Tmode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tmode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
