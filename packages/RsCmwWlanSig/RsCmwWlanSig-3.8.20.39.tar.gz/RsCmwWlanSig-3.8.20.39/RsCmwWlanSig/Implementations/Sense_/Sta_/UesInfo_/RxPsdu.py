from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxPsdu:
	"""RxPsdu commands group definition. 6 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxPsdu", core, parent)

	@property
	def noNht(self):
		"""noNht commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noNht'):
			from .RxPsdu_.NoNht import NoNht
			self._noNht = NoNht(self._core, self._base)
		return self._noNht

	@property
	def ht(self):
		"""ht commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ht'):
			from .RxPsdu_.Ht import Ht
			self._ht = Ht(self._core, self._base)
		return self._ht

	@property
	def vht(self):
		"""vht commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vht'):
			from .RxPsdu_.Vht import Vht
			self._vht = Vht(self._core, self._base)
		return self._vht

	@property
	def hesu(self):
		"""hesu commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hesu'):
			from .RxPsdu_.Hesu import Hesu
			self._hesu = Hesu(self._core, self._base)
		return self._hesu

	@property
	def hemu(self):
		"""hemu commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hemu'):
			from .RxPsdu_.Hemu import Hemu
			self._hemu = Hemu(self._core, self._base)
		return self._hemu

	@property
	def hetb(self):
		"""hetb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hetb'):
			from .RxPsdu_.Hetb import Hetb
			self._hetb = Hetb(self._core, self._base)
		return self._hetb

	def clone(self) -> 'RxPsdu':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxPsdu(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
