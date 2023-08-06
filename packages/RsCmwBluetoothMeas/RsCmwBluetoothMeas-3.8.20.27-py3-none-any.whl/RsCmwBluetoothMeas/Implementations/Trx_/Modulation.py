from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits, see 'Limits (Modulation LE) '.
			- Delta_F_299_P_9: float: float Unit: %
			- Freq_Accuracy: float: float Unit: Hz
			- Freq_Drift: float: float Unit: Hz
			- Max_Drift: float: float
			- Freq_Dev_Avg_F_1: float: No parameter help available
			- Freq_Dev_Min_F_1: float: No parameter help available
			- Freq_Dev_Max_F_1: float: No parameter help available
			- Freq_Dev_Avg_F_2: float: No parameter help available
			- Freq_Dev_Min_F_2: float: No parameter help available
			- Freq_Dev_Max_F_2: float: No parameter help available
			- Nominal_Power: float: float Unit: dBm
			- Mod_Ratio: float: float Range: 0 to 1
			- Freq_Offset: float: float
			- Init_Freq_Drift: float: float"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Delta_F_299_P_9'),
			ArgStruct.scalar_float('Freq_Accuracy'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_2'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_2'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_2'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Mod_Ratio'),
			ArgStruct.scalar_float('Freq_Offset'),
			ArgStruct.scalar_float('Init_Freq_Drift')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Delta_F_299_P_9: float = None
			self.Freq_Accuracy: float = None
			self.Freq_Drift: float = None
			self.Max_Drift: float = None
			self.Freq_Dev_Avg_F_1: float = None
			self.Freq_Dev_Min_F_1: float = None
			self.Freq_Dev_Max_F_1: float = None
			self.Freq_Dev_Avg_F_2: float = None
			self.Freq_Dev_Min_F_2: float = None
			self.Freq_Dev_Max_F_2: float = None
			self.Nominal_Power: float = None
			self.Mod_Ratio: float = None
			self.Freq_Offset: float = None
			self.Init_Freq_Drift: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:TRX:MODulation \n
		Snippet: value: FetchStruct = driver.trx.modulation.fetch() \n
		Returns current modulation results for TRx tests on advertiser packets (LE 1M PHY) . See also 'LE: Statistical Modulation
		Results '. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:TRX:MODulation?', self.__class__.FetchStruct())
