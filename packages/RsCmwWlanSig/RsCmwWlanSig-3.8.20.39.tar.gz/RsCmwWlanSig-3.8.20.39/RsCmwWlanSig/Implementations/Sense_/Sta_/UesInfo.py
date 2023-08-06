from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UesInfo:
	"""UesInfo commands group definition. 10 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uesInfo", core, parent)

	@property
	def rxbPower(self):
		"""rxbPower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxbPower'):
			from .UesInfo_.RxbPower import RxbPower
			self._rxbPower = RxbPower(self._core, self._base)
		return self._rxbPower

	@property
	def drate(self):
		"""drate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_drate'):
			from .UesInfo_.Drate import Drate
			self._drate = Drate(self._core, self._base)
		return self._drate

	@property
	def absReport(self):
		"""absReport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_absReport'):
			from .UesInfo_.AbsReport import AbsReport
			self._absReport = AbsReport(self._core, self._base)
		return self._absReport

	@property
	def rxPsdu(self):
		"""rxPsdu commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rxPsdu'):
			from .UesInfo_.RxPsdu import RxPsdu
			self._rxPsdu = RxPsdu(self._core, self._base)
		return self._rxPsdu

	@property
	def ueAddress(self):
		"""ueAddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ueAddress'):
			from .UesInfo_.UeAddress import UeAddress
			self._ueAddress = UeAddress(self._core, self._base)
		return self._ueAddress

	def clone(self) -> 'UesInfo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UesInfo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
