from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Minimum:
	"""Minimum commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("minimum", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tol: float: No parameter help available
			- Freq_Dev_Avg_F_1: float: No parameter help available
			- Freq_Dev_Min_F_1: float: No parameter help available
			- Freq_Dev_Max_F_1: float: No parameter help available
			- Freq_Dev_Avg_F_2: float: No parameter help available
			- Freq_Dev_Min_F_2: float: No parameter help available
			- Freq_Dev_Max_F_2: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
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
			self.Freq_Dev_Avg_F_1: float = None
			self.Freq_Dev_Min_F_1: float = None
			self.Freq_Dev_Max_F_1: float = None
			self.Freq_Dev_Avg_F_2: float = None
			self.Freq_Dev_Min_F_2: float = None
			self.Freq_Dev_Max_F_2: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:MINimum \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.nmode.classic.minimum.calculate() \n
		No command help available \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:MINimum?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Out_Of_Tol: float: No parameter help available
			- Freq_Dev_Avg_F_1: float: No parameter help available
			- Freq_Dev_Min_F_1: float: No parameter help available
			- Freq_Dev_Max_F_1: float: No parameter help available
			- Freq_Dev_Avg_F_2: float: No parameter help available
			- Freq_Dev_Min_F_2: float: No parameter help available
			- Freq_Dev_Max_F_2: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
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
			self.Freq_Dev_Avg_F_1: float = None
			self.Freq_Dev_Min_F_1: float = None
			self.Freq_Dev_Max_F_1: float = None
			self.Freq_Dev_Avg_F_2: float = None
			self.Freq_Dev_Min_F_2: float = None
			self.Freq_Dev_Max_F_2: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:MINimum \n
		Snippet: value: ResultData = driver.multiEval.modulation.nmode.classic.minimum.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:MINimum?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:MINimum \n
		Snippet: value: ResultData = driver.multiEval.modulation.nmode.classic.minimum.read() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:NMODe:CLASsic:MINimum?', self.__class__.ResultData())
