from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Srates:
	"""Srates commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srates", core, parent)

	# noinspection PyTypeChecker
	def get_vht_conf(self) -> enums.VhtRates:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes:VHTConf \n
		Snippet: value: enums.VhtRates = driver.configure.connection.srates.get_vht_conf() \n
		Definition of supported OFDM VHT modulation and coding schemes (MCS) . These settings apply only if user-defined
		supported rates are enabled, see method RsCmwWlanSig.Configure.Connection.Srates.value. \n
			:return: vht_rates: MC07 | MC08 | MC09 MC07: MCS 0 to MCS 7 MC08: MCS 0 to MCS 8 MC09: MCS 0 to MCS 9
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes:VHTConf?')
		return Conversions.str_to_scalar_enum(response, enums.VhtRates)

	def set_vht_conf(self, vht_rates: enums.VhtRates) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes:VHTConf \n
		Snippet: driver.configure.connection.srates.set_vht_conf(vht_rates = enums.VhtRates.MC07) \n
		Definition of supported OFDM VHT modulation and coding schemes (MCS) . These settings apply only if user-defined
		supported rates are enabled, see method RsCmwWlanSig.Configure.Connection.Srates.value. \n
			:param vht_rates: MC07 | MC08 | MC09 MC07: MCS 0 to MCS 7 MC08: MCS 0 to MCS 8 MC09: MCS 0 to MCS 9
		"""
		param = Conversions.enum_scalar_to_str(vht_rates, enums.VhtRates)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes:VHTConf {param}')

	# noinspection PyTypeChecker
	class OmcsConfStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Mcs_0: enums.McsSupport: NOTSupported | SUPPorted
			- Mcs_1: enums.McsSupport: NOTSupported | SUPPorted
			- Mcs_2: enums.McsSupport: NOTSupported | SUPPorted
			- Mcs_3: enums.McsSupport: NOTSupported | SUPPorted
			- Mcs_4: enums.McsSupport: NOTSupported | SUPPorted
			- Mcs_5: enums.McsSupport: NOTSupported | SUPPorted
			- Mcs_6: enums.McsSupport: NOTSupported | SUPPorted
			- Mcs_7: enums.McsSupport: NOTSupported | SUPPorted"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Mcs_0', enums.McsSupport),
			ArgStruct.scalar_enum('Mcs_1', enums.McsSupport),
			ArgStruct.scalar_enum('Mcs_2', enums.McsSupport),
			ArgStruct.scalar_enum('Mcs_3', enums.McsSupport),
			ArgStruct.scalar_enum('Mcs_4', enums.McsSupport),
			ArgStruct.scalar_enum('Mcs_5', enums.McsSupport),
			ArgStruct.scalar_enum('Mcs_6', enums.McsSupport),
			ArgStruct.scalar_enum('Mcs_7', enums.McsSupport)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mcs_0: enums.McsSupport = None
			self.Mcs_1: enums.McsSupport = None
			self.Mcs_2: enums.McsSupport = None
			self.Mcs_3: enums.McsSupport = None
			self.Mcs_4: enums.McsSupport = None
			self.Mcs_5: enums.McsSupport = None
			self.Mcs_6: enums.McsSupport = None
			self.Mcs_7: enums.McsSupport = None

	# noinspection PyTypeChecker
	def get_omcs_conf(self) -> OmcsConfStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes:OMCSconf \n
		Snippet: value: OmcsConfStruct = driver.configure.connection.srates.get_omcs_conf() \n
		Definition of supported OFDM HT modulation and coding schemes (MCS) . These settings apply only if user-defined supported
		rates are enabled, see method RsCmwWlanSig.Configure.Connection.Srates.value. \n
			:return: structure: for return value, see the help for OmcsConfStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes:OMCSconf?', self.__class__.OmcsConfStruct())

	def set_omcs_conf(self, value: OmcsConfStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes:OMCSconf \n
		Snippet: driver.configure.connection.srates.set_omcs_conf(value = OmcsConfStruct()) \n
		Definition of supported OFDM HT modulation and coding schemes (MCS) . These settings apply only if user-defined supported
		rates are enabled, see method RsCmwWlanSig.Configure.Connection.Srates.value. \n
			:param value: see the help for OmcsConfStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes:OMCSconf', value)

	# noinspection PyTypeChecker
	class OfdmConfStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Br_12: enums.RateSupport: DISabled | MANDatory | OPTional Support for BPSK, 1/2, 6 Mbit/s
			- Br_34: enums.RateSupport: DISabled | MANDatory | OPTional Support for BPSK, 3/4, 9 Mbit/s
			- Qr_12: enums.RateSupport: DISabled | MANDatory | OPTional Support for QPSK, 1/2, 12 Mbit/s
			- Qr_34: enums.RateSupport: DISabled | MANDatory | OPTional Support for QPSK, 3/4, 18 Mbit/s
			- Q_1_M_12: enums.RateSupport: DISabled | MANDatory | OPTional Support for 16-QAM, 1/2, 24 Mbit/s
			- Q_1_M_34: enums.RateSupport: DISabled | MANDatory | OPTional Support for 16-QAM, 3/4, 36 Mbit/s
			- Q_6_M_23: enums.RateSupport: DISabled | MANDatory | OPTional Support for 64-QAM, 2/3, 48 Mbit/s
			- Q_6_M_34: enums.RateSupport: DISabled | MANDatory | OPTional Support for 64-QAM, 3/4, 54 Mbit/s"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Br_12', enums.RateSupport),
			ArgStruct.scalar_enum('Br_34', enums.RateSupport),
			ArgStruct.scalar_enum('Qr_12', enums.RateSupport),
			ArgStruct.scalar_enum('Qr_34', enums.RateSupport),
			ArgStruct.scalar_enum('Q_1_M_12', enums.RateSupport),
			ArgStruct.scalar_enum('Q_1_M_34', enums.RateSupport),
			ArgStruct.scalar_enum('Q_6_M_23', enums.RateSupport),
			ArgStruct.scalar_enum('Q_6_M_34', enums.RateSupport)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Br_12: enums.RateSupport = None
			self.Br_34: enums.RateSupport = None
			self.Qr_12: enums.RateSupport = None
			self.Qr_34: enums.RateSupport = None
			self.Q_1_M_12: enums.RateSupport = None
			self.Q_1_M_34: enums.RateSupport = None
			self.Q_6_M_23: enums.RateSupport = None
			self.Q_6_M_34: enums.RateSupport = None

	# noinspection PyTypeChecker
	def get_ofdm_conf(self) -> OfdmConfStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes:OFDMconf \n
		Snippet: value: OfdmConfStruct = driver.configure.connection.srates.get_ofdm_conf() \n
		Definition of OFDM non-HT supported rates (modulation, coding rate, data rate) . These settings apply only if
		user-defined supported rates are enabled, see method RsCmwWlanSig.Configure.Connection.Srates.value. \n
			:return: structure: for return value, see the help for OfdmConfStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes:OFDMconf?', self.__class__.OfdmConfStruct())

	def set_ofdm_conf(self, value: OfdmConfStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes:OFDMconf \n
		Snippet: driver.configure.connection.srates.set_ofdm_conf(value = OfdmConfStruct()) \n
		Definition of OFDM non-HT supported rates (modulation, coding rate, data rate) . These settings apply only if
		user-defined supported rates are enabled, see method RsCmwWlanSig.Configure.Connection.Srates.value. \n
			:param value: see the help for OfdmConfStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes:OFDMconf', value)

	# noinspection PyTypeChecker
	class DsssConfStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- D_1_Mb: enums.RateSupport: DISabled | MANDatory | OPTional Support for DSSS, 1 Mbit/s
			- D_2_Mb: enums.RateSupport: DISabled | MANDatory | OPTional Support for DSSS, 2 Mbit/s
			- C_55_M: enums.RateSupport: DISabled | MANDatory | OPTional Support for CCK, 5.5 Mbit/s
			- C_11_M: enums.RateSupport: DISabled | MANDatory | OPTional Support for CCK, 11 Mbit/s"""
		__meta_args_list = [
			ArgStruct.scalar_enum('D_1_Mb', enums.RateSupport),
			ArgStruct.scalar_enum('D_2_Mb', enums.RateSupport),
			ArgStruct.scalar_enum('C_55_M', enums.RateSupport),
			ArgStruct.scalar_enum('C_11_M', enums.RateSupport)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.D_1_Mb: enums.RateSupport = None
			self.D_2_Mb: enums.RateSupport = None
			self.C_55_M: enums.RateSupport = None
			self.C_11_M: enums.RateSupport = None

	# noinspection PyTypeChecker
	def get_dsss_conf(self) -> DsssConfStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes:DSSSconf \n
		Snippet: value: DsssConfStruct = driver.configure.connection.srates.get_dsss_conf() \n
		Definition of DSSS/CCK supported rates. These settings apply only if user-defined supported rates are enabled, see method
		RsCmwWlanSig.Configure.Connection.Srates.value. \n
			:return: structure: for return value, see the help for DsssConfStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes:DSSSconf?', self.__class__.DsssConfStruct())

	def set_dsss_conf(self, value: DsssConfStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes:DSSSconf \n
		Snippet: driver.configure.connection.srates.set_dsss_conf(value = DsssConfStruct()) \n
		Definition of DSSS/CCK supported rates. These settings apply only if user-defined supported rates are enabled, see method
		RsCmwWlanSig.Configure.Connection.Srates.value. \n
			:param value: see the help for DsssConfStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes:DSSSconf', value)

	# noinspection PyTypeChecker
	def get_value(self) -> enums.EnableState:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes \n
		Snippet: value: enums.EnableState = driver.configure.connection.srates.get_value() \n
		Enables/disables user-defined supported rates. \n
			:return: state: ENABle | DISable
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes?')
		return Conversions.str_to_scalar_enum(response, enums.EnableState)

	def set_value(self, state: enums.EnableState) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:SRATes \n
		Snippet: driver.configure.connection.srates.set_value(state = enums.EnableState.DISable) \n
		Enables/disables user-defined supported rates. \n
			:param state: ENABle | DISable
		"""
		param = Conversions.enum_scalar_to_str(state, enums.EnableState)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:SRATes {param}')
