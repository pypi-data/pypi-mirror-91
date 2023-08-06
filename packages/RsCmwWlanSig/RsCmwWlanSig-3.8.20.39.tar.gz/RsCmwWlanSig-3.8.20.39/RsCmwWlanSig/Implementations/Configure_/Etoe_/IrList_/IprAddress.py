from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IprAddress:
	"""IprAddress commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: IpRouteAddress, default value after init: IpRouteAddress.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iprAddress", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_ipRouteAddress_get', 'repcap_ipRouteAddress_set', repcap.IpRouteAddress.Nr1)

	def repcap_ipRouteAddress_set(self, enum_value: repcap.IpRouteAddress) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IpRouteAddress.Default
		Default value after init: IpRouteAddress.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_ipRouteAddress_get(self) -> repcap.IpRouteAddress:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class IprAddressStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- State: bool: OFF | ON Entry disabled or enabled
			- Ip_41: int: integer First octet of the IPv4 destination address Range: 0 to 255
			- Ip_42: int: integer Second octet Range: 0 to 255
			- Ip_43: int: integer Third octet Range: 0 to 255
			- Ip_44: int: integer Fourth octet Range: 0 to 255
			- Ip_4_Netmask: int: integer Number of subnet bits for the IPv4 address Range: 1 to 32
			- Ip_6_Prefix: str: string IPv6 prefix as string, for example 'fc01:abab:cdcd:efe0::'
			- Ip_6_Netmask: int: integer Number of subnet bits for the IPv6 address Range: 1 to 128"""
		__meta_args_list = [
			ArgStruct.scalar_bool('State'),
			ArgStruct.scalar_int('Ip_41'),
			ArgStruct.scalar_int('Ip_42'),
			ArgStruct.scalar_int('Ip_43'),
			ArgStruct.scalar_int('Ip_44'),
			ArgStruct.scalar_int('Ip_4_Netmask'),
			ArgStruct.scalar_str('Ip_6_Prefix'),
			ArgStruct.scalar_int('Ip_6_Netmask')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.State: bool = None
			self.Ip_41: int = None
			self.Ip_42: int = None
			self.Ip_43: int = None
			self.Ip_44: int = None
			self.Ip_4_Netmask: int = None
			self.Ip_6_Prefix: str = None
			self.Ip_6_Netmask: int = None

	def set(self, structure: IprAddressStruct, ipRouteAddress=repcap.IpRouteAddress.Default) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:ETOE:IRList:IPRaddress<n> \n
		Snippet: driver.configure.etoe.irList.iprAddress.set(value = [PROPERTY_STRUCT_NAME](), ipRouteAddress = repcap.IpRouteAddress.Default) \n
		Configures an entry of the routes list. The routes list defines destination addresses for which the DAU routes packets to
		the DUT. \n
			:param structure: for set value, see the help for IprAddressStruct structure arguments.
			:param ipRouteAddress: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IprAddress')"""
		ipRouteAddress_cmd_val = self._base.get_repcap_cmd_value(ipRouteAddress, repcap.IpRouteAddress)
		self._core.io.write_struct(f'CONFigure:WLAN:SIGNaling<Instance>:ETOE:IRList:IPRaddress{ipRouteAddress_cmd_val}', structure)

	def get(self, ipRouteAddress=repcap.IpRouteAddress.Default) -> IprAddressStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:ETOE:IRList:IPRaddress<n> \n
		Snippet: value: IprAddressStruct = driver.configure.etoe.irList.iprAddress.get(ipRouteAddress = repcap.IpRouteAddress.Default) \n
		Configures an entry of the routes list. The routes list defines destination addresses for which the DAU routes packets to
		the DUT. \n
			:param ipRouteAddress: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IprAddress')
			:return: structure: for return value, see the help for IprAddressStruct structure arguments."""
		ipRouteAddress_cmd_val = self._base.get_repcap_cmd_value(ipRouteAddress, repcap.IpRouteAddress)
		return self._core.io.query_struct(f'CONFigure:WLAN:SIGNaling<Instance>:ETOE:IRList:IPRaddress{ipRouteAddress_cmd_val}?', self.__class__.IprAddressStruct())

	def clone(self) -> 'IprAddress':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IprAddress(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
