from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hemu:
	"""Hemu commands group definition. 8 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hemu", core, parent)

	@property
	def alsField(self):
		"""alsField commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alsField'):
			from .Hemu_.AlsField import AlsField
			self._alsField = AlsField(self._core, self._base)
		return self._alsField

	@property
	def ruAllocation(self):
		"""ruAllocation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ruAllocation'):
			from .Hemu_.RuAllocation import RuAllocation
			self._ruAllocation = RuAllocation(self._core, self._base)
		return self._ruAllocation

	@property
	def blAllocation(self):
		"""blAllocation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_blAllocation'):
			from .Hemu_.BlAllocation import BlAllocation
			self._blAllocation = BlAllocation(self._core, self._base)
		return self._blAllocation

	@property
	def user(self):
		"""user commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .Hemu_.User import User
			self._user = User(self._core, self._base)
		return self._user

	@property
	def dummy(self):
		"""dummy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dummy'):
			from .Hemu_.Dummy import Dummy
			self._dummy = Dummy(self._core, self._base)
		return self._dummy

	def clone(self) -> 'Hemu':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hemu(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
