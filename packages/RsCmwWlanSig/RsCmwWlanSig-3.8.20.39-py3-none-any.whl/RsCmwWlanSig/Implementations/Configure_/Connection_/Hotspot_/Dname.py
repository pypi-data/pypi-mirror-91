from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dname:
	"""Dname commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: DomainName, default value after init: DomainName.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dname", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_domainName_get', 'repcap_domainName_set', repcap.DomainName.Nr1)

	def repcap_domainName_set(self, enum_value: repcap.DomainName) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to DomainName.Default
		Default value after init: DomainName.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_domainName_get(self) -> repcap.DomainName:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class DnameStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- State: bool: OFF | ON Disables/enables the list entry
			- Name: str: string Domain name as string"""
		__meta_args_list = [
			ArgStruct.scalar_bool('State'),
			ArgStruct.scalar_str('Name')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.State: bool = None
			self.Name: str = None

	def set(self, structure: DnameStruct, domainName=repcap.DomainName.Default) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:DNAMe<nr> \n
		Snippet: driver.configure.connection.hotspot.dname.set(value = [PROPERTY_STRUCT_NAME](), domainName = repcap.DomainName.Default) \n
		Defines a list of domain names of the entity operating the IEEE 802.11 access network. The first domain name can also be
		defined via method RsCmwWlanSig.Configure.Connection.Hotspot.hspar. \n
			:param structure: for set value, see the help for DnameStruct structure arguments.
			:param domainName: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dname')"""
		domainName_cmd_val = self._base.get_repcap_cmd_value(domainName, repcap.DomainName)
		self._core.io.write_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:DNAMe{domainName_cmd_val}', structure)

	def get(self, domainName=repcap.DomainName.Default) -> DnameStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:DNAMe<nr> \n
		Snippet: value: DnameStruct = driver.configure.connection.hotspot.dname.get(domainName = repcap.DomainName.Default) \n
		Defines a list of domain names of the entity operating the IEEE 802.11 access network. The first domain name can also be
		defined via method RsCmwWlanSig.Configure.Connection.Hotspot.hspar. \n
			:param domainName: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dname')
			:return: structure: for return value, see the help for DnameStruct structure arguments."""
		domainName_cmd_val = self._base.get_repcap_cmd_value(domainName, repcap.DomainName)
		return self._core.io.query_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:DNAMe{domainName_cmd_val}?', self.__class__.DnameStruct())

	def clone(self) -> 'Dname':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dname(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
