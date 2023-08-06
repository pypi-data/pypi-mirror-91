from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccode:
	"""Ccode commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccode", core, parent)

	# noinspection PyTypeChecker
	def get_cc_state(self) -> enums.EnableState:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:CCODe:CCSTate \n
		Snippet: value: enums.EnableState = driver.configure.connection.ccode.get_cc_state() \n
		Enables/disables the broadcast of regulatory domain information in beacon frames. \n
			:return: state: DISable | ENABle
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:CCODe:CCSTate?')
		return Conversions.str_to_scalar_enum(response, enums.EnableState)

	def set_cc_state(self, state: enums.EnableState) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:CCODe:CCSTate \n
		Snippet: driver.configure.connection.ccode.set_cc_state(state = enums.EnableState.DISable) \n
		Enables/disables the broadcast of regulatory domain information in beacon frames. \n
			:param state: DISable | ENABle
		"""
		param = Conversions.enum_scalar_to_str(state, enums.EnableState)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:CCODe:CCSTate {param}')

	# noinspection PyTypeChecker
	class CcconfStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Code_Digit: str: string Country code as string
			- First_Channel: int: integer First in the range of allowed channels Range: 0 to 255
			- Nb_Of_Channels: int: integer Number of allowed channels Range: 0 to 255
			- Max_Tx_Power: int: integer Maximum transmit power Range: -40 dBm to 40 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_str('Code_Digit'),
			ArgStruct.scalar_int('First_Channel'),
			ArgStruct.scalar_int('Nb_Of_Channels'),
			ArgStruct.scalar_int('Max_Tx_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Code_Digit: str = None
			self.First_Channel: int = None
			self.Nb_Of_Channels: int = None
			self.Max_Tx_Power: int = None

	def get_ccconf(self) -> CcconfStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:CCODe:CCConf \n
		Snippet: value: CcconfStruct = driver.configure.connection.ccode.get_ccconf() \n
		Sets the regulatory domain information to be transmitted in beacon frames. To enable the transmission, see method
		RsCmwWlanSig.Configure.Connection.Ccode.ccState. \n
			:return: structure: for return value, see the help for CcconfStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:CCODe:CCConf?', self.__class__.CcconfStruct())

	def set_ccconf(self, value: CcconfStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:CCODe:CCConf \n
		Snippet: driver.configure.connection.ccode.set_ccconf(value = CcconfStruct()) \n
		Sets the regulatory domain information to be transmitted in beacon frames. To enable the transmission, see method
		RsCmwWlanSig.Configure.Connection.Ccode.ccState. \n
			:param value: see the help for CcconfStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:CCODe:CCConf', value)
