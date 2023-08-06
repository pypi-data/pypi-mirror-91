from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sense:
	"""Sense commands group definition. 21 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sense", core, parent)

	@property
	def uesInfo(self):
		"""uesInfo commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_uesInfo'):
			from .Sense_.UesInfo import UesInfo
			self._uesInfo = UesInfo(self._core, self._base)
		return self._uesInfo

	@property
	def sta(self):
		"""sta commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_sta'):
			from .Sense_.Sta import Sta
			self._sta = Sta(self._core, self._base)
		return self._sta

	@property
	def pgen(self):
		"""pgen commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pgen'):
			from .Sense_.Pgen import Pgen
			self._pgen = Pgen(self._core, self._base)
		return self._pgen

	@property
	def sinfo(self):
		"""sinfo commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinfo'):
			from .Sense_.Sinfo import Sinfo
			self._sinfo = Sinfo(self._core, self._base)
		return self._sinfo

	@property
	def eventLogging(self):
		"""eventLogging commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eventLogging'):
			from .Sense_.EventLogging import EventLogging
			self._eventLogging = EventLogging(self._core, self._base)
		return self._eventLogging

	def clone(self) -> 'Sense':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sense(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
