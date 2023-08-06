from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Schedule:
	"""Schedule commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("schedule", core, parent)

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Schedule_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def ftype(self):
		"""ftype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ftype'):
			from .Schedule_.Ftype import Ftype
			self._ftype = Ftype(self._core, self._base)
		return self._ftype

	@property
	def stime(self):
		"""stime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stime'):
			from .Schedule_.Stime import Stime
			self._stime = Stime(self._core, self._base)
		return self._stime

	@property
	def mwDuration(self):
		"""mwDuration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mwDuration'):
			from .Schedule_.MwDuration import MwDuration
			self._mwDuration = MwDuration(self._core, self._base)
		return self._mwDuration

	@property
	def tenable(self):
		"""tenable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tenable'):
			from .Schedule_.Tenable import Tenable
			self._tenable = Tenable(self._core, self._base)
		return self._tenable

	def clone(self) -> 'Schedule':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Schedule(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
