from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 4 total commands, 4 Sub-groups, 0 group commands
	Repeated Capability: User, default value after init: User.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_user_get', 'repcap_user_set', repcap.User.Nr1)

	def repcap_user_set(self, enum_value: repcap.User) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to User.Default
		Default value after init: User.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_user_get(self) -> repcap.User:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def allocation(self):
		"""allocation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_allocation'):
			from .User_.Allocation import Allocation
			self._allocation = Allocation(self._core, self._base)
		return self._allocation

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .User_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def streams(self):
		"""streams commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_streams'):
			from .User_.Streams import Streams
			self._streams = Streams(self._core, self._base)
		return self._streams

	@property
	def ctype(self):
		"""ctype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctype'):
			from .User_.Ctype import Ctype
			self._ctype = Ctype(self._core, self._base)
		return self._ctype

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
