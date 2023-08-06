from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StDev:
	"""StDev commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stDev", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tol: float: No parameter help available
			- Delta_F_199_P_9: float: No parameter help available
			- Freq_Accuracy: float: No parameter help available
			- Freq_Drift: float: No parameter help available
			- Max_Drift: float: No parameter help available
			- Nominal_Power: float: No parameter help available
			- Freq_Offset: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Delta_F_199_P_9'),
			ArgStruct.scalar_float('Freq_Accuracy'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift'),
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
			self.Nominal_Power: float = None
			self.Freq_Offset: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:STDev \n
		Snippet: value: ResultData = driver.multiEval.modulation.lowEnergy.lrange.stDev.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:STDev?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tol: float: No parameter help available
			- Delta_F_199_P_9: float: No parameter help available
			- Freq_Accuracy: float: No parameter help available
			- Freq_Drift: float: No parameter help available
			- Max_Drift: float: No parameter help available
			- Nominal_Power: float: No parameter help available
			- Freq_Offset: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Delta_F_199_P_9'),
			ArgStruct.scalar_float('Freq_Accuracy'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift'),
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
			self.Nominal_Power: float = None
			self.Freq_Offset: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:STDev \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.lowEnergy.lrange.stDev.calculate() \n
		No command help available \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:STDev?', self.__class__.CalculateStruct())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:STDev \n
		Snippet: value: ResultData = driver.multiEval.modulation.lowEnergy.lrange.stDev.read() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:LENergy:LRANge:STDev?', self.__class__.ResultData())
