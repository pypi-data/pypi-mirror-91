from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits, see 'Limits (Modulation BR) ' and 'Limits (Modulation EDR) '. Range: 0 % to 100 %
			- Freq_Accuracy: float: float Range: -0.99999 MHz to 0.99999 MHz
			- Freq_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz
			- Max_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz/50 μs
			- Freq_Dev_Avg_F_1: float: No parameter help available
			- Freq_Dev_Min_F_1: float: No parameter help available
			- Freq_Dev_Max_F_1: float: No parameter help available
			- Freq_Dev_Avg_F_2: float: No parameter help available
			- Freq_Dev_Min_F_2: float: No parameter help available
			- Freq_Dev_Max_F_2: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Freq_Accuracy'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_2'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_2'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Freq_Accuracy: float = None
			self.Freq_Drift: float = None
			self.Max_Drift: float = None
			self.Freq_Dev_Avg_F_1: float = None
			self.Freq_Dev_Min_F_1: float = None
			self.Freq_Dev_Max_F_1: float = None
			self.Freq_Dev_Avg_F_2: float = None
			self.Freq_Dev_Min_F_2: float = None
			self.Freq_Dev_Max_F_2: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:CURRent \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.nmode.classic.current.calculate() \n
		Returns the current, average, xmin, xmax, and max modulation results for BR/EDR, normal mode, see 'LE: Statistical
		Modulation Results '. An R&S CMW100/CMW with MUA returns all results. An R&S CMW500/2xx with BB Meas returns only three
		values: results 1 to 3. The values described below are returned by FETCh and READ commands. CALCulate commands return
		limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:CURRent?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits, see 'Limits (Modulation BR) ' and 'Limits (Modulation EDR) '. Range: 0 % to 100 %
			- Freq_Accuracy: float: float Range: -0.99999 MHz to 0.99999 MHz
			- Freq_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz
			- Max_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz/50 μs
			- Freq_Dev_Avg_F_1: float: No parameter help available
			- Freq_Dev_Min_F_1: float: No parameter help available
			- Freq_Dev_Max_F_1: float: No parameter help available
			- Freq_Dev_Avg_F_2: float: No parameter help available
			- Freq_Dev_Min_F_2: float: No parameter help available
			- Freq_Dev_Max_F_2: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Freq_Accuracy'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_2'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_2'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Freq_Accuracy: float = None
			self.Freq_Drift: float = None
			self.Max_Drift: float = None
			self.Freq_Dev_Avg_F_1: float = None
			self.Freq_Dev_Min_F_1: float = None
			self.Freq_Dev_Max_F_1: float = None
			self.Freq_Dev_Avg_F_2: float = None
			self.Freq_Dev_Min_F_2: float = None
			self.Freq_Dev_Max_F_2: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:CURRent \n
		Snippet: value: ResultData = driver.multiEval.modulation.nmode.classic.current.fetch() \n
		Returns the current, average, xmin, xmax, and max modulation results for BR/EDR, normal mode, see 'LE: Statistical
		Modulation Results '. An R&S CMW100/CMW with MUA returns all results. An R&S CMW500/2xx with BB Meas returns only three
		values: results 1 to 3. The values described below are returned by FETCh and READ commands. CALCulate commands return
		limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:CURRent?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:CURRent \n
		Snippet: value: ResultData = driver.multiEval.modulation.nmode.classic.current.read() \n
		Returns the current, average, xmin, xmax, and max modulation results for BR/EDR, normal mode, see 'LE: Statistical
		Modulation Results '. An R&S CMW100/CMW with MUA returns all results. An R&S CMW500/2xx with BB Meas returns only three
		values: results 1 to 3. The values described below are returned by FETCh and READ commands. CALCulate commands return
		limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:CURRent?', self.__class__.ResultData())
