from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sta:
	"""Sta commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sta", core, parent)

	# noinspection PyTypeChecker
	class StaStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- First_Number: int: No parameter help available
			- Sec_Number: int: No parameter help available
			- Third_Number: int: No parameter help available
			- Fourth_Number: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('First_Number'),
			ArgStruct.scalar_int('Sec_Number'),
			ArgStruct.scalar_int('Third_Number'),
			ArgStruct.scalar_int('Fourth_Number')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.First_Number: int = None
			self.Sec_Number: int = None
			self.Third_Number: int = None
			self.Fourth_Number: int = None

	def set(self, structure: StaStruct, station=repcap.Station.Default) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:STA<s> \n
		Snippet: driver.configure.ipv4.static.ipAddress.sta.set(value = [PROPERTY_STRUCT_NAME](), station = repcap.Station.Default) \n
		Defines the static IP V4 address of the DUT. The setting is only relevant for access point and instruments without a DAU. \n
			:param structure: for set value, see the help for StaStruct structure arguments.
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Static')"""
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		self._core.io.write_struct(f'CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:STA{station_cmd_val}', structure)

	def get(self, station=repcap.Station.Default) -> StaStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:STA<s> \n
		Snippet: value: StaStruct = driver.configure.ipv4.static.ipAddress.sta.get(station = repcap.Station.Default) \n
		Defines the static IP V4 address of the DUT. The setting is only relevant for access point and instruments without a DAU. \n
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Static')
			:return: structure: for return value, see the help for StaStruct structure arguments."""
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		return self._core.io.query_struct(f'CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:STA{station_cmd_val}?', self.__class__.StaStruct())
