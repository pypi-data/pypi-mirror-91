from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlsField:
	"""AlsField commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alsField", core, parent)

	def set(self, ch_20_index: enums.Ch20Index, subfield: enums.Subfield) -> None:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:PER:DFRame:HEMU:ALSField \n
		Snippet: driver.configure.per.dframe.hemu.alsField.set(ch_20_index = enums.Ch20Index.CHA1, subfield = enums.Subfield.A000) \n
		Sets 8-bit indices for resource unit (RU) allocation for the selected channel. The <Subfield> parameter specifies the
		number of RUs, their position and size. Refer to IEEE P802.11ax/D8.0, table 27-26, RU allocation subfield. \n
			:param ch_20_index: CHA1 | CHA2 | CHA3 | CHA4
			:param subfield: A000 | A001 | A002 | A003 | A004 | A005 | A006 | A007 | A008 | A009 | A010 | A011 | A012 | A013 | A014 | A015 | A016 | A024 | A032 | A040 | A048 | A056 | A064 | A072 | A080 | A088 | A096 | A112 | A113 | A114 | A115 | A116 | A120 | A128 | A192 | A200 | A208 | A216 | A224
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ch_20_index', ch_20_index, DataType.Enum), ArgSingle('subfield', subfield, DataType.Enum))
		self._core.io.write(f'CONFigure:WLAN:SIGNaling<Instance>:PER:DFRame:HEMU:ALSField {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self, ch_20_index: enums.Ch20Index) -> enums.Subfield:
		"""SCPI: CONFigure:WLAN:SIGNaling<instance>:PER:DFRame:HEMU:ALSField \n
		Snippet: value: enums.Subfield = driver.configure.per.dframe.hemu.alsField.get(ch_20_index = enums.Ch20Index.CHA1) \n
		Sets 8-bit indices for resource unit (RU) allocation for the selected channel. The <Subfield> parameter specifies the
		number of RUs, their position and size. Refer to IEEE P802.11ax/D8.0, table 27-26, RU allocation subfield. \n
			:param ch_20_index: CHA1 | CHA2 | CHA3 | CHA4
			:return: subfield: A000 | A001 | A002 | A003 | A004 | A005 | A006 | A007 | A008 | A009 | A010 | A011 | A012 | A013 | A014 | A015 | A016 | A024 | A032 | A040 | A048 | A056 | A064 | A072 | A080 | A088 | A096 | A112 | A113 | A114 | A115 | A116 | A120 | A128 | A192 | A200 | A208 | A216 | A224"""
		param = Conversions.enum_scalar_to_str(ch_20_index, enums.Ch20Index)
		response = self._core.io.query_str(f'CONFigure:WLAN:SIGNaling<Instance>:PER:DFRame:HEMU:ALSField? {param}')
		return Conversions.str_to_scalar_enum(response, enums.Subfield)
