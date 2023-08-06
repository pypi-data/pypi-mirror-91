from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UesInfo:
	"""UesInfo commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uesInfo", core, parent)

	@property
	def antenna(self):
		"""antenna commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_antenna'):
			from .UesInfo_.Antenna import Antenna
			self._antenna = Antenna(self._core, self._base)
		return self._antenna

	@property
	def cmwAddress(self):
		"""cmwAddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmwAddress'):
			from .UesInfo_.CmwAddress import CmwAddress
			self._cmwAddress = CmwAddress(self._core, self._base)
		return self._cmwAddress

	def get_ap_ssid(self) -> str:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:UESinfo:APSSid \n
		Snippet: value: str = driver.sense.uesInfo.get_ap_ssid() \n
		Returns the SSID of the associated access point. The command is only relevant in operation mode 'Station'. \n
			:return: ssid: string Service set identifier as string
		"""
		response = self._core.io.query_str('SENSe:WLAN:SIGNaling<Instance>:UESinfo:APSSid?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	class RxTrigFrameStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Total_Tf: int: decimal
			- Station_Tf: int: decimal"""
		__meta_args_list = [
			ArgStruct.scalar_int('Total_Tf'),
			ArgStruct.scalar_int('Station_Tf')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Total_Tf: int = None
			self.Station_Tf: int = None

	def get_rx_trig_frame(self) -> RxTrigFrameStruct:
		"""SCPI: SENSe:WLAN:SIGNaling<instance>:UESinfo:RXTRigframe \n
		Snippet: value: RxTrigFrameStruct = driver.sense.uesInfo.get_rx_trig_frame() \n
		Queries the total trigger frames received and the number of trigger frames directed to the station, i.e. R&S CMW. \n
			:return: structure: for return value, see the help for RxTrigFrameStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:WLAN:SIGNaling<Instance>:UESinfo:RXTRigframe?', self.__class__.RxTrigFrameStruct())

	def clone(self) -> 'UesInfo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UesInfo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
