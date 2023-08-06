from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	def get_nantenna(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:NANTenna \n
		Snippet: value: int = driver.configure.rfSettings.cte.lowEnergy.get_nantenna() \n
		Specifies the number of DUT's antennas. One reference and one non-reference antennas are mandatory. \n
			:return: nof_antennas: numeric Range: 2 to 4
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:NANTenna?')
		return Conversions.str_to_int(response)

	def set_nantenna(self, nof_antennas: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:NANTenna \n
		Snippet: driver.configure.rfSettings.cte.lowEnergy.set_nantenna(nof_antennas = 1) \n
		Specifies the number of DUT's antennas. One reference and one non-reference antennas are mandatory. \n
			:param nof_antennas: numeric Range: 2 to 4
		"""
		param = Conversions.decimal_value_to_str(nof_antennas)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:NANTenna {param}')

	# noinspection PyTypeChecker
	class AoffsetStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ant_Ref_1: float: numeric Range: -3 dB to 3 dB
			- Ant_Ref_2: float: numeric Range: -3 dB to 3 dB
			- Ant_Ref_3: float: numeric Range: -3 dB to 3 dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ant_Ref_1'),
			ArgStruct.scalar_float('Ant_Ref_2'),
			ArgStruct.scalar_float('Ant_Ref_3')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ant_Ref_1: float = None
			self.Ant_Ref_2: float = None
			self.Ant_Ref_3: float = None

	def get_aoffset(self) -> AoffsetStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:AOFFset \n
		Snippet: value: AoffsetStruct = driver.configure.rfSettings.cte.lowEnergy.get_aoffset() \n
		Specifies the offset of external attenuation per input antenna relative to the reference antenna. For the reference
		antenna, the offset is fixed and set to 0 dB. \n
			:return: structure: for return value, see the help for AoffsetStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:AOFFset?', self.__class__.AoffsetStruct())

	def set_aoffset(self, value: AoffsetStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:AOFFset \n
		Snippet: driver.configure.rfSettings.cte.lowEnergy.set_aoffset(value = AoffsetStruct()) \n
		Specifies the offset of external attenuation per input antenna relative to the reference antenna. For the reference
		antenna, the offset is fixed and set to 0 dB. \n
			:param value: see the help for AoffsetStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:AOFFset', value)

	def get_roffset(self) -> float:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:ROFFset \n
		Snippet: value: float = driver.configure.rfSettings.cte.lowEnergy.get_roffset() \n
		No command help available \n
			:return: ant_ref: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:CTE:LENergy:ROFFset?')
		return Conversions.str_to_float(response)
