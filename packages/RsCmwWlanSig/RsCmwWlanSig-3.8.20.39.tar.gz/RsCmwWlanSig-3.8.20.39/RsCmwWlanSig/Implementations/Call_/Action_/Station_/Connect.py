from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Connect:
	"""Connect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("connect", core, parent)

	def set(self) -> None:
		"""SCPI: CALL:WLAN:SIGNaling<Instance>:ACTion:STATion:CONNect \n
		Snippet: driver.call.action.station.connect.set() \n
		Initiates an association to the AP under test. The command is only relevant in the operation mode 'Station' with
		connection mode 'Manual'. \n
		"""
		self._core.io.write(f'CALL:WLAN:SIGNaling<Instance>:ACTion:STATion:CONNect')

	def set_with_opc(self) -> None:
		"""SCPI: CALL:WLAN:SIGNaling<Instance>:ACTion:STATion:CONNect \n
		Snippet: driver.call.action.station.connect.set_with_opc() \n
		Initiates an association to the AP under test. The command is only relevant in the operation mode 'Station' with
		connection mode 'Manual'. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwWlanSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALL:WLAN:SIGNaling<Instance>:ACTion:STATion:CONNect')
