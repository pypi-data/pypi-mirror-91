from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptx:
	"""Ptx commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptx", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:SGACp CMDLINK]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- No_Of_Exceptions: int: decimal Number of exceptions (channels ±3, ±4 ... with an ACP above the 'Exception PTx' threshold ) Range: 0 to 99
			- Ptx_Ref: float: float Reference power PTXref, measured in the center channel Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Ptx_N_26_Ch_N_1_Abs: float: No parameter help available
			- Ptx_N_26_Ch_P_1_Abs: float: No parameter help available
			- Ptx_N_26_Ch_N_1_Rel: float: No parameter help available
			- Ptx_N_26_Ch_P_1_Rel: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_int('No_Of_Exceptions'),
			ArgStruct.scalar_float('Ptx_Ref'),
			ArgStruct.scalar_float('Ptx_N_26_Ch_N_1_Abs'),
			ArgStruct.scalar_float('Ptx_N_26_Ch_P_1_Abs'),
			ArgStruct.scalar_float('Ptx_N_26_Ch_N_1_Rel'),
			ArgStruct.scalar_float('Ptx_N_26_Ch_P_1_Rel')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.No_Of_Exceptions: int = None
			self.Ptx_Ref: float = None
			self.Ptx_N_26_Ch_N_1_Abs: float = None
			self.Ptx_N_26_Ch_P_1_Abs: float = None
			self.Ptx_N_26_Ch_N_1_Rel: float = None
			self.Ptx_N_26_Ch_P_1_Rel: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:SGACp:EDRate[:PTX] \n
		Snippet: value: ResultData = driver.multiEval.sgacp.edrate.ptx.fetch() \n
		Returns the 'Spectrum Gated ACP' results for EDR packets (single values) . The values described below are returned by
		FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:SGACp:EDRate:PTX?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:SGACp:EDRate[:PTX] \n
		Snippet: value: ResultData = driver.multiEval.sgacp.edrate.ptx.read() \n
		Returns the 'Spectrum Gated ACP' results for EDR packets (single values) . The values described below are returned by
		FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:SGACp:EDRate:PTX?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:SGACp CMDLINK]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- No_Of_Exceptions: float: decimal Number of exceptions (channels ±3, ±4 ... with an ACP above the 'Exception PTx' threshold ) Range: 0 to 99
			- Ptx_Ref: float: float Reference power PTXref, measured in the center channel Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Ptx_N_26_Ch_N_1_Abs: float: No parameter help available
			- Ptx_N_26_Ch_P_1_Abs: float: No parameter help available
			- Ptx_N_26_Ch_N_1_Rel: float: No parameter help available
			- Ptx_N_26_Ch_P_1_Rel: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('No_Of_Exceptions'),
			ArgStruct.scalar_float('Ptx_Ref'),
			ArgStruct.scalar_float('Ptx_N_26_Ch_N_1_Abs'),
			ArgStruct.scalar_float('Ptx_N_26_Ch_P_1_Abs'),
			ArgStruct.scalar_float('Ptx_N_26_Ch_N_1_Rel'),
			ArgStruct.scalar_float('Ptx_N_26_Ch_P_1_Rel')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.No_Of_Exceptions: float = None
			self.Ptx_Ref: float = None
			self.Ptx_N_26_Ch_N_1_Abs: float = None
			self.Ptx_N_26_Ch_P_1_Abs: float = None
			self.Ptx_N_26_Ch_N_1_Rel: float = None
			self.Ptx_N_26_Ch_P_1_Rel: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:SGACp:EDRate[:PTX] \n
		Snippet: value: CalculateStruct = driver.multiEval.sgacp.edrate.ptx.calculate() \n
		Returns the 'Spectrum Gated ACP' results for EDR packets (single values) . The values described below are returned by
		FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:SGACp:EDRate:PTX?', self.__class__.CalculateStruct())
