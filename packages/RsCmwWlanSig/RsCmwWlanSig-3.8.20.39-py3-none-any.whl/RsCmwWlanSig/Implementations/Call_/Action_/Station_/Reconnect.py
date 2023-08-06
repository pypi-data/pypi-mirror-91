from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reconnect:
	"""Reconnect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reconnect", core, parent)

	def set(self) -> None:
		"""SCPI: CALL:WLAN:SIGNaling<Instance>:ACTion:STATion:REConnect \n
		Snippet: driver.call.action.station.reconnect.set() \n
		Re-establishes the existing association to the AP under test. The command has the same effect as a disconnect, followed
		immediately by a connect. The command is only relevant in the operation mode 'Station' with connection mode 'Manual'. \n
		"""
		self._core.io.write(f'CALL:WLAN:SIGNaling<Instance>:ACTion:STATion:REConnect')

	def set_with_opc(self) -> None:
		"""SCPI: CALL:WLAN:SIGNaling<Instance>:ACTion:STATion:REConnect \n
		Snippet: driver.call.action.station.reconnect.set_with_opc() \n
		Re-establishes the existing association to the AP under test. The command has the same effect as a disconnect, followed
		immediately by a connect. The command is only relevant in the operation mode 'Station' with connection mode 'Manual'. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwWlanSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALL:WLAN:SIGNaling<Instance>:ACTion:STATion:REConnect')
