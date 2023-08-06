from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal.StructBase import StructBase
from ..Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Per:
	"""Per commands group definition. 7 total commands, 1 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("per", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Per_.State import State
			self._state = State(self._core, self._base)
		return self._state

	# noinspection PyTypeChecker
	class ReadStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Per: float: float Range: 0 % to 100 %
			- Current_No_Frames: int: No parameter help available
			- Frames_Lost: int: No parameter help available
			- Frame_Transmitted: int: No parameter help available
			- Rx_Burst_Power: float: float Average received burst power of uplink ACK frames Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_int('Current_No_Frames'),
			ArgStruct.scalar_int('Frames_Lost'),
			ArgStruct.scalar_int('Frame_Transmitted'),
			ArgStruct.scalar_float('Rx_Burst_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Current_No_Frames: int = None
			self.Frames_Lost: int = None
			self.Frame_Transmitted: int = None
			self.Rx_Burst_Power: float = None

	def read(self) -> ReadStruct:
		"""SCPI: READ:WLAN:SIGNaling<instance>:PER \n
		Snippet: value: ReadStruct = driver.per.read() \n
		Returns all results of the PER measurement. \n
			:return: structure: for return value, see the help for ReadStruct structure arguments."""
		return self._core.io.query_struct(f'READ:WLAN:SIGNaling<Instance>:PER?', self.__class__.ReadStruct())

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Per: float: float Range: 0 % to 100 %
			- Current_No_Frames: int: No parameter help available
			- Frames_Lost: int: No parameter help available
			- Rx_Burst_Power: float: float Average received burst power of uplink ACK frames Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_int('Current_No_Frames'),
			ArgStruct.scalar_int('Frames_Lost'),
			ArgStruct.scalar_float('Rx_Burst_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Current_No_Frames: int = None
			self.Frames_Lost: int = None
			self.Rx_Burst_Power: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:WLAN:SIGNaling<instance>:PER \n
		Snippet: value: FetchStruct = driver.per.fetch() \n
		Returns all results of the PER measurement. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:WLAN:SIGNaling<Instance>:PER?', self.__class__.FetchStruct())

	def stop(self) -> None:
		"""SCPI: STOP:WLAN:SIGNaling<instance>:PER \n
		Snippet: driver.per.stop() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'STOP:WLAN:SIGNaling<Instance>:PER')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:WLAN:SIGNaling<instance>:PER \n
		Snippet: driver.per.stop_with_opc() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCmwWlanSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:WLAN:SIGNaling<Instance>:PER')

	def abort(self) -> None:
		"""SCPI: ABORt:WLAN:SIGNaling<instance>:PER \n
		Snippet: driver.per.abort() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'ABORt:WLAN:SIGNaling<Instance>:PER')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:WLAN:SIGNaling<instance>:PER \n
		Snippet: driver.per.abort_with_opc() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCmwWlanSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:WLAN:SIGNaling<Instance>:PER')

	def initiate(self) -> None:
		"""SCPI: INITiate:WLAN:SIGNaling<instance>:PER \n
		Snippet: driver.per.initiate() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'INITiate:WLAN:SIGNaling<Instance>:PER')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:WLAN:SIGNaling<instance>:PER \n
		Snippet: driver.per.initiate_with_opc() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCmwWlanSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:WLAN:SIGNaling<Instance>:PER')

	def clone(self) -> 'Per':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Per(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
