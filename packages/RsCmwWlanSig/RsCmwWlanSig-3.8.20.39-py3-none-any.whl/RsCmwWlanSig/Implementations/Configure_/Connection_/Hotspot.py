from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hotspot:
	"""Hotspot commands group definition. 7 total commands, 3 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hotspot", core, parent)

	@property
	def realm(self):
		"""realm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_realm'):
			from .Hotspot_.Realm import Realm
			self._realm = Realm(self._core, self._base)
		return self._realm

	@property
	def dname(self):
		"""dname commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dname'):
			from .Hotspot_.Dname import Dname
			self._dname = Dname(self._core, self._base)
		return self._dname

	@property
	def plmn(self):
		"""plmn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plmn'):
			from .Hotspot_.Plmn import Plmn
			self._plmn = Plmn(self._core, self._base)
		return self._plmn

	# noinspection PyTypeChecker
	class CutilStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Station_Count: int: numeric Number of stations that are currently associated with the BSS Range: 0 to 65535
			- Channel_Utilization: int: numeric Percentage of time, that the access point sensed the primary channel was busy Range: 0 % to 100 %, Unit: %
			- Available_Admission_Capacity: int: numeric Remaining time available via explicit admission control, in units of 32 μs/s Range: 0 to 31250"""
		__meta_args_list = [
			ArgStruct.scalar_int('Station_Count'),
			ArgStruct.scalar_int('Channel_Utilization'),
			ArgStruct.scalar_int('Available_Admission_Capacity')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Station_Count: int = None
			self.Channel_Utilization: int = None
			self.Available_Admission_Capacity: int = None

	def get_cutil(self) -> CutilStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:CUTil \n
		Snippet: value: CutilStruct = driver.configure.connection.hotspot.get_cutil() \n
		Configures the contents of the BSS load element. \n
			:return: structure: for return value, see the help for CutilStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:CUTil?', self.__class__.CutilStruct())

	def set_cutil(self, value: CutilStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:CUTil \n
		Snippet: driver.configure.connection.hotspot.set_cutil(value = CutilStruct()) \n
		Configures the contents of the BSS load element. \n
			:param value: see the help for CutilStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:CUTil', value)

	# noinspection PyTypeChecker
	class HssparStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Downlink_Speed: int: numeric Range: 0 kbit/s to 300000 kbit/s, Unit: kbit/s
			- Uplink_Speed: int: numeric Range: 0 kbit/s to 300000 kbit/s, Unit: kbit/s
			- Ip_V_6_Add_Field: enums.Ipv6AddField: ATNavailable | ATAVailable | AATNknown Indicates whether an IPv6 address can be allocated to the station ATNavailable: address type not available ATAVailable: address type available AATNknown: availability of the address type is not known
			- Ipv_4_Add_Field: enums.Ipv6AddFieldExt: ATNavailable | PIAavailable | PRIaavailabl | SNPiaavailab | DNPiaavailab | PSNiaavailab | PDNiaavailab | AATNknown Indicates whether an IPv4 address can be allocated to the station ATNavailable: address type not available PIAavailable: public IPv4 address available PRIaavailabl: port-restricted IPv4 address available SNPiaavailab: single-NATed private IPv4 address available DNPiaavailab: double-NATed private IPv4 address available PSNiaavailab: port-restricted and single-NATed IPv4 address available PDNiaavailab: port-restricted and double-NATed IPv4 address available AATNknown: availability of the address type not known
			- Realm_Name: str: string Name of reachable NAI realm as string To configure more than one realm, use [CMDLINK: CONFigure:WLAN:SIGNi:CONNection:HOTSpot:REALmno CMDLINK].
			- Eap_Type: enums.EapType: SIM | TTLS | AKA | APRime | TLS Supported extensible authorization protocol type EAP-SIM, EAP-TTLS, EAP-AKA, EAP-AKA' or EAP-TLS To enable multiple EAP types, use [CMDLINK: CONFigure:WLAN:SIGNi:CONNection:HOTSpot:REALmno CMDLINK].
			- Internet_Access: bool: OFF | ON Specifies whether the hotspot provides internet access
			- Net_Auth_Type_Ind: enums.NetAuthTypeInd: ATConditions | OESupported | HREDirection | DREDirection Network authentication type ATConditions: acceptance of terms and conditions OESupported: on-line enrollment supported HREDirection: http/https redirection DREDirection: DNS redirection"""
		__meta_args_list = [
			ArgStruct.scalar_int('Downlink_Speed'),
			ArgStruct.scalar_int('Uplink_Speed'),
			ArgStruct.scalar_enum('Ip_V_6_Add_Field', enums.Ipv6AddField),
			ArgStruct.scalar_enum('Ipv_4_Add_Field', enums.Ipv6AddFieldExt),
			ArgStruct.scalar_str('Realm_Name'),
			ArgStruct.scalar_enum('Eap_Type', enums.EapType),
			ArgStruct.scalar_bool('Internet_Access'),
			ArgStruct.scalar_enum('Net_Auth_Type_Ind', enums.NetAuthTypeInd)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Downlink_Speed: int = None
			self.Uplink_Speed: int = None
			self.Ip_V_6_Add_Field: enums.Ipv6AddField = None
			self.Ipv_4_Add_Field: enums.Ipv6AddFieldExt = None
			self.Realm_Name: str = None
			self.Eap_Type: enums.EapType = None
			self.Internet_Access: bool = None
			self.Net_Auth_Type_Ind: enums.NetAuthTypeInd = None

	def get_hsspar(self) -> HssparStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:HSSPar \n
		Snippet: value: HssparStruct = driver.configure.connection.hotspot.get_hsspar() \n
		Defines supplementary parameters of the Hotspot 2.0 operation mode. \n
			:return: structure: for return value, see the help for HssparStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:HSSPar?', self.__class__.HssparStruct())

	def set_hsspar(self, value: HssparStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:HSSPar \n
		Snippet: driver.configure.connection.hotspot.set_hsspar(value = HssparStruct()) \n
		Defines supplementary parameters of the Hotspot 2.0 operation mode. \n
			:param value: see the help for HssparStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:HSSPar', value)

	# noinspection PyTypeChecker
	def get_mn_digits(self) -> enums.NumOfDigits:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:MNDigits \n
		Snippet: value: enums.NumOfDigits = driver.configure.connection.hotspot.get_mn_digits() \n
		Defines the length of the MNC of the first PLMN in Hotspot 2.0 operation mode. \n
			:return: num_of_digits: TWDigits | THDigits TWDigits: two digits THDigits: three digits
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:MNDigits?')
		return Conversions.str_to_scalar_enum(response, enums.NumOfDigits)

	def set_mn_digits(self, num_of_digits: enums.NumOfDigits) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:MNDigits \n
		Snippet: driver.configure.connection.hotspot.set_mn_digits(num_of_digits = enums.NumOfDigits.THDigits) \n
		Defines the length of the MNC of the first PLMN in Hotspot 2.0 operation mode. \n
			:param num_of_digits: TWDigits | THDigits TWDigits: two digits THDigits: three digits
		"""
		param = Conversions.enum_scalar_to_str(num_of_digits, enums.NumOfDigits)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:MNDigits {param}')

	# noinspection PyTypeChecker
	class HsparStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Access_Net_Type: enums.AccessNetType: PNETwork | PNWGaccess | CPNetwork | FPNetwork | PDNetwork | ESONetwork | TOEXperiment | WILDcard PNETwork: private network PNWGaccess: private network with guest access CPNetwork: chargeable public network FPNetwork: free public network PDNetwork: personal device network ESONetwork: emergency services only network TOEXperiment: test or experimental WILDcard: wildcard
			- Venue_Group: float: numeric | UNSPecified | ASSembly | BUSiness | EDUCational | FAINdustrial | INSTitutional | MERCantile | RESidential | STORage | UAMisc | VEHicular | OUTDoor FAINdustrial: factory and industrial UAMisc: utility and miscellaneous
			- Venue_Type: float: numeric Range: 0 to 255
			- He_Ssid: float: numeric Homogeneous extended service set identifier Range: #H0 to #HFFFFFFFFFFFF
			- Venue_Name: str: string String with up to 252 ASCII characters
			- Mcc: int: numeric Mobile country code of 3GPP network reachable via the hotspot To configure more than one PLMN, use [CMDLINK: CONFigure:WLAN:SIGNi:CONNection:HOTSpot:PLMNno CMDLINK]. Range: 1 to 999
			- Mnc: int: numeric Mobile network code of 3GPP network reachable via the hotspot To configure more than one PLMN, use [CMDLINK: CONFigure:WLAN:SIGNi:CONNection:HOTSpot:PLMNno CMDLINK]. Range: 1 to 9991)
			- Domain_Name: str: string Domain name of the network operator as string To configure more than one domain name, use [CMDLINK: CONFigure:WLAN:SIGNi:CONNection:HOTSpot:DNAMeno CMDLINK].
			- Op_Frie_Name: str: string Friendly name of the network operator as string"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Access_Net_Type', enums.AccessNetType),
			ArgStruct.scalar_float('Venue_Group'),
			ArgStruct.scalar_float('Venue_Type'),
			ArgStruct.scalar_float('He_Ssid'),
			ArgStruct.scalar_str('Venue_Name'),
			ArgStruct.scalar_int('Mcc'),
			ArgStruct.scalar_int('Mnc'),
			ArgStruct.scalar_str('Domain_Name'),
			ArgStruct.scalar_str('Op_Frie_Name')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Access_Net_Type: enums.AccessNetType = None
			self.Venue_Group: float = None
			self.Venue_Type: float = None
			self.He_Ssid: float = None
			self.Venue_Name: str = None
			self.Mcc: int = None
			self.Mnc: int = None
			self.Domain_Name: str = None
			self.Op_Frie_Name: str = None

	# noinspection PyTypeChecker
	def get_hspar(self) -> HsparStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:HSPar \n
		Snippet: value: HsparStruct = driver.configure.connection.hotspot.get_hspar() \n
		Defines basic parameters of the Hotspot 2.0 operation mode. \n
			:return: structure: for return value, see the help for HsparStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:HSPar?', self.__class__.HsparStruct())

	def set_hspar(self, value: HsparStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:HSPar \n
		Snippet: driver.configure.connection.hotspot.set_hspar(value = HsparStruct()) \n
		Defines basic parameters of the Hotspot 2.0 operation mode. \n
			:param value: see the help for HsparStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:HSPar', value)

	def clone(self) -> 'Hotspot':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hotspot(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
