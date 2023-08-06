from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eattenuation:
	"""Eattenuation commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eattenuation", core, parent)

	@property
	def inputPy(self):
		"""inputPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inputPy'):
			from .Eattenuation_.InputPy import InputPy
			self._inputPy = InputPy(self._core, self._base)
		return self._inputPy

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Eattenuation_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	def clone(self) -> 'Eattenuation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Eattenuation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
