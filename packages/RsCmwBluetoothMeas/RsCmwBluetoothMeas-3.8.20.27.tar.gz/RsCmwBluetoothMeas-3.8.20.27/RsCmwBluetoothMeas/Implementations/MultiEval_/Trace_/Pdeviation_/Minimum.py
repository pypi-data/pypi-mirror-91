from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Minimum:
	"""Minimum commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("minimum", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDEViation:MINimum \n
		Snippet: value: List[float] = driver.multiEval.trace.pdeviation.minimum.fetch() \n
		Returns the results of power deviation per slot for LE CTE traces. Deviation value is calculated as peak to average power
		ratio. The results of the minimum and maximum traces can be retrieved. The values described below are returned by FETCh
		and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: pv_s: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDEViation:MINimum?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDEViation:MINimum \n
		Snippet: value: List[float] = driver.multiEval.trace.pdeviation.minimum.read() \n
		Returns the results of power deviation per slot for LE CTE traces. Deviation value is calculated as peak to average power
		ratio. The results of the minimum and maximum traces can be retrieved. The values described below are returned by FETCh
		and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: pv_s: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDEViation:MINimum?', suppressed)
		return response

	def calculate(self) -> List[float]:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDEViation:MINimum \n
		Snippet: value: List[float] = driver.multiEval.trace.pdeviation.minimum.calculate() \n
		Returns the results of power deviation per slot for LE CTE traces. Deviation value is calculated as peak to average power
		ratio. The results of the minimum and maximum traces can be retrieved. The values described below are returned by FETCh
		and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: pv_s: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDEViation:MINimum?', suppressed)
		return response
