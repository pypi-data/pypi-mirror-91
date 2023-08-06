from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rserver:
	"""Rserver commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rserver", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SourceInt:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:RSERver:MODE \n
		Snippet: value: enums.SourceInt = driver.configure.connection.security.rserver.get_mode() \n
		Selects the RADIUS server mode for WPA/WPA2 enterprise. \n
			:return: mode: INTernal | EXTernal
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:RSERver:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def set_mode(self, mode: enums.SourceInt) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:RSERver:MODE \n
		Snippet: driver.configure.connection.security.rserver.set_mode(mode = enums.SourceInt.EXTernal) \n
		Selects the RADIUS server mode for WPA/WPA2 enterprise. \n
			:param mode: INTernal | EXTernal
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.SourceInt)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:RSERver:MODE {param}')

	def get_skey(self) -> str:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:RSERver:SKEY \n
		Snippet: value: str = driver.configure.connection.security.rserver.get_skey() \n
		Sets the shared key of an external RADIUS server. \n
			:return: string: string Shared key as string
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:RSERver:SKEY?')
		return trim_str_response(response)

	def set_skey(self, string: str) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:RSERver:SKEY \n
		Snippet: driver.configure.connection.security.rserver.set_skey(string = '1') \n
		Sets the shared key of an external RADIUS server. \n
			:param string: string Shared key as string
		"""
		param = Conversions.value_to_quoted_str(string)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:RSERver:SKEY {param}')

	def get_pnumber(self) -> int:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:RSERver:PNUMber \n
		Snippet: value: int = driver.configure.connection.security.rserver.get_pnumber() \n
		Sets the UDP port number of an external RADIUS server. \n
			:return: number: integer Range: 1 to 65535
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:RSERver:PNUMber?')
		return Conversions.str_to_int(response)

	def set_pnumber(self, number: int) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:RSERver:PNUMber \n
		Snippet: driver.configure.connection.security.rserver.set_pnumber(number = 1) \n
		Sets the UDP port number of an external RADIUS server. \n
			:param number: integer Range: 1 to 65535
		"""
		param = Conversions.decimal_value_to_str(number)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:RSERver:PNUMber {param}')

	# noinspection PyTypeChecker
	class IconfStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ip_First_Part: int: No parameter help available
			- Ip_Second_Part: int: No parameter help available
			- Ip_Third_Part: int: No parameter help available
			- Ip_Fourth_Part: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Ip_First_Part'),
			ArgStruct.scalar_int('Ip_Second_Part'),
			ArgStruct.scalar_int('Ip_Third_Part'),
			ArgStruct.scalar_int('Ip_Fourth_Part')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ip_First_Part: int = None
			self.Ip_Second_Part: int = None
			self.Ip_Third_Part: int = None
			self.Ip_Fourth_Part: int = None

	def get_iconf(self) -> IconfStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:RSERver:ICONf \n
		Snippet: value: IconfStruct = driver.configure.connection.security.rserver.get_iconf() \n
		Sets the IPv4 address of an external RADIUS server. \n
			:return: structure: for return value, see the help for IconfStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:RSERver:ICONf?', self.__class__.IconfStruct())

	def set_iconf(self, value: IconfStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SECurity:RSERver:ICONf \n
		Snippet: driver.configure.connection.security.rserver.set_iconf(value = IconfStruct()) \n
		Sets the IPv4 address of an external RADIUS server. \n
			:param value: see the help for IconfStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SECurity:RSERver:ICONf', value)
