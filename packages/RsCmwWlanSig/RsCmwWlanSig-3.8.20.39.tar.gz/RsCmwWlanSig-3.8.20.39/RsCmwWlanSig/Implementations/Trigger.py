from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 14 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	@property
	def rx(self):
		"""rx commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rx'):
			from .Trigger_.Rx import Rx
			self._rx = Rx(self._core, self._base)
		return self._rx

	@property
	def tx(self):
		"""tx commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tx'):
			from .Trigger_.Tx import Tx
			self._tx = Tx(self._core, self._base)
		return self._tx

	def clone(self) -> 'Trigger':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trigger(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
