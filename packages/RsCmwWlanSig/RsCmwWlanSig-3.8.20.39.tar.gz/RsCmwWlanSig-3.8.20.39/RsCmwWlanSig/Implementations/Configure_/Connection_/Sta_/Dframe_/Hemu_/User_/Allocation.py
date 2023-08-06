from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Allocation:
	"""Allocation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("allocation", core, parent)

	# noinspection PyTypeChecker
	class AllocationStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Ch_20_Index: enums.Ch20Index: CHA1 | CHA2 | CHA3 | CHA4
			- Ru_Index: enums.RuIndex: RU1 | RU2 | RU3 | RU4 | RU5 | RU6 | RU7 | RU8 | RU9"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Ch_20_Index', enums.Ch20Index),
			ArgStruct.scalar_enum('Ru_Index', enums.RuIndex)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ch_20_Index: enums.Ch20Index = None
			self.Ru_Index: enums.RuIndex = None

	def set(self, structure: AllocationStruct, station=repcap.Station.Default, user=repcap.User.Default) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:STA<s>:DFRame:HEMU:USER<index>:ALLocation \n
		Snippet: driver.configure.connection.sta.dframe.hemu.user.allocation.set(value = [PROPERTY_STRUCT_NAME](), station = repcap.Station.Default, user = repcap.User.Default) \n
		Configures allocations for the user in HE MU PPDU. Maps the user to a resource unit (RU) . \n
			:param structure: for set value, see the help for AllocationStruct structure arguments.
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sta')
			:param user: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		user_cmd_val = self._base.get_repcap_cmd_value(user, repcap.User)
		self._core.io.write_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:STA{station_cmd_val}:DFRame:HEMU:USER{user_cmd_val}:ALLocation', structure)

	def get(self, station=repcap.Station.Default, user=repcap.User.Default) -> AllocationStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:STA<s>:DFRame:HEMU:USER<index>:ALLocation \n
		Snippet: value: AllocationStruct = driver.configure.connection.sta.dframe.hemu.user.allocation.get(station = repcap.Station.Default, user = repcap.User.Default) \n
		Configures allocations for the user in HE MU PPDU. Maps the user to a resource unit (RU) . \n
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sta')
			:param user: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: structure: for return value, see the help for AllocationStruct structure arguments."""
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		user_cmd_val = self._base.get_repcap_cmd_value(user, repcap.User)
		return self._core.io.query_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:STA{station_cmd_val}:DFRame:HEMU:USER{user_cmd_val}:ALLocation?', self.__class__.AllocationStruct())
