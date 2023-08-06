from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pgen:
	"""Pgen commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: PacketGenerator, default value after init: PacketGenerator.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pgen", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_packetGenerator_get', 'repcap_packetGenerator_set', repcap.PacketGenerator.Nr1)

	def repcap_packetGenerator_set(self, enum_value: repcap.PacketGenerator) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to PacketGenerator.Default
		Default value after init: PacketGenerator.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_packetGenerator_get(self) -> repcap.PacketGenerator:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def pgStats(self):
		"""pgStats commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pgStats'):
			from .Pgen_.PgStats import PgStats
			self._pgStats = PgStats(self._core, self._base)
		return self._pgStats

	def clone(self) -> 'Pgen':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pgen(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
