from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Realm:
	"""Realm commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Realm, default value after init: Realm.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("realm", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_realm_get', 'repcap_realm_set', repcap.Realm.Nr1)

	def repcap_realm_set(self, enum_value: repcap.Realm) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Realm.Default
		Default value after init: Realm.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_realm_get(self) -> repcap.Realm:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class RealmStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- State: bool: OFF | ON Disables/enables the list entry
			- Name: str: string Realm name as string
			- Sim: bool: OFF | ON Realm supports EAP-SIM
			- Tls: bool: OFF | ON Realm supports EAP-TLS
			- Ttls: bool: OFF | ON Realm supports EAP-TTLS
			- Aka: bool: OFF | ON Realm supports EAP-AKA
			- Aka_Prime: bool: OFF | ON Realm supports EAP-AKA'"""
		__meta_args_list = [
			ArgStruct.scalar_bool('State'),
			ArgStruct.scalar_str('Name'),
			ArgStruct.scalar_bool('Sim'),
			ArgStruct.scalar_bool('Tls'),
			ArgStruct.scalar_bool('Ttls'),
			ArgStruct.scalar_bool('Aka'),
			ArgStruct.scalar_bool('Aka_Prime')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.State: bool = None
			self.Name: str = None
			self.Sim: bool = None
			self.Tls: bool = None
			self.Ttls: bool = None
			self.Aka: bool = None
			self.Aka_Prime: bool = None

	def set(self, structure: RealmStruct, realm=repcap.Realm.Default) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:REALm<nr> \n
		Snippet: driver.configure.connection.hotspot.realm.set(value = [PROPERTY_STRUCT_NAME](), realm = repcap.Realm.Default) \n
		Defines a list of NAI realms that are reachable via the hotspot. The first realm can also be defined via method
		RsCmwWlanSig.Configure.Connection.Hotspot.hsspar. \n
			:param structure: for set value, see the help for RealmStruct structure arguments.
			:param realm: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Realm')"""
		realm_cmd_val = self._base.get_repcap_cmd_value(realm, repcap.Realm)
		self._core.io.write_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:REALm{realm_cmd_val}', structure)

	def get(self, realm=repcap.Realm.Default) -> RealmStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:REALm<nr> \n
		Snippet: value: RealmStruct = driver.configure.connection.hotspot.realm.get(realm = repcap.Realm.Default) \n
		Defines a list of NAI realms that are reachable via the hotspot. The first realm can also be defined via method
		RsCmwWlanSig.Configure.Connection.Hotspot.hsspar. \n
			:param realm: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Realm')
			:return: structure: for return value, see the help for RealmStruct structure arguments."""
		realm_cmd_val = self._base.get_repcap_cmd_value(realm, repcap.Realm)
		return self._core.io.query_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:REALm{realm_cmd_val}?', self.__class__.RealmStruct())

	def clone(self) -> 'Realm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Realm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
