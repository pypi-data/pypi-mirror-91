from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eaka:
	"""Eaka commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eaka", core, parent)

	# noinspection PyTypeChecker
	class KalgoStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ki: str: string Secret key as string with 32 hexadecimal digits
			- Opc: str: string Operator variant key as string with 32 hexadecimal digits
			- Rand: str: string Random number as string with 32 hexadecimal digits
			- Algorithm: enums.AuthAlgorithm: MILenage | XOR Authentication algorithm to be used"""
		__meta_args_list = [
			ArgStruct.scalar_str('Ki'),
			ArgStruct.scalar_str('Opc'),
			ArgStruct.scalar_str('Rand'),
			ArgStruct.scalar_enum('Algorithm', enums.AuthAlgorithm)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ki: str = None
			self.Opc: str = None
			self.Rand: str = None
			self.Algorithm: enums.AuthAlgorithm = None

	def get_kalgo(self) -> KalgoStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:EAKA:KALGo \n
		Snippet: value: KalgoStruct = driver.configure.connection.security.eaka.get_kalgo() \n
		Configures EAP-AKA on the internal RADIUS server. \n
			:return: structure: for return value, see the help for KalgoStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:EAKA:KALGo?', self.__class__.KalgoStruct())

	def set_kalgo(self, value: KalgoStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:EAKA:KALGo \n
		Snippet: driver.configure.connection.security.eaka.set_kalgo(value = KalgoStruct()) \n
		Configures EAP-AKA on the internal RADIUS server. \n
			:param value: see the help for KalgoStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:EAKA:KALGo', value)
