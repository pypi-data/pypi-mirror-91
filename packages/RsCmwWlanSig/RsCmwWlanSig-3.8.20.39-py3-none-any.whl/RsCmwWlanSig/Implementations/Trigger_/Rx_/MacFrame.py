from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MacFrame:
	"""MacFrame commands group definition. 11 total commands, 1 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("macFrame", core, parent)

	@property
	def plength(self):
		"""plength commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_plength'):
			from .MacFrame_.Plength import Plength
			self._plength = Plength(self._core, self._base)
		return self._plength

	# noinspection PyTypeChecker
	class DsmLengthStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Mode: enums.LenMode: DEFault | UDEFined DEFault: automatically calculated value UDEFined: configured Length
			- Length: int: numeric Minimum number of bytes for UDEFined mode Range: 16 to 1500, Unit: byte"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Mode', enums.LenMode),
			ArgStruct.scalar_int('Length')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mode: enums.LenMode = None
			self.Length: int = None

	# noinspection PyTypeChecker
	def get_dsm_length(self) -> DsmLengthStruct:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:DSMLength \n
		Snippet: value: DsmLengthStruct = driver.trigger.rx.macFrame.get_dsm_length() \n
		Defines the minimum length for the RX frame trigger mode DSSS/CCK Bursts, see method RsCmwWlanSig.Trigger.Rx.MacFrame.
		btype. \n
			:return: structure: for return value, see the help for DsmLengthStruct structure arguments.
		"""
		return self._core.io.query_struct('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:DSMLength?', self.__class__.DsmLengthStruct())

	def set_dsm_length(self, value: DsmLengthStruct) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:DSMLength \n
		Snippet: driver.trigger.rx.macFrame.set_dsm_length(value = DsmLengthStruct()) \n
		Defines the minimum length for the RX frame trigger mode DSSS/CCK Bursts, see method RsCmwWlanSig.Trigger.Rx.MacFrame.
		btype. \n
			:param value: see the help for DsmLengthStruct structure arguments.
		"""
		self._core.io.write_struct('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:DSMLength', value)

	# noinspection PyTypeChecker
	class OfmLengthStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Mode: enums.LenMode: DEFault | UDEFined DEFault: automatically calculated value UDEFined: configured Length
			- Length: int: numeric Range: 1 to 1500"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Mode', enums.LenMode),
			ArgStruct.scalar_int('Length')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mode: enums.LenMode = None
			self.Length: int = None

	# noinspection PyTypeChecker
	def get_ofm_length(self) -> OfmLengthStruct:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:OFMLength \n
		Snippet: value: OfmLengthStruct = driver.trigger.rx.macFrame.get_ofm_length() \n
		Defines the minimum length for the all OFDM RX frame trigger modes (all modes except All Bursts and DSSS/CCK Bursts) ,
		see method RsCmwWlanSig.Trigger.Rx.MacFrame.btype. \n
			:return: structure: for return value, see the help for OfmLengthStruct structure arguments.
		"""
		return self._core.io.query_struct('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:OFMLength?', self.__class__.OfmLengthStruct())

	def set_ofm_length(self, value: OfmLengthStruct) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:OFMLength \n
		Snippet: driver.trigger.rx.macFrame.set_ofm_length(value = OfmLengthStruct()) \n
		Defines the minimum length for the all OFDM RX frame trigger modes (all modes except All Bursts and DSSS/CCK Bursts) ,
		see method RsCmwWlanSig.Trigger.Rx.MacFrame.btype. \n
			:param value: see the help for OfmLengthStruct structure arguments.
		"""
		self._core.io.write_struct('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:OFMLength', value)

	# noinspection PyTypeChecker
	def get_btype(self) -> enums.BurstType:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:BTYPe \n
		Snippet: value: enums.BurstType = driver.trigger.rx.macFrame.get_btype() \n
		Defines for which bursts a trigger pulse is generated for the RX frame trigger signal. Note that the trigger pulse is
		generated only for bursts matching the specified trigger bandwidth and trigger rate, see: method RsCmwWlanSig.Trigger.Rx.
		MacFrame.bw method RsCmwWlanSig.Trigger.Rx.MacFrame.rate \n
			:return: type_py: ABURsts | OBURsts | DCBursts | NHTBursts | HTBursts | VHTBursts | HESBursts ABURsts All received bursts result in an RX frame trigger pulse. OBURsts Only OFDM bursts with the configured minimum length result in an RX frame trigger pulse. DCBursts Only DSSS/CCK bursts with the configured minimum length result in an RX frame trigger pulse. NHTBursts Only non-HT bursts with the configured minimum length result in an RX frame trigger pulse. HTBursts Only HT bursts with the configured minimum length result in an RX frame trigger pulse. VHTBursts Only VHT bursts with the configured minimum length result in an RX frame trigger pulse. HESBursts Only HE SU bursts with the configured minimum length result in an RX frame trigger pulse.
		"""
		response = self._core.io.query_str('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:BTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BurstType)

	def set_btype(self, type_py: enums.BurstType) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:BTYPe \n
		Snippet: driver.trigger.rx.macFrame.set_btype(type_py = enums.BurstType.ABURsts) \n
		Defines for which bursts a trigger pulse is generated for the RX frame trigger signal. Note that the trigger pulse is
		generated only for bursts matching the specified trigger bandwidth and trigger rate, see: method RsCmwWlanSig.Trigger.Rx.
		MacFrame.bw method RsCmwWlanSig.Trigger.Rx.MacFrame.rate \n
			:param type_py: ABURsts | OBURsts | DCBursts | NHTBursts | HTBursts | VHTBursts | HESBursts ABURsts All received bursts result in an RX frame trigger pulse. OBURsts Only OFDM bursts with the configured minimum length result in an RX frame trigger pulse. DCBursts Only DSSS/CCK bursts with the configured minimum length result in an RX frame trigger pulse. NHTBursts Only non-HT bursts with the configured minimum length result in an RX frame trigger pulse. HTBursts Only HT bursts with the configured minimum length result in an RX frame trigger pulse. VHTBursts Only VHT bursts with the configured minimum length result in an RX frame trigger pulse. HESBursts Only HE SU bursts with the configured minimum length result in an RX frame trigger pulse.
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.BurstType)
		self._core.io.write(f'TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:BTYPe {param}')

	# noinspection PyTypeChecker
	def get_bw(self) -> enums.TriggerBandwidth:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:BW \n
		Snippet: value: enums.TriggerBandwidth = driver.trigger.rx.macFrame.get_bw() \n
		Defines for which bandwidth of received bursts a trigger pulse is generated for the RX frame trigger signal. \n
			:return: trigger_bandwidth: BW20 | BW40 | BW80 | BW160 | ALL | ON | OFF BWx: RX frame trigger signal generated for the received bursts with the bandwidth of x MHz ALL: RX frame trigger signal generated for all bandwidths ON: RX frame trigger signal switched on OFF: RX frame trigger signal switched off
		"""
		response = self._core.io.query_str('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:BW?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerBandwidth)

	def set_bw(self, trigger_bandwidth: enums.TriggerBandwidth) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:BW \n
		Snippet: driver.trigger.rx.macFrame.set_bw(trigger_bandwidth = enums.TriggerBandwidth.ALL) \n
		Defines for which bandwidth of received bursts a trigger pulse is generated for the RX frame trigger signal. \n
			:param trigger_bandwidth: BW20 | BW40 | BW80 | BW160 | ALL | ON | OFF BWx: RX frame trigger signal generated for the received bursts with the bandwidth of x MHz ALL: RX frame trigger signal generated for all bandwidths ON: RX frame trigger signal switched on OFF: RX frame trigger signal switched off
		"""
		param = Conversions.enum_scalar_to_str(trigger_bandwidth, enums.TriggerBandwidth)
		self._core.io.write(f'TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:BW {param}')

	# noinspection PyTypeChecker
	def get_streams(self) -> enums.SpatialStreams:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:STReams \n
		Snippet: value: enums.SpatialStreams = driver.trigger.rx.macFrame.get_streams() \n
		Sets the spatial streams for RX frame trigger for MIMO connections. \n
			:return: spatial_streams: ALL | STR1 | STR2 | ON | OFF Both streams, stream 1, or stream 2 used for the trigger signal
		"""
		response = self._core.io.query_str('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:STReams?')
		return Conversions.str_to_scalar_enum(response, enums.SpatialStreams)

	def set_streams(self, spatial_streams: enums.SpatialStreams) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:STReams \n
		Snippet: driver.trigger.rx.macFrame.set_streams(spatial_streams = enums.SpatialStreams.ALL) \n
		Sets the spatial streams for RX frame trigger for MIMO connections. \n
			:param spatial_streams: ALL | STR1 | STR2 | ON | OFF Both streams, stream 1, or stream 2 used for the trigger signal
		"""
		param = Conversions.enum_scalar_to_str(spatial_streams, enums.SpatialStreams)
		self._core.io.write(f'TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:STReams {param}')

	# noinspection PyTypeChecker
	def get_rate(self) -> enums.TriggerRate:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:RATE \n
		Snippet: value: enums.TriggerRate = driver.trigger.rx.macFrame.get_rate() \n
		Defines for which rate of received bursts a trigger pulse is generated for the RX frame trigger signal. \n
			:return: trigger_rate: BR12 | QR12 | QR34 | Q1M12 | Q1M34 | Q6M23 | Q6M34 | BR34 | MCS0 | MCS1 | MCS2 | MCS3 | MCS4 | MCS5 | MCS6 | MCS7 | D1MBit | D2MBits | C55Mbits | C11Mbits | MCS8 | MCS9 | MCS10 | MCS11 | MCS12 | MCS13 | MCS14 | MCS15 | ALL | ON | OFF D1MBit: DSSS, 1 Mbit/s D2MBits: DSSS, 2 Mbit/s C55Mbits: CCK, 5.5 Mbit/s C11Mbits: CCK, 11 Mbit/s BR12: BPSK, 1/2, 6 Mbit/s BR34: BPSK, 3/4, 9 Mbit/s QR12: QPSK, 1/2, 12 Mbit/s QR34: QPSK, 3/4, 18 Mbit/s Q1M12: 16-QAM, 1/2, 24 Mbit/s Q1M34: 16-QAM, 3/4, 36 Mbit/s Q6M23: 64-QAM, 2/3, 48 Mbit/s Q6M34: 64-QAM, 3/4, 54 Mbit/s MCS, MCS1,...,MCS15: MCS 0 to MCS 15 ALL: RX frame trigger signal generated for all rates ON: RX frame trigger signal switched on OFF: RX frame trigger signal switched off
		"""
		response = self._core.io.query_str('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:RATE?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerRate)

	def set_rate(self, trigger_rate: enums.TriggerRate) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:RATE \n
		Snippet: driver.trigger.rx.macFrame.set_rate(trigger_rate = enums.TriggerRate.ALL) \n
		Defines for which rate of received bursts a trigger pulse is generated for the RX frame trigger signal. \n
			:param trigger_rate: BR12 | QR12 | QR34 | Q1M12 | Q1M34 | Q6M23 | Q6M34 | BR34 | MCS0 | MCS1 | MCS2 | MCS3 | MCS4 | MCS5 | MCS6 | MCS7 | D1MBit | D2MBits | C55Mbits | C11Mbits | MCS8 | MCS9 | MCS10 | MCS11 | MCS12 | MCS13 | MCS14 | MCS15 | ALL | ON | OFF D1MBit: DSSS, 1 Mbit/s D2MBits: DSSS, 2 Mbit/s C55Mbits: CCK, 5.5 Mbit/s C11Mbits: CCK, 11 Mbit/s BR12: BPSK, 1/2, 6 Mbit/s BR34: BPSK, 3/4, 9 Mbit/s QR12: QPSK, 1/2, 12 Mbit/s QR34: QPSK, 3/4, 18 Mbit/s Q1M12: 16-QAM, 1/2, 24 Mbit/s Q1M34: 16-QAM, 3/4, 36 Mbit/s Q6M23: 64-QAM, 2/3, 48 Mbit/s Q6M34: 64-QAM, 3/4, 54 Mbit/s MCS, MCS1,...,MCS15: MCS 0 to MCS 15 ALL: RX frame trigger signal generated for all rates ON: RX frame trigger signal switched on OFF: RX frame trigger signal switched off
		"""
		param = Conversions.enum_scalar_to_str(trigger_rate, enums.TriggerRate)
		self._core.io.write(f'TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:RATE {param}')

	# noinspection PyTypeChecker
	def get_ct_delay(self) -> enums.DelayType:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:CTDelay \n
		Snippet: value: enums.DelayType = driver.trigger.rx.macFrame.get_ct_delay() \n
		Sets the trigger delay type burst (automatic configuration) or constant delay of 200 µs for RX frame trigger, OFDM. \n
			:return: delay_type: BURSt | CONStant
		"""
		response = self._core.io.query_str('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:CTDelay?')
		return Conversions.str_to_scalar_enum(response, enums.DelayType)

	def set_ct_delay(self, delay_type: enums.DelayType) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:CTDelay \n
		Snippet: driver.trigger.rx.macFrame.set_ct_delay(delay_type = enums.DelayType.BURSt) \n
		Sets the trigger delay type burst (automatic configuration) or constant delay of 200 µs for RX frame trigger, OFDM. \n
			:param delay_type: BURSt | CONStant
		"""
		param = Conversions.enum_scalar_to_str(delay_type, enums.DelayType)
		self._core.io.write(f'TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:CTDelay {param}')

	def get_rrestriction(self) -> bool:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:RREStriction \n
		Snippet: value: bool = driver.trigger.rx.macFrame.get_rrestriction() \n
		Enables or disables the rate control of the DUT. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:RREStriction?')
		return Conversions.str_to_bool(response)

	def set_rrestriction(self, enable: bool) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:RREStriction \n
		Snippet: driver.trigger.rx.macFrame.set_rrestriction(enable = False) \n
		Enables or disables the rate control of the DUT. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:RREStriction {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.TriggerSlope:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:SLOPe \n
		Snippet: value: enums.TriggerSlope = driver.trigger.rx.macFrame.get_slope() \n
		Aligns either the rising edge or the falling edge of the trigger pulses with the start of the MAC frames. \n
			:return: trig_slope: REDGe | FEDGe
		"""
		response = self._core.io.query_str('TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSlope)

	def set_slope(self, trig_slope: enums.TriggerSlope) -> None:
		"""SCPI: TRIGger:WLAN:SIGNaling<instance>:RX:MACFrame:SLOPe \n
		Snippet: driver.trigger.rx.macFrame.set_slope(trig_slope = enums.TriggerSlope.FEDGe) \n
		Aligns either the rising edge or the falling edge of the trigger pulses with the start of the MAC frames. \n
			:param trig_slope: REDGe | FEDGe
		"""
		param = Conversions.enum_scalar_to_str(trig_slope, enums.TriggerSlope)
		self._core.io.write(f'TRIGger:WLAN:SIGNaling<Instance>:RX:MACFrame:SLOPe {param}')

	def clone(self) -> 'MacFrame':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MacFrame(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
