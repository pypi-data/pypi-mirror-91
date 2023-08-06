from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfSettings:
	"""RfSettings commands group definition. 11 total commands, 5 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rfSettings", core, parent)

	@property
	def antenna(self):
		"""antenna commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_antenna'):
			from .RfSettings_.Antenna import Antenna
			self._antenna = Antenna(self._core, self._base)
		return self._antenna

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_frequency'):
			from .RfSettings_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def envelopePower(self):
		"""envelopePower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_envelopePower'):
			from .RfSettings_.EnvelopePower import EnvelopePower
			self._envelopePower = EnvelopePower(self._core, self._base)
		return self._envelopePower

	@property
	def eattenuation(self):
		"""eattenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eattenuation'):
			from .RfSettings_.Eattenuation import Eattenuation
			self._eattenuation = Eattenuation(self._core, self._base)
		return self._eattenuation

	@property
	def umargin(self):
		"""umargin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_umargin'):
			from .RfSettings_.Umargin import Umargin
			self._umargin = Umargin(self._core, self._base)
		return self._umargin

	def get_santennas(self) -> bool:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:SANTennas \n
		Snippet: value: bool = driver.configure.rfSettings.get_santennas() \n
		It specifies whether the DUT uses separate antennas for the two segments of an 80+80 MHz signal. To assign RF input
		connectors to the two antennas, see CONFigure:WLAN:MEAS<i>:RFSettings:ANTenna<n>. \n
			:return: sep_ant: ON | OFF ON: separate antennas for each segment OFF: same antennas for both segments
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:RFSettings:SANTennas?')
		return Conversions.str_to_bool(response)

	def set_santennas(self, sep_ant: bool) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:SANTennas \n
		Snippet: driver.configure.rfSettings.set_santennas(sep_ant = False) \n
		It specifies whether the DUT uses separate antennas for the two segments of an 80+80 MHz signal. To assign RF input
		connectors to the two antennas, see CONFigure:WLAN:MEAS<i>:RFSettings:ANTenna<n>. \n
			:param sep_ant: ON | OFF ON: separate antennas for each segment OFF: same antennas for both segments
		"""
		param = Conversions.bool_to_str(sep_ant)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:SANTennas {param}')

	def get_ml_offset(self) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:MLOFfset \n
		Snippet: value: float = driver.configure.rfSettings.get_ml_offset() \n
		Varies the input level of the mixer in the analyzer path. For the combined signal path scenario,
		useCONFigure:WLAN:SIGN<i>:RFSettings:ANTenna<n>:MLOFfset. \n
			:return: ml_offset: numeric Range: -10 dB to 10 dB, for R&S CMW with TRX160: -10 dB to 16 dB , Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:RFSettings:MLOFfset?')
		return Conversions.str_to_float(response)

	def set_ml_offset(self, ml_offset: float) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:MLOFfset \n
		Snippet: driver.configure.rfSettings.set_ml_offset(ml_offset = 1.0) \n
		Varies the input level of the mixer in the analyzer path. For the combined signal path scenario,
		useCONFigure:WLAN:SIGN<i>:RFSettings:ANTenna<n>:MLOFfset. \n
			:param ml_offset: numeric Range: -10 dB to 10 dB, for R&S CMW with TRX160: -10 dB to 16 dB , Unit: dB
		"""
		param = Conversions.decimal_value_to_str(ml_offset)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:MLOFfset {param}')

	def get_freq_offset(self) -> float:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:FOFFset \n
		Snippet: value: float = driver.configure.rfSettings.get_freq_offset() \n
		Sets a positive or negative frequency offset to be added to the center frequency (method RsCmwWlanMeas.Configure.
		RfSettings.Frequency.value) . \n
			:return: freq_offset: numeric Range: -80 kHz to 80 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:WLAN:MEASurement<Instance>:RFSettings:FOFFset?')
		return Conversions.str_to_float(response)

	def set_freq_offset(self, freq_offset: float) -> None:
		"""SCPI: CONFigure:WLAN:MEASurement<Instance>:RFSettings:FOFFset \n
		Snippet: driver.configure.rfSettings.set_freq_offset(freq_offset = 1.0) \n
		Sets a positive or negative frequency offset to be added to the center frequency (method RsCmwWlanMeas.Configure.
		RfSettings.Frequency.value) . \n
			:param freq_offset: numeric Range: -80 kHz to 80 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(freq_offset)
		self._core.io.write(f'CONFigure:WLAN:MEASurement<Instance>:RFSettings:FOFFset {param}')

	def clone(self) -> 'RfSettings':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfSettings(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
