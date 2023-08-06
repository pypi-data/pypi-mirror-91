from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Etoe:
	"""Etoe commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("etoe", core, parent)

	@property
	def irList(self):
		"""irList commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_irList'):
			from .Etoe_.IrList import IrList
			self._irList = IrList(self._core, self._base)
		return self._irList

	# noinspection PyTypeChecker
	class DuIpStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- State: bool: OFF | ON Disables/enables the IP address configuration
			- First_Number: int: No parameter help available
			- Sec_Number: int: No parameter help available
			- Third_Number: int: No parameter help available
			- Fourth_Number: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('State'),
			ArgStruct.scalar_int('First_Number'),
			ArgStruct.scalar_int('Sec_Number'),
			ArgStruct.scalar_int('Third_Number'),
			ArgStruct.scalar_int('Fourth_Number')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.State: bool = None
			self.First_Number: int = None
			self.Sec_Number: int = None
			self.Third_Number: int = None
			self.Fourth_Number: int = None

	def get_du_ip(self) -> DuIpStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:ETOE:DUIP \n
		Snippet: value: DuIpStruct = driver.configure.etoe.get_du_ip() \n
		Allows you to specify the IPv4 address that the DAU assigns to the DUT via DHCP. \n
			:return: structure: for return value, see the help for DuIpStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:ETOE:DUIP?', self.__class__.DuIpStruct())

	def set_du_ip(self, value: DuIpStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:ETOE:DUIP \n
		Snippet: driver.configure.etoe.set_du_ip(value = DuIpStruct()) \n
		Allows you to specify the IPv4 address that the DAU assigns to the DUT via DHCP. \n
			:param value: see the help for DuIpStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:ETOE:DUIP', value)

	def clone(self) -> 'Etoe':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Etoe(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
