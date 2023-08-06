from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Muedca:
	"""Muedca commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("muedca", core, parent)

	# noinspection PyTypeChecker
	class AcbeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Aif_Sn: int: integer Arbitration inter-frame space number. Zero disables channel access. Range: 0, 2 to 15
			- Ecw_Min: int: integer Minimal contention window Range: 0 to 15
			- Ecw_Max: int: integer Maximal contention window Range: 0 to 15
			- Timer: int: integer MU EDCA timer Range: 1 to 255 , Unit: 8x TUs (8x 1024 µs)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Aif_Sn'),
			ArgStruct.scalar_int('Ecw_Min'),
			ArgStruct.scalar_int('Ecw_Max'),
			ArgStruct.scalar_int('Timer')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Aif_Sn: int = None
			self.Ecw_Min: int = None
			self.Ecw_Max: int = None
			self.Timer: int = None

	def get_acbe(self) -> AcbeStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MUEDca:ACBE \n
		Snippet: value: AcbeStruct = driver.configure.connection.muedca.get_acbe() \n
		Configures the record fields of MU EDCA parameter set. \n
			:return: structure: for return value, see the help for AcbeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MUEDca:ACBE?', self.__class__.AcbeStruct())

	def set_acbe(self, value: AcbeStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MUEDca:ACBE \n
		Snippet: driver.configure.connection.muedca.set_acbe(value = AcbeStruct()) \n
		Configures the record fields of MU EDCA parameter set. \n
			:param value: see the help for AcbeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MUEDca:ACBE', value)

	# noinspection PyTypeChecker
	class AcbkStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Aif_Sn: int: integer Arbitration inter-frame space number. Zero disables channel access. Range: 0, 2 to 15
			- Ecw_Min: int: integer Minimal contention window Range: 0 to 15
			- Ecw_Max: int: integer Maximal contention window Range: 0 to 15
			- Timer: int: integer MU EDCA timer Range: 1 to 255 , Unit: 8x TUs (8x 1024 µs)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Aif_Sn'),
			ArgStruct.scalar_int('Ecw_Min'),
			ArgStruct.scalar_int('Ecw_Max'),
			ArgStruct.scalar_int('Timer')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Aif_Sn: int = None
			self.Ecw_Min: int = None
			self.Ecw_Max: int = None
			self.Timer: int = None

	def get_acbk(self) -> AcbkStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MUEDca:ACBK \n
		Snippet: value: AcbkStruct = driver.configure.connection.muedca.get_acbk() \n
		Configures the record fields of MU EDCA parameter set. \n
			:return: structure: for return value, see the help for AcbkStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MUEDca:ACBK?', self.__class__.AcbkStruct())

	def set_acbk(self, value: AcbkStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MUEDca:ACBK \n
		Snippet: driver.configure.connection.muedca.set_acbk(value = AcbkStruct()) \n
		Configures the record fields of MU EDCA parameter set. \n
			:param value: see the help for AcbkStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MUEDca:ACBK', value)

	# noinspection PyTypeChecker
	class AcviStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Aif_Sn: int: integer Arbitration inter-frame space number. Zero disables channel access. Range: 0, 2 to 15
			- Ecw_Min: int: integer Minimal contention window Range: 0 to 15
			- Ecw_Max: int: integer Maximal contention window Range: 0 to 15
			- Timer: int: integer MU EDCA timer Range: 1 to 255 , Unit: 8x TUs (8x 1024 µs)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Aif_Sn'),
			ArgStruct.scalar_int('Ecw_Min'),
			ArgStruct.scalar_int('Ecw_Max'),
			ArgStruct.scalar_int('Timer')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Aif_Sn: int = None
			self.Ecw_Min: int = None
			self.Ecw_Max: int = None
			self.Timer: int = None

	def get_acvi(self) -> AcviStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MUEDca:ACVI \n
		Snippet: value: AcviStruct = driver.configure.connection.muedca.get_acvi() \n
		Configures the record fields of MU EDCA parameter set. \n
			:return: structure: for return value, see the help for AcviStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MUEDca:ACVI?', self.__class__.AcviStruct())

	def set_acvi(self, value: AcviStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MUEDca:ACVI \n
		Snippet: driver.configure.connection.muedca.set_acvi(value = AcviStruct()) \n
		Configures the record fields of MU EDCA parameter set. \n
			:param value: see the help for AcviStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MUEDca:ACVI', value)

	# noinspection PyTypeChecker
	class AcvoStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Aif_Sn: int: integer Arbitration inter-frame space number. Zero disables channel access. Range: 0, 2 to 15
			- Ecw_Min: int: integer Minimal contention window Range: 0 to 15
			- Ecw_Max: int: integer Maximal contention window Range: 0 to 15
			- Timer: int: integer MU EDCA timer Range: 1 to 255 , Unit: 8x TUs (8x 1024 µs)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Aif_Sn'),
			ArgStruct.scalar_int('Ecw_Min'),
			ArgStruct.scalar_int('Ecw_Max'),
			ArgStruct.scalar_int('Timer')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Aif_Sn: int = None
			self.Ecw_Min: int = None
			self.Ecw_Max: int = None
			self.Timer: int = None

	def get_acvo(self) -> AcvoStruct:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MUEDca:ACVO \n
		Snippet: value: AcvoStruct = driver.configure.connection.muedca.get_acvo() \n
		Configures the record fields of MU EDCA parameter set. \n
			:return: structure: for return value, see the help for AcvoStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MUEDca:ACVO?', self.__class__.AcvoStruct())

	def set_acvo(self, value: AcvoStruct) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:CONNection:MUEDca:ACVO \n
		Snippet: driver.configure.connection.muedca.set_acvo(value = AcvoStruct()) \n
		Configures the record fields of MU EDCA parameter set. \n
			:param value: see the help for AcvoStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WLAN:SIGNaling<Instance>:CONNection:MUEDca:ACVO', value)
