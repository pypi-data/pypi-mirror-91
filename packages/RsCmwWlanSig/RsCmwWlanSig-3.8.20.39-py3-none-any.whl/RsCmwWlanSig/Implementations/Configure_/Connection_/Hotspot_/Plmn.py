from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Plmn:
	"""Plmn commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Plnm, default value after init: Plnm.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("plmn", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_plnm_get', 'repcap_plnm_set', repcap.Plnm.Nr1)

	def repcap_plnm_set(self, enum_value: repcap.Plnm) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Plnm.Default
		Default value after init: Plnm.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_plnm_get(self) -> repcap.Plnm:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class PlmnStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- State: bool: OFF | ON Disables/enables the list entry
			- Mcc: int: integer Mobile country code Range: 1 to 999
			- Mnc: int: integer Mobile network code Range: Depends on NumOfDigits
			- Num_Of_Digits: enums.NumOfDigits: TWDigits | THDigits Length of the MNC TWDigits: two digits (1 to 99) THDigits: three digits (1 to 999)"""
		__meta_args_list = [
			ArgStruct.scalar_bool('State'),
			ArgStruct.scalar_int('Mcc'),
			ArgStruct.scalar_int('Mnc'),
			ArgStruct.scalar_enum('Num_Of_Digits', enums.NumOfDigits)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.State: bool = None
			self.Mcc: int = None
			self.Mnc: int = None
			self.Num_Of_Digits: enums.NumOfDigits = None

	def set(self, structure: PlmnStruct, plnm=repcap.Plnm.Default) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:PLMN<nr> \n
		Snippet: driver.configure.connection.hotspot.plmn.set(value = [PROPERTY_STRUCT_NAME](), plnm = repcap.Plnm.Default) \n
		Defines a list of 3GPP networks that the hotspot provides service for. The MCC and MNC of the first PLMN can also be
		defined via method RsCmwWlanSig.Configure.Connection.Hotspot.hspar. \n
			:param structure: for set value, see the help for PlmnStruct structure arguments.
			:param plnm: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Plmn')"""
		plnm_cmd_val = self._base.get_repcap_cmd_value(plnm, repcap.Plnm)
		self._core.io.write_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:PLMN{plnm_cmd_val}', structure)

	def get(self, plnm=repcap.Plnm.Default) -> PlmnStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:HOTSpot:PLMN<nr> \n
		Snippet: value: PlmnStruct = driver.configure.connection.hotspot.plmn.get(plnm = repcap.Plnm.Default) \n
		Defines a list of 3GPP networks that the hotspot provides service for. The MCC and MNC of the first PLMN can also be
		defined via method RsCmwWlanSig.Configure.Connection.Hotspot.hspar. \n
			:param plnm: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Plmn')
			:return: structure: for return value, see the help for PlmnStruct structure arguments."""
		plnm_cmd_val = self._base.get_repcap_cmd_value(plnm, repcap.Plnm)
		return self._core.io.query_struct(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:HOTSpot:PLMN{plnm_cmd_val}?', self.__class__.PlmnStruct())

	def clone(self) -> 'Plmn':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Plmn(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
