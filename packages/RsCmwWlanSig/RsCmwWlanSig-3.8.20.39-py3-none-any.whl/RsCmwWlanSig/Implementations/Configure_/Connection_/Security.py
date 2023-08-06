from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Security:
	"""Security commands group definition. 11 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("security", core, parent)

	@property
	def eaka(self):
		"""eaka commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eaka'):
			from .Security_.Eaka import Eaka
			self._eaka = Eaka(self._core, self._base)
		return self._eaka

	@property
	def esim(self):
		"""esim commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_esim'):
			from .Security_.Esim import Esim
			self._esim = Esim(self._core, self._base)
		return self._esim

	@property
	def rserver(self):
		"""rserver commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_rserver'):
			from .Security_.Rserver import Rserver
			self._rserver = Rserver(self._core, self._base)
		return self._rserver

	# noinspection PyTypeChecker
	class TypePyStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Security_Type: enums.SecurityType: No parameter help available
			- End_Part: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Security_Type', enums.SecurityType),
			ArgStruct.scalar_str('End_Part')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Security_Type: enums.SecurityType = None
			self.End_Part: str = None

	# noinspection PyTypeChecker
	def get_type_py(self) -> TypePyStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:TYPE \n
		Snippet: value: TypePyStruct = driver.configure.connection.security.get_type_py() \n
		No command help available \n
			:return: structure: for return value, see the help for TypePyStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:TYPE?', self.__class__.TypePyStruct())

	def set_type_py(self, value: TypePyStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:TYPE \n
		Snippet: driver.configure.connection.security.set_type_py(value = TypePyStruct()) \n
		No command help available \n
			:param value: see the help for TypePyStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:TYPE', value)

	# noinspection PyTypeChecker
	class PassphraseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Security_Type: enums.SecurityType: DISabled | WPERsonal | WENTerprise | W2Personal | W2ENterprise DISabled: no security WPERsonal: WPA personal WENTerprise: WPA enterprise W2Personal: WPA2 personal W2ENterprise: WPA2 enterprise
			- Passphrase: str: string Passphrase for AP operation mode as a string, 1 to 63 characters"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Security_Type', enums.SecurityType),
			ArgStruct.scalar_str('Passphrase')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Security_Type: enums.SecurityType = None
			self.Passphrase: str = None

	# noinspection PyTypeChecker
	def get_passphrase(self) -> PassphraseStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:PASSphrase \n
		Snippet: value: PassphraseStruct = driver.configure.connection.security.get_passphrase() \n
		Selects the WLAN security mechanism to be used and defines the passphrase for WPA/WPA2 personal. For supported values
		depending on operation mode, see Table 'Supported security mechanisms'. \n
			:return: structure: for return value, see the help for PassphraseStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:PASSphrase?', self.__class__.PassphraseStruct())

	def set_passphrase(self, value: PassphraseStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:PASSphrase \n
		Snippet: driver.configure.connection.security.set_passphrase(value = PassphraseStruct()) \n
		Selects the WLAN security mechanism to be used and defines the passphrase for WPA/WPA2 personal. For supported values
		depending on operation mode, see Table 'Supported security mechanisms'. \n
			:param value: see the help for PassphraseStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:PASSphrase', value)

	# noinspection PyTypeChecker
	def get_encryption(self) -> enums.EncryptionType:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:ENCRyption \n
		Snippet: value: enums.EncryptionType = driver.configure.connection.security.get_encryption() \n
		Sets the encryption type for AP operation mode, if WPA or WPA2 personal security mode is selected. In the current release,
		encryption for WPA is limited to TKIP and encryption for WPA2 is limited to AES. \n
			:return: encryption_type: AES | TKIP | DISabled
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:ENCRyption?')
		return Conversions.str_to_scalar_enum(response, enums.EncryptionType)

	def set_encryption(self, encryption_type: enums.EncryptionType) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:ENCRyption \n
		Snippet: driver.configure.connection.security.set_encryption(encryption_type = enums.EncryptionType.AES) \n
		Sets the encryption type for AP operation mode, if WPA or WPA2 personal security mode is selected. In the current release,
		encryption for WPA is limited to TKIP and encryption for WPA2 is limited to AES. \n
			:param encryption_type: AES | TKIP | DISabled
		"""
		param = Conversions.enum_scalar_to_str(encryption_type, enums.EncryptionType)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:ENCRyption {param}')

	def clone(self) -> 'Security':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Security(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
