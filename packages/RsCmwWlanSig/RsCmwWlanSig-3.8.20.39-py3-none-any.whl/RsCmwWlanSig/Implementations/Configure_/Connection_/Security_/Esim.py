from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Esim:
	"""Esim commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("esim", core, parent)

	# noinspection PyTypeChecker
	class KtThreeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rand: str: string Random challenge as string with 32 hexadecimal digits
			- Sres: str: string Signed response as string with 8 hexadecimal digits
			- Kc: str: string Ciphering key as string with 16 hexadecimal digits"""
		__meta_args_list = [
			ArgStruct.scalar_str('Rand'),
			ArgStruct.scalar_str('Sres'),
			ArgStruct.scalar_str('Kc')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rand: str = None
			self.Sres: str = None
			self.Kc: str = None

	def get_kt_three(self) -> KtThreeStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:ESIM:KTTHree \n
		Snippet: value: KtThreeStruct = driver.configure.connection.security.esim.get_kt_three() \n
		Defines the third triplet for EAP-SIM authentication (internal RADIUS server) . \n
			:return: structure: for return value, see the help for KtThreeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:ESIM:KTTHree?', self.__class__.KtThreeStruct())

	def set_kt_three(self, value: KtThreeStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:ESIM:KTTHree \n
		Snippet: driver.configure.connection.security.esim.set_kt_three(value = KtThreeStruct()) \n
		Defines the third triplet for EAP-SIM authentication (internal RADIUS server) . \n
			:param value: see the help for KtThreeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:ESIM:KTTHree', value)

	# noinspection PyTypeChecker
	class KtTwoStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rand: str: string Random challenge as string with 32 hexadecimal digits
			- Sres: str: string Signed response as string with 8 hexadecimal digits
			- Kc: str: string Ciphering key as string with 16 hexadecimal digits"""
		__meta_args_list = [
			ArgStruct.scalar_str('Rand'),
			ArgStruct.scalar_str('Sres'),
			ArgStruct.scalar_str('Kc')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rand: str = None
			self.Sres: str = None
			self.Kc: str = None

	def get_kt_two(self) -> KtTwoStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:ESIM:KTTWo \n
		Snippet: value: KtTwoStruct = driver.configure.connection.security.esim.get_kt_two() \n
		Defines the second triplet for EAP-SIM authentication (internal RADIUS server) . \n
			:return: structure: for return value, see the help for KtTwoStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:ESIM:KTTWo?', self.__class__.KtTwoStruct())

	def set_kt_two(self, value: KtTwoStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:ESIM:KTTWo \n
		Snippet: driver.configure.connection.security.esim.set_kt_two(value = KtTwoStruct()) \n
		Defines the second triplet for EAP-SIM authentication (internal RADIUS server) . \n
			:param value: see the help for KtTwoStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:ESIM:KTTWo', value)

	# noinspection PyTypeChecker
	class KtoneStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rand: str: string Random challenge as string with 32 hexadecimal digits
			- Sres: str: string Signed response as string with 8 hexadecimal digits
			- Kc: str: string Ciphering key as string with 16 hexadecimal digits"""
		__meta_args_list = [
			ArgStruct.scalar_str('Rand'),
			ArgStruct.scalar_str('Sres'),
			ArgStruct.scalar_str('Kc')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rand: str = None
			self.Sres: str = None
			self.Kc: str = None

	def get_ktone(self) -> KtoneStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:ESIM:KTONe \n
		Snippet: value: KtoneStruct = driver.configure.connection.security.esim.get_ktone() \n
		Defines the first triplet for EAP-SIM authentication (internal RADIUS server) . \n
			:return: structure: for return value, see the help for KtoneStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:ESIM:KTONe?', self.__class__.KtoneStruct())

	def set_ktone(self, value: KtoneStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:ESIM:KTONe \n
		Snippet: driver.configure.connection.security.esim.set_ktone(value = KtoneStruct()) \n
		Defines the first triplet for EAP-SIM authentication (internal RADIUS server) . \n
			:param value: see the help for KtoneStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:ESIM:KTONe', value)
