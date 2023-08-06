from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SsTx:
	"""SsTx commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssTx", core, parent)

	def set(self) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:NDPSounding:SSTX \n
		Snippet: driver.configure.connection.ndpSounding.ssTx.set() \n
		Triggers the single-shot transmission for NDP sounding procedure. \n
		"""
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:NDPSounding:SSTX')

	def set_with_opc(self) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:NDPSounding:SSTX \n
		Snippet: driver.configure.connection.ndpSounding.ssTx.set_with_opc() \n
		Triggers the single-shot transmission for NDP sounding procedure. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwWlanSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:NDPSounding:SSTX')
