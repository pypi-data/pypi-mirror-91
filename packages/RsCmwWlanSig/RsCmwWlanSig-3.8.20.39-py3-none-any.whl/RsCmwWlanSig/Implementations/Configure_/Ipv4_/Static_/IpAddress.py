from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IpAddress:
	"""IpAddress commands group definition. 6 total commands, 1 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ipAddress", core, parent)

	@property
	def sta(self):
		"""sta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sta'):
			from .IpAddress_.Sta import Sta
			self._sta = Sta(self._core, self._base)
		return self._sta

	# noinspection PyTypeChecker
	class CmwStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- First: int: No parameter help available
			- Sec: int: No parameter help available
			- Third: int: No parameter help available
			- Fourth: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('First'),
			ArgStruct.scalar_int('Sec'),
			ArgStruct.scalar_int('Third'),
			ArgStruct.scalar_int('Fourth')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.First: int = None
			self.Sec: int = None
			self.Third: int = None
			self.Fourth: int = None

	def get_cmw(self) -> CmwStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:CMW \n
		Snippet: value: CmwStruct = driver.configure.ipv4.static.ipAddress.get_cmw() \n
		Defines the static IP V4 address of the R&S CMW. The setting is relevant for instruments without a DAU. \n
			:return: structure: for return value, see the help for CmwStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:CMW?', self.__class__.CmwStruct())

	def set_cmw(self, value: CmwStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:CMW \n
		Snippet: driver.configure.ipv4.static.ipAddress.set_cmw(value = CmwStruct()) \n
		Defines the static IP V4 address of the R&S CMW. The setting is relevant for instruments without a DAU. \n
			:param value: see the help for CmwStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:CMW', value)

	# noinspection PyTypeChecker
	class GatewayStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- First: int: No parameter help available
			- Sec: int: No parameter help available
			- Third: int: No parameter help available
			- Fourth: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('First'),
			ArgStruct.scalar_int('Sec'),
			ArgStruct.scalar_int('Third'),
			ArgStruct.scalar_int('Fourth')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.First: int = None
			self.Sec: int = None
			self.Third: int = None
			self.Fourth: int = None

	def get_gateway(self) -> GatewayStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:GATeway \n
		Snippet: value: GatewayStruct = driver.configure.ipv4.static.ipAddress.get_gateway() \n
		Provides the IPv4 address of the default gateway. The setting is relevant for instruments without DAU. \n
			:return: structure: for return value, see the help for GatewayStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:GATeway?', self.__class__.GatewayStruct())

	def set_gateway(self, value: GatewayStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:GATeway \n
		Snippet: driver.configure.ipv4.static.ipAddress.set_gateway(value = GatewayStruct()) \n
		Provides the IPv4 address of the default gateway. The setting is relevant for instruments without DAU. \n
			:param value: see the help for GatewayStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:GATeway', value)

	# noinspection PyTypeChecker
	class DnsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- First: int: No parameter help available
			- Sec: int: No parameter help available
			- Third: int: No parameter help available
			- Fourth: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('First'),
			ArgStruct.scalar_int('Sec'),
			ArgStruct.scalar_int('Third'),
			ArgStruct.scalar_int('Fourth')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.First: int = None
			self.Sec: int = None
			self.Third: int = None
			self.Fourth: int = None

	def get_dns(self) -> DnsStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:DNS \n
		Snippet: value: DnsStruct = driver.configure.ipv4.static.ipAddress.get_dns() \n
		Provides the IPv4 address of a DNS server to the built-in IPv4 stack. The setting is relevant for instruments without DAU. \n
			:return: structure: for return value, see the help for DnsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:DNS?', self.__class__.DnsStruct())

	def set_dns(self, value: DnsStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:DNS \n
		Snippet: driver.configure.ipv4.static.ipAddress.set_dns(value = DnsStruct()) \n
		Provides the IPv4 address of a DNS server to the built-in IPv4 stack. The setting is relevant for instruments without DAU. \n
			:param value: see the help for DnsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:DNS', value)

	# noinspection PyTypeChecker
	class StackStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- First: int: No parameter help available
			- Sec: int: No parameter help available
			- Third: int: No parameter help available
			- Fourth: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('First'),
			ArgStruct.scalar_int('Sec'),
			ArgStruct.scalar_int('Third'),
			ArgStruct.scalar_int('Fourth')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.First: int = None
			self.Sec: int = None
			self.Third: int = None
			self.Fourth: int = None

	def get_stack(self) -> StackStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:STACk \n
		Snippet: value: StackStruct = driver.configure.ipv4.static.ipAddress.get_stack() \n
		No command help available \n
			:return: structure: for return value, see the help for StackStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:STACk?', self.__class__.StackStruct())

	def set_stack(self, value: StackStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:STACk \n
		Snippet: driver.configure.ipv4.static.ipAddress.set_stack(value = StackStruct()) \n
		No command help available \n
			:param value: see the help for StackStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:STACk', value)

	# noinspection PyTypeChecker
	class DestinationStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
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

	def get_destination(self) -> DestinationStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:DESTination \n
		Snippet: value: DestinationStruct = driver.configure.ipv4.static.ipAddress.get_destination() \n
		No command help available \n
			:return: structure: for return value, see the help for DestinationStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:DESTination?', self.__class__.DestinationStruct())

	def set_destination(self, value: DestinationStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:STATic:IPADdress:DESTination \n
		Snippet: driver.configure.ipv4.static.ipAddress.set_destination(value = DestinationStruct()) \n
		No command help available \n
			:param value: see the help for DestinationStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:STATic:IPADdress:DESTination', value)

	def clone(self) -> 'IpAddress':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IpAddress(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
