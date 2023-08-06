from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 179 total commands, 14 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	@property
	def fading(self):
		"""fading commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fading'):
			from .Configure_.Fading import Fading
			self._fading = Fading(self._core, self._base)
		return self._fading

	@property
	def edau(self):
		"""edau commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_edau'):
			from .Configure_.Edau import Edau
			self._edau = Edau(self._core, self._base)
		return self._edau

	@property
	def mimo(self):
		"""mimo commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mimo'):
			from .Configure_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	@property
	def uesInfo(self):
		"""uesInfo commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_uesInfo'):
			from .Configure_.UesInfo import UesInfo
			self._uesInfo = UesInfo(self._core, self._base)
		return self._uesInfo

	@property
	def etoe(self):
		"""etoe commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_etoe'):
			from .Configure_.Etoe import Etoe
			self._etoe = Etoe(self._core, self._base)
		return self._etoe

	@property
	def rfSettings(self):
		"""rfSettings commands group. 2 Sub-classes, 12 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Configure_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def connection(self):
		"""connection commands group. 16 Sub-classes, 16 commands."""
		if not hasattr(self, '_connection'):
			from .Configure_.Connection import Connection
			self._connection = Connection(self._core, self._base)
		return self._connection

	@property
	def sta(self):
		"""sta commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sta'):
			from .Configure_.Sta import Sta
			self._sta = Sta(self._core, self._base)
		return self._sta

	@property
	def pgen(self):
		"""pgen commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_pgen'):
			from .Configure_.Pgen import Pgen
			self._pgen = Pgen(self._core, self._base)
		return self._pgen

	@property
	def ipv6(self):
		"""ipv6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ipv6'):
			from .Configure_.Ipv6 import Ipv6
			self._ipv6 = Ipv6(self._core, self._base)
		return self._ipv6

	@property
	def ipv4(self):
		"""ipv4 commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ipv4'):
			from .Configure_.Ipv4 import Ipv4
			self._ipv4 = Ipv4(self._core, self._base)
		return self._ipv4

	@property
	def hetBased(self):
		"""hetBased commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hetBased'):
			from .Configure_.HetBased import HetBased
			self._hetBased = HetBased(self._core, self._base)
		return self._hetBased

	@property
	def per(self):
		"""per commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_per'):
			from .Configure_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	@property
	def mmonitor(self):
		"""mmonitor commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmonitor'):
			from .Configure_.Mmonitor import Mmonitor
			self._mmonitor = Mmonitor(self._core, self._base)
		return self._mmonitor

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
