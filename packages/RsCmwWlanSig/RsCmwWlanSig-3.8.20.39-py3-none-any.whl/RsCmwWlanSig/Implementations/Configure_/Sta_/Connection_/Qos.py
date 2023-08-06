from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Qos:
	"""Qos commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("qos", core, parent)

	@property
	def barMethod(self):
		"""barMethod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_barMethod'):
			from .Qos_.BarMethod import BarMethod
			self._barMethod = BarMethod(self._core, self._base)
		return self._barMethod

	@property
	def black(self):
		"""black commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_black'):
			from .Qos_.Black import Black
			self._black = Black(self._core, self._base)
		return self._black

	def clone(self) -> 'Qos':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Qos(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
