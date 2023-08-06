from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sta:
	"""Sta commands group definition. 13 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: Station, default value after init: Station.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sta", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_station_get', 'repcap_station_set', repcap.Station.Nr1)

	def repcap_station_set(self, enum_value: repcap.Station) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Station.Default
		Default value after init: Station.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_station_get(self) -> repcap.Station:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def uesInfo(self):
		"""uesInfo commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_uesInfo'):
			from .Sta_.UesInfo import UesInfo
			self._uesInfo = UesInfo(self._core, self._base)
		return self._uesInfo

	@property
	def ueCapability(self):
		"""ueCapability commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ueCapability'):
			from .Sta_.UeCapability import UeCapability
			self._ueCapability = UeCapability(self._core, self._base)
		return self._ueCapability

	@property
	def hetbInfo(self):
		"""hetbInfo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hetbInfo'):
			from .Sta_.HetbInfo import HetbInfo
			self._hetbInfo = HetbInfo(self._core, self._base)
		return self._hetbInfo

	def clone(self) -> 'Sta':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sta(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
