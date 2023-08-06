from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MacReserve:
	"""MacReserve commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("macReserve", core, parent)

	# noinspection PyTypeChecker
	class MacReserveStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- Reservation: enums.Reservation: ANY | SET | OFF ANY - the slot is available to a STA of any MAC address SET - reserves the slot for a particular MAC address OFF - the slot is disabled
			- Address: str: Optional setting parameter. string MAC address of the DUT for Reservation = SET"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Reservation', enums.Reservation),
			ArgStruct.scalar_str('Address')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reservation: enums.Reservation = None
			self.Address: str = None

	def set(self, structure: MacReserveStruct, station=repcap.Station.Default) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:ASSociation:STA<s>:MACReserve \n
		Snippet: driver.configure.connection.association.sta.macReserve.set(value = [PROPERTY_STRUCT_NAME](), station = repcap.Station.Default) \n
		Configures three slots available for STAs, if method RsCmwWlanSig.Configure.Connection.mstation is set to ON \n
			:param structure: for set value, see the help for MacReserveStruct structure arguments.
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sta')"""
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		self._core.io.write_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:ASSociation:STA{station_cmd_val}:MACReserve', structure)

	def get(self, station=repcap.Station.Default) -> MacReserveStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:ASSociation:STA<s>:MACReserve \n
		Snippet: value: MacReserveStruct = driver.configure.connection.association.sta.macReserve.get(station = repcap.Station.Default) \n
		Configures three slots available for STAs, if method RsCmwWlanSig.Configure.Connection.mstation is set to ON \n
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sta')
			:return: structure: for return value, see the help for MacReserveStruct structure arguments."""
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		return self._core.io.query_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:ASSociation:STA{station_cmd_val}:MACReserve?', self.__class__.MacReserveStruct())
