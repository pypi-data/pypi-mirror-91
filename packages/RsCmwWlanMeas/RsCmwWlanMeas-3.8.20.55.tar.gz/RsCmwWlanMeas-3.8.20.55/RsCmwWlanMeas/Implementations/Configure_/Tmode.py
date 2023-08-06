from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmode:
	"""Tmode commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmode", core, parent)

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_file'):
			from .Tmode_.File import File
			self._file = File(self._core, self._base)
		return self._file

	def get_no_antennas(self) -> int:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:TMODe:NOANtennas \n
		Snippet: value: int = driver.configure.tmode.get_no_antennas() \n
		Gets/sets the number of TX antennas contributing to the MIMO training signal. \n
			:return: no_of_antennas: decimal Range: 1 to 8 (4 for R&S CMW100)
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:TMODe:NOANtennas?')
		return Conversions.str_to_int(response)

	def set_no_antennas(self, no_of_antennas: int) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:TMODe:NOANtennas \n
		Snippet: driver.configure.tmode.set_no_antennas(no_of_antennas = 1) \n
		Gets/sets the number of TX antennas contributing to the MIMO training signal. \n
			:param no_of_antennas: decimal Range: 1 to 8 (4 for R&S CMW100)
		"""
		param = Conversions.decimal_value_to_str(no_of_antennas)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:TMODe:NOANtennas {param}')

	def clone(self) -> 'Tmode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tmode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
