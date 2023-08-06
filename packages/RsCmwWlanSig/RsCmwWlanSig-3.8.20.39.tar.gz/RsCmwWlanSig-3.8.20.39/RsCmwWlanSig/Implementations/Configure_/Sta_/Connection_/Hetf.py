from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hetf:
	"""Hetf commands group definition. 9 total commands, 9 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hetf", core, parent)

	@property
	def nss(self):
		"""nss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nss'):
			from .Hetf_.Nss import Nss
			self._nss = Nss(self._core, self._base)
		return self._nss

	@property
	def sss(self):
		"""sss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sss'):
			from .Hetf_.Sss import Sss
			self._sss = Sss(self._core, self._base)
		return self._sss

	@property
	def dcm(self):
		"""dcm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcm'):
			from .Hetf_.Dcm import Dcm
			self._dcm = Dcm(self._core, self._base)
		return self._dcm

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Hetf_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def ctyp(self):
		"""ctyp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctyp'):
			from .Hetf_.Ctyp import Ctyp
			self._ctyp = Ctyp(self._core, self._base)
		return self._ctyp

	@property
	def rual(self):
		"""rual commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rual'):
			from .Hetf_.Rual import Rual
			self._rual = Rual(self._core, self._base)
		return self._rual

	@property
	def trssi(self):
		"""trssi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trssi'):
			from .Hetf_.Trssi import Trssi
			self._trssi = Trssi(self._core, self._base)
		return self._trssi

	@property
	def trsMode(self):
		"""trsMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trsMode'):
			from .Hetf_.TrsMode import TrsMode
			self._trsMode = TrsMode(self._core, self._base)
		return self._trsMode

	@property
	def tsrControl(self):
		"""tsrControl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsrControl'):
			from .Hetf_.TsrControl import TsrControl
			self._tsrControl = TsrControl(self._core, self._base)
		return self._tsrControl

	def clone(self) -> 'Hetf':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hetf(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
