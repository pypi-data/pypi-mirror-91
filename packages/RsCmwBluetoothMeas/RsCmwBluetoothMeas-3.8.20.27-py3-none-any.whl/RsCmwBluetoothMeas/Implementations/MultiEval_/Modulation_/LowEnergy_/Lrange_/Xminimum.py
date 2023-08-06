from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Xminimum:
	"""Xminimum commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("xminimum", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits, see 'Limits (Modulation LE) '. Range: 0 % to 100 %, Unit: %
			- Delta_F_199_P_9: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Accuracy: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Max_Drift: float: float Range: -0.99999 MHz/50 μs to 0.99999 MHz/50 μs , Unit: Hz/50 μs
			- Freq_Dev_Avg_F_1: float: No parameter help available
			- Freq_Dev_Min_F_1: float: No parameter help available
			- Freq_Dev_Max_F_1: float: No parameter help available
			- Nominal_Power: float: float Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Freq_Offset: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Delta_F_199_P_9'),
			ArgStruct.scalar_float('Freq_Accuracy'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_1'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Freq_Offset')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Delta_F_199_P_9: float = None
			self.Freq_Accuracy: float = None
			self.Freq_Drift: float = None
			self.Max_Drift: float = None
			self.Freq_Dev_Avg_F_1: float = None
			self.Freq_Dev_Min_F_1: float = None
			self.Freq_Dev_Max_F_1: float = None
			self.Nominal_Power: float = None
			self.Freq_Offset: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:XMINimum \n
		Snippet: value: ResultData = driver.multiEval.modulation.lowEnergy.lrange.xminimum.fetch() \n
		Returns the current, average, absolute min (xmin) , absolute max (xmax) , and max modulation results for LE coded PHY,
		see 'LE: Statistical Modulation Results '. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:XMINimum?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits, see 'Limits (Modulation LE) '. Range: 0 % to 100 %, Unit: %
			- Delta_F_199_P_9: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Accuracy: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Max_Drift: float: float Range: -0.99999 MHz/50 μs to 0.99999 MHz/50 μs , Unit: Hz/50 μs
			- Freq_Dev_Avg_F_1: float: No parameter help available
			- Freq_Dev_Min_F_1: float: No parameter help available
			- Freq_Dev_Max_F_1: float: No parameter help available
			- Nominal_Power: float: float Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Freq_Offset: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Delta_F_199_P_9'),
			ArgStruct.scalar_float('Freq_Accuracy'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_1'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Freq_Offset')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Delta_F_199_P_9: float = None
			self.Freq_Accuracy: float = None
			self.Freq_Drift: float = None
			self.Max_Drift: float = None
			self.Freq_Dev_Avg_F_1: float = None
			self.Freq_Dev_Min_F_1: float = None
			self.Freq_Dev_Max_F_1: float = None
			self.Nominal_Power: float = None
			self.Freq_Offset: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:XMINimum \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.lowEnergy.lrange.xminimum.calculate() \n
		Returns the current, average, absolute min (xmin) , absolute max (xmax) , and max modulation results for LE coded PHY,
		see 'LE: Statistical Modulation Results '. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:XMINimum?', self.__class__.CalculateStruct())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:XMINimum \n
		Snippet: value: ResultData = driver.multiEval.modulation.lowEnergy.lrange.xminimum.read() \n
		Returns the current, average, absolute min (xmin) , absolute max (xmax) , and max modulation results for LE coded PHY,
		see 'LE: Statistical Modulation Results '. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:XMINimum?', self.__class__.ResultData())
