from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Station:
	"""Station commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("station", core, parent)

	@property
	def reconnect(self):
		"""reconnect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reconnect'):
			from .Station_.Reconnect import Reconnect
			self._reconnect = Reconnect(self._core, self._base)
		return self._reconnect

	@property
	def connect(self):
		"""connect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connect'):
			from .Station_.Connect import Connect
			self._connect = Connect(self._core, self._base)
		return self._connect

	def clone(self) -> 'Station':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Station(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
