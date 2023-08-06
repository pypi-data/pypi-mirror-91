from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rx:
	"""Rx commands group definition. 11 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rx", core, parent)

	@property
	def macFrame(self):
		"""macFrame commands group. 1 Sub-classes, 9 commands."""
		if not hasattr(self, '_macFrame'):
			from .Rx_.MacFrame import MacFrame
			self._macFrame = MacFrame(self._core, self._base)
		return self._macFrame

	def clone(self) -> 'Rx':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rx(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
