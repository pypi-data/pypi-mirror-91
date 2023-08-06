from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pgen:
	"""Pgen commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
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
	def ipVersion(self):
		"""ipVersion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ipVersion'):
			from .Pgen_.IpVersion import IpVersion
			self._ipVersion = IpVersion(self._core, self._base)
		return self._ipVersion

	@property
	def uports(self):
		"""uports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uports'):
			from .Pgen_.Uports import Uports
			self._uports = Uports(self._core, self._base)
		return self._uports

	@property
	def protocol(self):
		"""protocol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_protocol'):
			from .Pgen_.Protocol import Protocol
			self._protocol = Protocol(self._core, self._base)
		return self._protocol

	@property
	def config(self):
		"""config commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_config'):
			from .Pgen_.Config import Config
			self._config = Config(self._core, self._base)
		return self._config

	@property
	def destination(self):
		"""destination commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_destination'):
			from .Pgen_.Destination import Destination
			self._destination = Destination(self._core, self._base)
		return self._destination

	def clone(self) -> 'Pgen':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pgen(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
