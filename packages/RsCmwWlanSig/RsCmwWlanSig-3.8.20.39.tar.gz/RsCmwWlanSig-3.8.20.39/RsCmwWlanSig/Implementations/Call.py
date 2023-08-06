from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Call:
	"""Call commands group definition. 5 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("call", core, parent)

	@property
	def action(self):
		"""action commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_action'):
			from .Call_.Action import Action
			self._action = Action(self._core, self._base)
		return self._action

	@property
	def sta(self):
		"""sta commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sta'):
			from .Call_.Sta import Sta
			self._sta = Sta(self._core, self._base)
		return self._sta

	def clone(self) -> 'Call':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Call(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
