from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UesInfo:
	"""UesInfo commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uesInfo", core, parent)

	def reset(self) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:UESinfo:RESet \n
		Snippet: driver.configure.uesInfo.reset() \n
		Clears entries in all statistic tables concerning user data traffic. \n
		"""
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:UESinfo:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:UESinfo:RESet \n
		Snippet: driver.configure.uesInfo.reset_with_opc() \n
		Clears entries in all statistic tables concerning user data traffic. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsCmwWlanSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CONFigure:WLAN:SIGNaling<Instance>:UESinfo:RESet')

	# noinspection PyTypeChecker
	class SettingsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Reporting_Interval: float: float Range: 0.2 s to 5 s
			- Time_Span: int: integer Range: 1 to 1500"""
		__meta_args_list = [
			ArgStruct.scalar_float('Reporting_Interval'),
			ArgStruct.scalar_int('Time_Span')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reporting_Interval: float = None
			self.Time_Span: int = None

	def get_settings(self) -> SettingsStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:UESinfo:SETTings \n
		Snippet: value: SettingsStruct = driver.configure.uesInfo.get_settings() \n
		Sets reporting interval and time span used for enhanced statistics of user data traffic. \n
			:return: structure: for return value, see the help for SettingsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:UESinfo:SETTings?', self.__class__.SettingsStruct())

	def set_settings(self, value: SettingsStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:UESinfo:SETTings \n
		Snippet: driver.configure.uesInfo.set_settings(value = SettingsStruct()) \n
		Sets reporting interval and time span used for enhanced statistics of user data traffic. \n
			:param value: see the help for SettingsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:UESinfo:SETTings', value)
