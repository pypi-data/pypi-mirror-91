from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Audio:
	"""Audio commands group definition. 17 total commands, 3 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("audio", core, parent)

	@property
	def volControl(self):
		"""volControl commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_volControl'):
			from .Audio_.VolControl import VolControl
			self._volControl = VolControl(self._core, self._base)
		return self._volControl

	@property
	def hfp(self):
		"""hfp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hfp'):
			from .Audio_.Hfp import Hfp
			self._hfp = Hfp(self._core, self._base)
		return self._hfp

	@property
	def a2Dp(self):
		"""a2Dp commands group. 0 Sub-classes, 10 commands."""
		if not hasattr(self, '_a2Dp'):
			from .Audio_.A2Dp import A2Dp
			self._a2Dp = A2Dp(self._core, self._base)
		return self._a2Dp

	# noinspection PyTypeChecker
	def get_sec_mode(self) -> enums.SecurityMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SECMode \n
		Snippet: value: enums.SecurityMode = driver.configure.connection.audio.get_sec_mode() \n
		Specifies security mode for audio tests. \n
			:return: security_mode: SEC2 | SEC3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SECMode?')
		return Conversions.str_to_scalar_enum(response, enums.SecurityMode)

	def set_sec_mode(self, security_mode: enums.SecurityMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SECMode \n
		Snippet: driver.configure.connection.audio.set_sec_mode(security_mode = enums.SecurityMode.SEC2) \n
		Specifies security mode for audio tests. \n
			:param security_mode: SEC2 | SEC3
		"""
		param = Conversions.enum_scalar_to_str(security_mode, enums.SecurityMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SECMode {param}')

	# noinspection PyTypeChecker
	def get_vlink(self) -> enums.VoiceLinkType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VLINk \n
		Snippet: value: enums.VoiceLinkType = driver.configure.connection.audio.get_vlink() \n
		No command help available \n
			:return: voice_link: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VLINk?')
		return Conversions.str_to_scalar_enum(response, enums.VoiceLinkType)

	def set_vlink(self, voice_link: enums.VoiceLinkType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VLINk \n
		Snippet: driver.configure.connection.audio.set_vlink(voice_link = enums.VoiceLinkType.ESCO) \n
		No command help available \n
			:param voice_link: No help available
		"""
		param = Conversions.enum_scalar_to_str(voice_link, enums.VoiceLinkType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VLINk {param}')

	def get_pin_code(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:PINCode \n
		Snippet: value: str = driver.configure.connection.audio.get_pin_code() \n
		Specifies PIN code for audio profile tests. \n
			:return: pin_code: string
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:PINCode?')
		return trim_str_response(response)

	def set_pin_code(self, pin_code: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:PINCode \n
		Snippet: driver.configure.connection.audio.set_pin_code(pin_code = '1') \n
		Specifies PIN code for audio profile tests. \n
			:param pin_code: string
		"""
		param = Conversions.value_to_quoted_str(pin_code)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:PINCode {param}')

	# noinspection PyTypeChecker
	def get_codec(self) -> enums.SpeechCode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec \n
		Snippet: value: enums.SpeechCode = driver.configure.connection.audio.get_codec() \n
		Specifies the codec to be used for synchronous connection-oriented audio connections. \n
			:return: codec: CVSD | ALAW | ULAW | MSBC CVSD: continuously variable slope delta codec (8 kHz - SCO link) ALAW: A-law coding (8 kHz - SCO link) ULAW: μ-law coding (8 kHz - SCO link) mSBC: modified subband coding (16 kHz - eSCO link)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec?')
		return Conversions.str_to_scalar_enum(response, enums.SpeechCode)

	def set_codec(self, codec: enums.SpeechCode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec \n
		Snippet: driver.configure.connection.audio.set_codec(codec = enums.SpeechCode.ALAW) \n
		Specifies the codec to be used for synchronous connection-oriented audio connections. \n
			:param codec: CVSD | ALAW | ULAW | MSBC CVSD: continuously variable slope delta codec (8 kHz - SCO link) ALAW: A-law coding (8 kHz - SCO link) ULAW: μ-law coding (8 kHz - SCO link) mSBC: modified subband coding (16 kHz - eSCO link)
		"""
		param = Conversions.enum_scalar_to_str(codec, enums.SpeechCode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec {param}')

	def clone(self) -> 'Audio':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Audio(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
