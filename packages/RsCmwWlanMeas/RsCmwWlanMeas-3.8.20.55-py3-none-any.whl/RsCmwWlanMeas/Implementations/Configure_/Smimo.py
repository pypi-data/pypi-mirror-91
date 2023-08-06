from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Smimo:
	"""Smimo commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("smimo", core, parent)

	# noinspection PyTypeChecker
	def get_ctuple(self) -> enums.ConnectorTuple:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:SMIMo:CTUPle \n
		Snippet: value: enums.ConnectorTuple = driver.configure.smimo.get_ctuple() \n
		This command is available on the R&S CMW100 only. It sets the connectors to be reserved for switched MIMO measurements.
		The number of connected antennas can be further limited using method RsCmwWlanMeas.Configure.Mimo.noAntennas. Setting the
		<ConTuple> is only possible if a switched MIMO scenario has already been activated via
		ROUTe:WLAN:MEAS<i>:SCENario:SMIMo<PathCount>. \n
			:return: con_tuple: CT12 | CT34 | CT56 | CT78 | CT14 | CT58 | CT18 Connector range to be reserved CTxy means connector 1.x to 1.y. For the MIMO2x2 scenario, the values CT12, CT34, CT56 and CT78 are possible. For the MIMO4x4 scenario, the values CT14 and CT58 are possible. For the MIMO8x8 scenario, the values CT18 is possible.
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:SMIMo:CTUPle?')
		return Conversions.str_to_scalar_enum(response, enums.ConnectorTuple)

	def set_ctuple(self, con_tuple: enums.ConnectorTuple) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<instance>:SMIMo:CTUPle \n
		Snippet: driver.configure.smimo.set_ctuple(con_tuple = enums.ConnectorTuple.CT12) \n
		This command is available on the R&S CMW100 only. It sets the connectors to be reserved for switched MIMO measurements.
		The number of connected antennas can be further limited using method RsCmwWlanMeas.Configure.Mimo.noAntennas. Setting the
		<ConTuple> is only possible if a switched MIMO scenario has already been activated via
		ROUTe:WLAN:MEAS<i>:SCENario:SMIMo<PathCount>. \n
			:param con_tuple: CT12 | CT34 | CT56 | CT78 | CT14 | CT58 | CT18 Connector range to be reserved CTxy means connector 1.x to 1.y. For the MIMO2x2 scenario, the values CT12, CT34, CT56 and CT78 are possible. For the MIMO4x4 scenario, the values CT14 and CT58 are possible. For the MIMO8x8 scenario, the values CT18 is possible.
		"""
		param = Conversions.enum_scalar_to_str(con_tuple, enums.ConnectorTuple)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:SMIMo:CTUPle {param}')
