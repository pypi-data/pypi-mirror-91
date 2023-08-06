from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Association:
	"""Association commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("association", core, parent)

	@property
	def sta(self):
		"""sta commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sta'):
			from .Association_.Sta import Sta
			self._sta = Sta(self._core, self._base)
		return self._sta

	# noinspection PyTypeChecker
	class DisassStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Timeout: int: numeric Range: 1 s to 3600 s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_int('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Timeout: int = None

	def get_disass(self) -> DisassStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:ASSociation:DISass \n
		Snippet: value: DisassStruct = driver.configure.connection.association.get_disass() \n
		Enables or disables automatic STA disassociation, when a STA is no longer present. If enabled, the R&S CMW detects that a
		STA is absent, it automatically removes its association after some user-specified period of time. \n
			:return: structure: for return value, see the help for DisassStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:ASSociation:DISass?', self.__class__.DisassStruct())

	def set_disass(self, value: DisassStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:ASSociation:DISass \n
		Snippet: driver.configure.connection.association.set_disass(value = DisassStruct()) \n
		Enables or disables automatic STA disassociation, when a STA is no longer present. If enabled, the R&S CMW detects that a
		STA is absent, it automatically removes its association after some user-specified period of time. \n
			:param value: see the help for DisassStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:ASSociation:DISass', value)

	def get_preemption(self) -> bool:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:ASSociation:PREemption \n
		Snippet: value: bool = driver.configure.connection.association.get_preemption() \n
		If enabled, then the existing association possible with any MAC addresses is replaced by a new incoming one. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:ASSociation:PREemption?')
		return Conversions.str_to_bool(response)

	def set_preemption(self, enable: bool) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:ASSociation:PREemption \n
		Snippet: driver.configure.connection.association.set_preemption(enable = False) \n
		If enabled, then the existing association possible with any MAC addresses is replaced by a new incoming one. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:ASSociation:PREemption {param}')

	# noinspection PyTypeChecker
	def get_sta_priority(self) -> enums.PrioModeB:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:ASSociation:STAPriority \n
		Snippet: value: enums.PrioModeB = driver.configure.connection.association.get_sta_priority() \n
		Specifies how the stack prioritizes one STA over another in multi-STA connections. \n
			:return: mode: AUTO | ROURobin Automatic or round robin
		"""
		response = self._core.io.query_str('CONFigure:WLAN:SIGNaling<Instance>:CONNection:ASSociation:STAPriority?')
		return Conversions.str_to_scalar_enum(response, enums.PrioModeB)

	def set_sta_priority(self, mode: enums.PrioModeB) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:ASSociation:STAPriority \n
		Snippet: driver.configure.connection.association.set_sta_priority(mode = enums.PrioModeB.AUTO) \n
		Specifies how the stack prioritizes one STA over another in multi-STA connections. \n
			:param mode: AUTO | ROURobin Automatic or round robin
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PrioModeB)
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:CONNection:ASSociation:STAPriority {param}')

	def clone(self) -> 'Association':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Association(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
