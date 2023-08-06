from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tenable:
	"""Tenable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tenable", core, parent)

	def set(self, flow_id: int, enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:BTWT:SCHedule:TENable \n
		Snippet: driver.configure.connection.btwt.schedule.tenable.set(flow_id = 1, enable = False) \n
		Enables/disables the broadcast TWT trigger for the specified schedule period. \n
			:param flow_id: integer
			:param enable: OFF | ON
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('flow_id', flow_id, DataType.Integer), ArgSingle('enable', enable, DataType.Boolean))
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:BTWT:SCHedule:TENable {param}'.rstrip())

	def get(self, flow_id: int) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:BTWT:SCHedule:TENable \n
		Snippet: value: bool = driver.configure.connection.btwt.schedule.tenable.get(flow_id = 1) \n
		Enables/disables the broadcast TWT trigger for the specified schedule period. \n
			:param flow_id: integer
			:return: enable: OFF | ON"""
		param = Conversions.decimal_value_to_str(flow_id)
		response = self._core.io.query_str(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:BTWT:SCHedule:TENable? {param}')
		return Conversions.str_to_bool(response)
