from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ipv:
	"""Ipv commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ipv", core, parent)

	def get(self, ipVersion=repcap.IpVersion.Default) -> str:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:UESinfo:CMWaddress:IPV<n> \n
		Snippet: value: str = driver.sense.uesInfo.cmwAddress.ipv.get(ipVersion = repcap.IpVersion.Default) \n
		Queries the IP address of the R&S CMW. \n
			:param ipVersion: optional repeated capability selector. Default value: V4 (settable in the interface 'CmwAddress')
			:return: ip_address: string The assigned IPv4 or IPv6 addresses."""
		ipVersion_cmd_val = self._base.get_repcap_cmd_value(ipVersion, repcap.IpVersion)
		response = self._core.io.query_str(f'SENSe:WLAN:SIGNaling<Instance>:UESinfo:CMWaddress:IPV{ipVersion_cmd_val}?')
		return trim_str_response(response)
