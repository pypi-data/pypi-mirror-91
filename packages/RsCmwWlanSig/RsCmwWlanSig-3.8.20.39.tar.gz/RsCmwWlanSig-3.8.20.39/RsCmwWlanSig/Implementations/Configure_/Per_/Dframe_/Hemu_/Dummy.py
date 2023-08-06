from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dummy:
	"""Dummy commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Dummy, default value after init: Dummy.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dummy", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_dummy_get', 'repcap_dummy_set', repcap.Dummy.Nr1)

	def repcap_dummy_set(self, enum_value: repcap.Dummy) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Dummy.Default
		Default value after init: Dummy.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_dummy_get(self) -> repcap.Dummy:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Dummy_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	def clone(self) -> 'Dummy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dummy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
