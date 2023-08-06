from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MacFrame:
	"""MacFrame commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("macFrame", core, parent)

	@property
	def plength(self):
		"""plength commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_plength'):
			from .MacFrame_.Plength import Plength
			self._plength = Plength(self._core, self._base)
		return self._plength

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.TriggerSlope:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:TX:MACFrame:SLOPe \n
		Snippet: value: enums.TriggerSlope = driver.trigger.tx.macFrame.get_slope() \n
		Aligns either the rising edge or the falling edge of the trigger pulses with the start of the MAC frames. \n
			:return: trig_slope: REDGe | FEDGe
		"""
		response = self._core.io.query_str('TRIGger:WLAN:SIGNaling<Instance>:TX:MACFrame:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSlope)

	def set_slope(self, trig_slope: enums.TriggerSlope) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:TX:MACFrame:SLOPe \n
		Snippet: driver.trigger.tx.macFrame.set_slope(trig_slope = enums.TriggerSlope.FEDGe) \n
		Aligns either the rising edge or the falling edge of the trigger pulses with the start of the MAC frames. \n
			:param trig_slope: REDGe | FEDGe
		"""
		param = Conversions.enum_scalar_to_str(trig_slope, enums.TriggerSlope)
		self._core.io.write(f'TRIGger:WLAN:SIGNaling<Instance>:TX:MACFrame:SLOPe {param}')

	def clone(self) -> 'MacFrame':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MacFrame(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
