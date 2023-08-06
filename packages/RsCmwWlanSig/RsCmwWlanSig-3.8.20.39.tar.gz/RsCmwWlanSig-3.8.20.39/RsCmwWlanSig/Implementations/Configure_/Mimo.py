from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mimo:
	"""Mimo commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mimo", core, parent)

	# noinspection PyTypeChecker
	def get_tm_mode(self) -> enums.MimoMode:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:MIMO:TMMode \n
		Snippet: value: enums.MimoMode = driver.configure.mimo.get_tm_mode() \n
		Selects the transmission mode for MIMO connections. This command supports only spatial multiplexing and space time block
		coding (STBC) . In addition, to enable STBC in a particular data frame, use the commands: method RsCmwWlanSig.Configure.
		Sta.Connection.Dfdef.set or method RsCmwWlanSig.Configure.Per.fdef \n
			:return: mode: STBC | SMULtiplexin
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:MIMO:TMMode?')
		return Conversions.str_to_scalar_enum(response, enums.MimoMode)

	def set_tm_mode(self, mode: enums.MimoMode) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:MIMO:TMMode \n
		Snippet: driver.configure.mimo.set_tm_mode(mode = enums.MimoMode.SMULtiplexin) \n
		Selects the transmission mode for MIMO connections. This command supports only spatial multiplexing and space time block
		coding (STBC) . In addition, to enable STBC in a particular data frame, use the commands: method RsCmwWlanSig.Configure.
		Sta.Connection.Dfdef.set or method RsCmwWlanSig.Configure.Per.fdef \n
			:param mode: STBC | SMULtiplexin
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.MimoMode)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:MIMO:TMMode {param}')

	# noinspection PyTypeChecker
	class TcsdStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Csd_1: int: No parameter help available
			- Csd_2: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Csd_1'),
			ArgStruct.scalar_int('Csd_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Csd_1: int = None
			self.Csd_2: int = None

	def get_tcsd(self) -> TcsdStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:MIMO:TCSD \n
		Snippet: value: TcsdStruct = driver.configure.mimo.get_tcsd() \n
		No command help available \n
			:return: structure: for return value, see the help for TcsdStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:MIMO:TCSD?', self.__class__.TcsdStruct())

	def set_tcsd(self, value: TcsdStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:MIMO:TCSD \n
		Snippet: driver.configure.mimo.set_tcsd(value = TcsdStruct()) \n
		No command help available \n
			:param value: see the help for TcsdStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:MIMO:TCSD', value)
