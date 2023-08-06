from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2M:
	"""Le2M commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le2M", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm
			- No_Of_Exceptions: int: decimal Number of exceptions (channels ±3, ±4 ... with an ACP above the 'Exception PTx' threshold ) Range: 0 to 99"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_int('No_Of_Exceptions')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nominal_Power: float = None
			self.No_Of_Exceptions: int = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:SACP:LENergy:LE2M \n
		Snippet: value: ResultData = driver.multiEval.sacp.lowEnergy.le2M.read() \n
		Returns the 'Spectrum ACP' results for LE 2M PHY (...:LE2M...) and LE coded PHY (...:LRANge...) , see 'LE: Spectrum ACP
		Results '. The values described below are returned by FETCh and READ commands. CALCulate commands return limit check
		results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:SACP:LENergy:LE2M?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:SACP:LENergy:LE2M \n
		Snippet: value: ResultData = driver.multiEval.sacp.lowEnergy.le2M.fetch() \n
		Returns the 'Spectrum ACP' results for LE 2M PHY (...:LE2M...) and LE coded PHY (...:LRANge...) , see 'LE: Spectrum ACP
		Results '. The values described below are returned by FETCh and READ commands. CALCulate commands return limit check
		results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:SACP:LENergy:LE2M?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm
			- No_Of_Exceptions: float: decimal Number of exceptions (channels ±3, ±4 ... with an ACP above the 'Exception PTx' threshold ) Range: 0 to 99"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('No_Of_Exceptions')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nominal_Power: float = None
			self.No_Of_Exceptions: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:SACP:LENergy:LE2M \n
		Snippet: value: CalculateStruct = driver.multiEval.sacp.lowEnergy.le2M.calculate() \n
		Returns the 'Spectrum ACP' results for LE 2M PHY (...:LE2M...) and LE coded PHY (...:LRANge...) , see 'LE: Spectrum ACP
		Results '. The values described below are returned by FETCh and READ commands. CALCulate commands return limit check
		results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:SACP:LENergy:LE2M?', self.__class__.CalculateStruct())
