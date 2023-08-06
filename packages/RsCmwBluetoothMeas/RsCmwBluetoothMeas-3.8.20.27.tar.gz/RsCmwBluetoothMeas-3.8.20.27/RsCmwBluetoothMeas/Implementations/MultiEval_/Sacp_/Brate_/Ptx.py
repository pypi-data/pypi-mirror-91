from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptx:
	"""Ptx commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptx", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:SACP CMDLINK]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- No_Of_Exceptions: float: decimal Number of exceptions (channels ±3, ±4 ... with an ACP above the 'Exception PTx' threshold ) Range: 0 to 99
			- Acp: List[float]: float 79 ACP results Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('No_Of_Exceptions'),
			ArgStruct('Acp', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.No_Of_Exceptions: float = None
			self.Acp: List[float] = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:SACP:BRATe[:PTX] \n
		Snippet: value: CalculateStruct = driver.multiEval.sacp.brate.ptx.calculate() \n
		Returns the 'Spectrum ACP' results for BR packets. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below.
			INTRO_CMD_HELP: The number of valid ACP results depends on the ACP measurement mode (method RsCmwBluetoothMeas.Configure.MultiEval.Sacp.Brate.Measurement.mode CH21 | CH79) : \n
			- If 'ACP +/- 10 Channels' is selected, the first 21 ACP values contain the results for the relative channels –10, ..., 0, ..., +10; the remaining 58 values are not displayed.
			- If 'ACP 79 Channels' is selected, valid ACP values are available for all channels in the Bluetooth regulatory range. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:SACP:BRATe:PTX?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:SACP CMDLINK]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- No_Of_Exceptions: int: decimal Number of exceptions (channels ±3, ±4 ... with an ACP above the 'Exception PTx' threshold ) Range: 0 to 99
			- Acp: List[float]: float 79 ACP results Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_int('No_Of_Exceptions'),
			ArgStruct('Acp', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.No_Of_Exceptions: int = None
			self.Acp: List[float] = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:SACP:BRATe[:PTX] \n
		Snippet: value: ResultData = driver.multiEval.sacp.brate.ptx.fetch() \n
		Returns the 'Spectrum ACP' results for BR packets. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below.
			INTRO_CMD_HELP: The number of valid ACP results depends on the ACP measurement mode (method RsCmwBluetoothMeas.Configure.MultiEval.Sacp.Brate.Measurement.mode CH21 | CH79) : \n
			- If 'ACP +/- 10 Channels' is selected, the first 21 ACP values contain the results for the relative channels –10, ..., 0, ..., +10; the remaining 58 values are not displayed.
			- If 'ACP 79 Channels' is selected, valid ACP values are available for all channels in the Bluetooth regulatory range. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:SACP:BRATe:PTX?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:SACP:BRATe[:PTX] \n
		Snippet: value: ResultData = driver.multiEval.sacp.brate.ptx.read() \n
		Returns the 'Spectrum ACP' results for BR packets. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below.
			INTRO_CMD_HELP: The number of valid ACP results depends on the ACP measurement mode (method RsCmwBluetoothMeas.Configure.MultiEval.Sacp.Brate.Measurement.mode CH21 | CH79) : \n
			- If 'ACP +/- 10 Channels' is selected, the first 21 ACP values contain the results for the relative channels –10, ..., 0, ..., +10; the remaining 58 values are not displayed.
			- If 'ACP 79 Channels' is selected, valid ACP values are available for all channels in the Bluetooth regulatory range. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:SACP:BRATe:PTX?', self.__class__.ResultData())
