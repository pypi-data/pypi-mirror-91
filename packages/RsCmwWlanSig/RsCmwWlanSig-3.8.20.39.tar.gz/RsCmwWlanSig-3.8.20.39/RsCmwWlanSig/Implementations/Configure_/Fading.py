from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fading:
	"""Fading commands group definition. 6 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fading", core, parent)

	@property
	def fsimulator(self):
		"""fsimulator commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_fsimulator'):
			from .Fading_.Fsimulator import Fsimulator
			self._fsimulator = Fsimulator(self._core, self._base)
		return self._fsimulator

	@property
	def awgn(self):
		"""awgn commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_awgn'):
			from .Fading_.Awgn import Awgn
			self._awgn = Awgn(self._core, self._base)
		return self._awgn

	def clone(self) -> 'Fading':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fading(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
