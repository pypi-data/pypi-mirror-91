from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PVTime:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.powerVsTime.maximum.fetch() \n
		Returns the values of the power vs. time traces. The results of the current, average minimum and maximum traces can be
		retrieved. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: pv_t: float M power results, depending on the packet type and payload length; see 'PvT and Freq. Dev. Trace Points (Classic) ', 'DEVM Trace Points for Test Mode (EDR) ' and 'PvT and Modulation Trace Points (LE) '. Range: –128.0 dBm to 30.0 dBm , Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PVTime:MAXimum?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PVTime:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.powerVsTime.maximum.read() \n
		Returns the values of the power vs. time traces. The results of the current, average minimum and maximum traces can be
		retrieved. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: pv_t: float M power results, depending on the packet type and payload length; see 'PvT and Freq. Dev. Trace Points (Classic) ', 'DEVM Trace Points for Test Mode (EDR) ' and 'PvT and Modulation Trace Points (LE) '. Range: –128.0 dBm to 30.0 dBm , Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PVTime:MAXimum?', suppressed)
		return response
