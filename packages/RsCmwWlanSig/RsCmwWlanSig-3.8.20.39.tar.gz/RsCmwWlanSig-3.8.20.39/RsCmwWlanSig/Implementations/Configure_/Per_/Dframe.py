from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dframe:
	"""Dframe commands group definition. 8 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dframe", core, parent)

	@property
	def hemu(self):
		"""hemu commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_hemu'):
			from .Dframe_.Hemu import Hemu
			self._hemu = Hemu(self._core, self._base)
		return self._hemu

	def clone(self) -> 'Dframe':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dframe(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
