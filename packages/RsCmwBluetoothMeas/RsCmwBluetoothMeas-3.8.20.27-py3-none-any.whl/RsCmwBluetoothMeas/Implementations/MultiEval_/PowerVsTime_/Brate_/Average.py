from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float: float | ON | OFF Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:PVTime CMDLINK]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Peak_Power: float: float Peak power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Leakage_Power: float: float Average power during the carrier-off state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Packet_Timing: float: float Time between the expected and actual start of the first symbol of the Bluetooth burst Range: -99.99 µs to 99.99 µs, Unit: s
			- Gfsk_Power: float: float Average power within the access code and header portion of the BR burst (first 126 symbols) . Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Leakage_Power'),
			ArgStruct.scalar_float('Packet_Timing'),
			ArgStruct.scalar_float('Gfsk_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.Peak_Power: float = None
			self.Leakage_Power: float = None
			self.Packet_Timing: float = None
			self.Gfsk_Power: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:BRATe:AVERage \n
		Snippet: value: CalculateStruct = driver.multiEval.powerVsTime.brate.average.calculate() \n
		Returns the power results for BR packets. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:BRATe:AVERage?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ReadStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float or bool: float | ON | OFF Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:PVTime CMDLINK]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Peak_Power: float: float Peak power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Leakage_Power: float: float Average power during the carrier-off state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Packet_Timing: float: float Time between the expected and actual start of the first symbol of the Bluetooth burst Range: -99.99 µs to 99.99 µs, Unit: s
			- Gfsk_Power: float: float Average power within the access code and header portion of the BR burst (first 126 symbols) . Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Leakage_Power'),
			ArgStruct.scalar_float('Packet_Timing'),
			ArgStruct.scalar_float('Gfsk_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float or bool = None
			self.Nominal_Power: float = None
			self.Peak_Power: float = None
			self.Leakage_Power: float = None
			self.Packet_Timing: float = None
			self.Gfsk_Power: float = None

	def read(self) -> ReadStruct:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:BRATe:AVERage \n
		Snippet: value: ReadStruct = driver.multiEval.powerVsTime.brate.average.read() \n
		Returns the power results for BR packets. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ReadStruct structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:BRATe:AVERage?', self.__class__.ReadStruct())

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float: float | ON | OFF Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:PVTime CMDLINK]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Peak_Power: float: float Peak power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Leakage_Power: float: float Average power during the carrier-off state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Packet_Timing: float: float Time between the expected and actual start of the first symbol of the Bluetooth burst Range: -99.99 µs to 99.99 µs, Unit: s
			- Gfsk_Power: float: float Average power within the access code and header portion of the BR burst (first 126 symbols) . Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Leakage_Power'),
			ArgStruct.scalar_float('Packet_Timing'),
			ArgStruct.scalar_float('Gfsk_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.Peak_Power: float = None
			self.Leakage_Power: float = None
			self.Packet_Timing: float = None
			self.Gfsk_Power: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:BRATe:AVERage \n
		Snippet: value: FetchStruct = driver.multiEval.powerVsTime.brate.average.fetch() \n
		Returns the power results for BR packets. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:BRATe:AVERage?', self.__class__.FetchStruct())
