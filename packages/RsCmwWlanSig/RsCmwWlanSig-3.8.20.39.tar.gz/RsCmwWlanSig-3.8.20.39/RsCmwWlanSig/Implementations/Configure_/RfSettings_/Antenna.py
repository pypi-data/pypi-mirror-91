from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Antenna:
	"""Antenna commands group definition. 4 total commands, 3 Sub-groups, 0 group commands
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
	def mlOffset(self):
		"""mlOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mlOffset'):
			from .Antenna_.MlOffset import MlOffset
			self._mlOffset = MlOffset(self._core, self._base)
		return self._mlOffset

	@property
	def epePower(self):
		"""epePower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_epePower'):
			from .Antenna_.EpePower import EpePower
			self._epePower = EpePower(self._core, self._base)
		return self._epePower

	@property
	def eattenuation(self):
		"""eattenuation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_eattenuation'):
			from .Antenna_.Eattenuation import Eattenuation
			self._eattenuation = Eattenuation(self._core, self._base)
		return self._eattenuation

	def clone(self) -> 'Antenna':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Antenna(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
