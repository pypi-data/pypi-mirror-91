from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Action:
	"""Action commands group definition. 4 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("action", core, parent)

	@property
	def wps(self):
		"""wps commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_wps'):
			from .Action_.Wps import Wps
			self._wps = Wps(self._core, self._base)
		return self._wps

	@property
	def wdirect(self):
		"""wdirect commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_wdirect'):
			from .Action_.Wdirect import Wdirect
			self._wdirect = Wdirect(self._core, self._base)
		return self._wdirect

	@property
	def station(self):
		"""station commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_station'):
			from .Action_.Station import Station
			self._station = Station(self._core, self._base)
		return self._station

	def clone(self) -> 'Action':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Action(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
