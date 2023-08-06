from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ampdu:
	"""Ampdu commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ampdu", core, parent)

	# noinspection PyTypeChecker
	class AmpduStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Enable: enums.EnableState: DISable | ENABle Enables/ disables the A-MPDUs
			- Multi_Tid: enums.EnableState: DISable | ENABle Enables/ disables multi-TID A-MPDU
			- Max_Length: int: integer The maximal length of entire A-MPDU Range: 50 to 131.071E+3, Unit: byte"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Enable', enums.EnableState),
			ArgStruct.scalar_enum('Multi_Tid', enums.EnableState),
			ArgStruct.scalar_int('Max_Length')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: enums.EnableState = None
			self.Multi_Tid: enums.EnableState = None
			self.Max_Length: int = None

	def set(self, structure: AmpduStruct, station=repcap.Station.Default) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:STA<s>:CONNection:AMPDu \n
		Snippet: driver.configure.sta.connection.ampdu.set(value = [PROPERTY_STRUCT_NAME](), station = repcap.Station.Default) \n
		Configures aggregate MPDUs (A-MPDU) . \n
			:param structure: for set value, see the help for AmpduStruct structure arguments.
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sta')"""
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		self._core.io.write_struct(f'CONFigure:WLAN:SIGNaling<Instance>:STA{station_cmd_val}:CONNection:AMPDu', structure)

	def get(self, station=repcap.Station.Default) -> AmpduStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:STA<s>:CONNection:AMPDu \n
		Snippet: value: AmpduStruct = driver.configure.sta.connection.ampdu.get(station = repcap.Station.Default) \n
		Configures aggregate MPDUs (A-MPDU) . \n
			:param station: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sta')
			:return: structure: for return value, see the help for AmpduStruct structure arguments."""
		station_cmd_val = self._base.get_repcap_cmd_value(station, repcap.Station)
		return self._core.io.query_struct(f'CONFigure:WLAN:SIGNaling<Instance>:STA{station_cmd_val}:CONNection:AMPDu?', self.__class__.AmpduStruct())
