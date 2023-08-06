from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Disconnect:
	"""Disconnect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("disconnect", core, parent)

	def set(self, station=repcap.Station.Default) -> None:
		"""SCPI: CALL:WLAN:SIGNaling<Instance>:STA<s>:ACTion:DISConnect \n
		Snippet: driver.call.sta.action.disconnect.set(station = repcap.Station.Default) \n
		Disassociates and deauthenticates the DUT by sending a deauthentication frame. \n
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sta')"""
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		self._core.io.write(f'CALL:WLAN:SIGNaling<Instance>:STA{station_cmd_val}:ACTion:DISConnect')

	def set_with_opc(self, station=repcap.Station.Default) -> None:
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		"""SCPI: CALL:WLAN:SIGNaling<Instance>:STA<s>:ACTion:DISConnect \n
		Snippet: driver.call.sta.action.disconnect.set_with_opc(station = repcap.Station.Default) \n
		Disassociates and deauthenticates the DUT by sending a deauthentication frame. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwWlanSig.utilities.opc_timeout_set() to set the timeout value. \n
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sta')"""
		self._core.io.write_with_opc(f'CALL:WLAN:SIGNaling<Instance>:STA{station_cmd_val}:ACTion:DISConnect')
