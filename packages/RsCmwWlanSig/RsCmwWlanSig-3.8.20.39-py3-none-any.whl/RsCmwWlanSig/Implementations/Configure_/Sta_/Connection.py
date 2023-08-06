from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Connection:
	"""Connection commands group definition. 13 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("connection", core, parent)

	@property
	def qos(self):
		"""qos commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_qos'):
			from .Connection_.Qos import Qos
			self._qos = Qos(self._core, self._base)
		return self._qos

	@property
	def dfdef(self):
		"""dfdef commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfdef'):
			from .Connection_.Dfdef import Dfdef
			self._dfdef = Dfdef(self._core, self._base)
		return self._dfdef

	@property
	def hetf(self):
		"""hetf commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_hetf'):
			from .Connection_.Hetf import Hetf
			self._hetf = Hetf(self._core, self._base)
		return self._hetf

	@property
	def ampdu(self):
		"""ampdu commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ampdu'):
			from .Connection_.Ampdu import Ampdu
			self._ampdu = Ampdu(self._core, self._base)
		return self._ampdu

	def clone(self) -> 'Connection':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Connection(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
