from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UeCapability:
	"""UeCapability commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ueCapability", core, parent)

	@property
	def mac(self):
		"""mac commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mac'):
			from .UeCapability_.Mac import Mac
			self._mac = Mac(self._core, self._base)
		return self._mac

	@property
	def he(self):
		"""he commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_he'):
			from .UeCapability_.He import He
			self._he = He(self._core, self._base)
		return self._he

	def clone(self) -> 'UeCapability':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UeCapability(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
