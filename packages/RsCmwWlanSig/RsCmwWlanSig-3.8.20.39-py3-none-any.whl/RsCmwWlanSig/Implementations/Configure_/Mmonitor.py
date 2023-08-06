from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mmonitor:
	"""Mmonitor commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mmonitor", core, parent)

	@property
	def ipAddress(self):
		"""ipAddress commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ipAddress'):
			from .Mmonitor_.IpAddress import IpAddress
			self._ipAddress = IpAddress(self._core, self._base)
		return self._ipAddress

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:MMONitor:ENABle \n
		Snippet: value: bool = driver.configure.mmonitor.get_enable() \n
		Enables or disables message monitoring for the WLAN signaling application. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:MMONitor:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:MMONitor:ENABle \n
		Snippet: driver.configure.mmonitor.set_enable(enable = False) \n
		Enables or disables message monitoring for the WLAN signaling application. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:MMONitor:ENABle {param}')

	def clone(self) -> 'Mmonitor':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mmonitor(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
