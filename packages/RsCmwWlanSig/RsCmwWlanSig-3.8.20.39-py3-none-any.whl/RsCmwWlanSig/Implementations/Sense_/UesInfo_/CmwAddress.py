from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CmwAddress:
	"""CmwAddress commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: IpVersion, default value after init: IpVersion.V4"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cmwAddress", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_ipVersion_get', 'repcap_ipVersion_set', repcap.IpVersion.V4)

	def repcap_ipVersion_set(self, enum_value: repcap.IpVersion) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IpVersion.Default
		Default value after init: IpVersion.V4"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_ipVersion_get(self) -> repcap.IpVersion:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def ipv(self):
		"""ipv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ipv'):
			from .CmwAddress_.Ipv import Ipv
			self._ipv = Ipv(self._core, self._base)
		return self._ipv

	def clone(self) -> 'CmwAddress':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CmwAddress(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
