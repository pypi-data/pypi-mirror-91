from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Antenna:
	"""Antenna commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Antenna, default value after init: Antenna.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("antenna", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_antenna_get', 'repcap_antenna_set', repcap.Antenna.Nr1)

	def repcap_antenna_set(self, enum_value: repcap.Antenna) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Antenna.Default
		Default value after init: Antenna.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_antenna_get(self) -> repcap.Antenna:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def rxpIndicator(self):
		"""rxpIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxpIndicator'):
			from .Antenna_.RxpIndicator import RxpIndicator
			self._rxpIndicator = RxpIndicator(self._core, self._base)
		return self._rxpIndicator

	def clone(self) -> 'Antenna':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Antenna(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
