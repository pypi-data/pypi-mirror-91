from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wdirect:
	"""Wdirect commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wdirect", core, parent)

	# noinspection PyTypeChecker
	class AtypeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Method: enums.AuthMethod: No parameter help available
			- Mode: enums.AutoManualMode: No parameter help available
			- Pin: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Method', enums.AuthMethod),
			ArgStruct.scalar_enum('Mode', enums.AutoManualMode),
			ArgStruct.scalar_str('Pin')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Method: enums.AuthMethod = None
			self.Mode: enums.AutoManualMode = None
			self.Pin: str = None

	# noinspection PyTypeChecker
	def get_atype(self) -> AtypeStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:WDIRect:ATYPe \n
		Snippet: value: AtypeStruct = driver.configure.connection.wdirect.get_atype() \n
		No command help available \n
			:return: structure: for return value, see the help for AtypeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:WDIRect:ATYPe?', self.__class__.AtypeStruct())

	def set_atype(self, value: AtypeStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:WDIRect:ATYPe \n
		Snippet: driver.configure.connection.wdirect.set_atype(value = AtypeStruct()) \n
		No command help available \n
			:param value: see the help for AtypeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:WDIRect:ATYPe', value)

	# noinspection PyTypeChecker
	class WdconfStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Manufacturer: str: No parameter help available
			- Model_Name: str: No parameter help available
			- Model_Number: str: No parameter help available
			- Serial_Number: str: No parameter help available
			- Device_Name: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Manufacturer'),
			ArgStruct.scalar_str('Model_Name'),
			ArgStruct.scalar_str('Model_Number'),
			ArgStruct.scalar_str('Serial_Number'),
			ArgStruct.scalar_str('Device_Name')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Manufacturer: str = None
			self.Model_Name: str = None
			self.Model_Number: str = None
			self.Serial_Number: str = None
			self.Device_Name: str = None

	def get_wdconf(self) -> WdconfStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:WDIRect:WDConf \n
		Snippet: value: WdconfStruct = driver.configure.connection.wdirect.get_wdconf() \n
		No command help available \n
			:return: structure: for return value, see the help for WdconfStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:WDIRect:WDConf?', self.__class__.WdconfStruct())

	def set_wdconf(self, value: WdconfStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:WDIRect:WDConf \n
		Snippet: driver.configure.connection.wdirect.set_wdconf(value = WdconfStruct()) \n
		No command help available \n
			:param value: see the help for WdconfStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:WDIRect:WDConf', value)
