from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MimFading:
	"""MimFading commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mimFading", core, parent)

	# noinspection PyTypeChecker
	class FlexibleStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pcc_Bb_Board: enums.PccBasebandBoard: Signaling unit
			- Rx_Connector: enums.RxConnector: RF connector for the input path 1
			- Rx_Converter: enums.RxConverter: RX module for the input path 1
			- Tx_Connector: enums.TxConnector: RF connector for the output path 1
			- Tx_Converter: enums.TxConverter: TX module for the output path 1
			- Tx_2_Connector: enums.TxConnector: RF connector for the output path 2
			- Tx_2_Converter: enums.TxConverter: TX module for the output path 2
			- Rx_2_Connector: enums.RxConnector: RF connector for the input path 2
			- Rx_2_Converter: enums.RxConverter: RX module for the input path 2
			- Pcc_Fading_Board: enums.PccFadingBoard: Internal fader"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Pcc_Bb_Board', enums.PccBasebandBoard),
			ArgStruct.scalar_enum('Rx_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rx_Converter', enums.RxConverter),
			ArgStruct.scalar_enum('Tx_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Tx_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Tx_2_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Tx_2_Converter', enums.TxConverter),
			ArgStruct.scalar_enum('Rx_2_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rx_2_Converter', enums.RxConverter),
			ArgStruct.scalar_enum('Pcc_Fading_Board', enums.PccFadingBoard)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pcc_Bb_Board: enums.PccBasebandBoard = None
			self.Rx_Connector: enums.RxConnector = None
			self.Rx_Converter: enums.RxConverter = None
			self.Tx_Connector: enums.TxConnector = None
			self.Tx_Converter: enums.TxConverter = None
			self.Tx_2_Connector: enums.TxConnector = None
			self.Tx_2_Converter: enums.TxConverter = None
			self.Rx_2_Connector: enums.RxConnector = None
			self.Rx_2_Converter: enums.RxConverter = None
			self.Pcc_Fading_Board: enums.PccFadingBoard = None

	# noinspection PyTypeChecker
	def get_flexible(self) -> FlexibleStruct:
		"""SCPI: ROUTe:WLAN:SIGNaling<instance>:SCENario:MIMFading:FLEXible \n
		Snippet: value: FlexibleStruct = driver.route.scenario.mimFading.get_flexible() \n
		Activates the 'MIMO 2x2 Fading' scenario and selects the signal paths. For possible parameter values, see 'Values for
		Signal Path Selection'. \n
			:return: structure: for return value, see the help for FlexibleStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:WLAN:SIGNaling<Instance>:SCENario:MIMFading:FLEXible?', self.__class__.FlexibleStruct())

	def set_flexible(self, value: FlexibleStruct) -> None:
		"""SCPI: ROUTe:WLAN:SIGNaling<instance>:SCENario:MIMFading:FLEXible \n
		Snippet: driver.route.scenario.mimFading.set_flexible(value = FlexibleStruct()) \n
		Activates the 'MIMO 2x2 Fading' scenario and selects the signal paths. For possible parameter values, see 'Values for
		Signal Path Selection'. \n
			:param value: see the help for FlexibleStruct structure arguments.
		"""
		self._core.io.write_struct('ROUTe:WLAN:SIGNaling<Instance>:SCENario:MIMFading:FLEXible', value)
