from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Static:
	"""Static commands group definition. 7 total commands, 1 Sub-groups, 1 group commands
	Repeated Capability: Station, default value after init: Station.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("static", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_station_get', 'repcap_station_set', repcap.Station.Nr1)

	def repcap_station_set(self, enum_value: repcap.Station) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Station.Default
		Default value after init: Station.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_station_get(self) -> repcap.Station:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def ipAddress(self):
		"""ipAddress commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_ipAddress'):
			from .Static_.IpAddress import IpAddress
			self._ipAddress = IpAddress(self._core, self._base)
		return self._ipAddress

	# noinspection PyTypeChecker
	class SmaskStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- First_Octet: int: No parameter help available
			- Second_Octet: int: No parameter help available
			- Third_Octet: int: No parameter help available
			- Fourth_Octet: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('First_Octet'),
			ArgStruct.scalar_int('Second_Octet'),
			ArgStruct.scalar_int('Third_Octet'),
			ArgStruct.scalar_int('Fourth_Octet')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.First_Octet: int = None
			self.Second_Octet: int = None
			self.Third_Octet: int = None
			self.Fourth_Octet: int = None

	def get_smask(self) -> SmaskStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:SMASk \n
		Snippet: value: SmaskStruct = driver.configure.ipv4.static.get_smask() \n
		Specifies the subnet mask of the built-in IPv4 stack. The setting is relevant for instruments without DAU. \n
			:return: structure: for return value, see the help for SmaskStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:SMASk?', self.__class__.SmaskStruct())

	def set_smask(self, value: SmaskStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:SMASk \n
		Snippet: driver.configure.ipv4.static.set_smask(value = SmaskStruct()) \n
		Specifies the subnet mask of the built-in IPv4 stack. The setting is relevant for instruments without DAU. \n
			:param value: see the help for SmaskStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:SMASk', value)

	def clone(self) -> 'Static':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Static(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
