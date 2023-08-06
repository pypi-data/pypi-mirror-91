from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ipv6:
	"""Ipv6 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ipv6", core, parent)

	def get_prefix(self) -> str:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVSix:PREFix \n
		Snippet: value: str = driver.configure.ipv6.get_prefix() \n
		Defines the IPv6 prefix of the built-in IPv6 stack. \n
			:return: prefix: string IPv6 prefix as string
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:IPVSix:PREFix?')
		return trim_str_response(response)

	def set_prefix(self, prefix: str) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:IPVSix:PREFix \n
		Snippet: driver.configure.ipv6.set_prefix(prefix = '1') \n
		Defines the IPv6 prefix of the built-in IPv6 stack. \n
			:param prefix: string IPv6 prefix as string
		"""
		param = Conversions.value_to_quoted_str(prefix)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:IPVSix:PREFix {param}')
