from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ipv4:
	"""Ipv4 commands group definition. 8 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ipv4", core, parent)

	@property
	def static(self):
		"""static commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_static'):
			from .Ipv4_.Static import Static
			self._static = Static(self._core, self._base)
		return self._static

	def get_dhcp(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:DHCP \n
		Snippet: value: bool = driver.configure.ipv4.get_dhcp() \n
		Enables or disables the built-in DHCP server. The setting is relevant for station mode, with or without a DAU.
		This setting is not relevant for AP mode. \n
			:return: activate: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:IPVFour:DHCP?')
		return Conversions.str_to_bool(response)

	def set_dhcp(self, activate: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVFour:DHCP \n
		Snippet: driver.configure.ipv4.set_dhcp(activate = False) \n
		Enables or disables the built-in DHCP server. The setting is relevant for station mode, with or without a DAU.
		This setting is not relevant for AP mode. \n
			:param activate: OFF | ON
		"""
		param = Conversions.bool_to_str(activate)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:IPVFour:DHCP {param}')

	def clone(self) -> 'Ipv4':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ipv4(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
