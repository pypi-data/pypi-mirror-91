from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:SOBW:CURRent \n
		Snippet: value: List[float] = driver.multiEval.trace.soBw.current.read() \n
		Returns current, average and maximum results of the 'Spectrum 20 dB Bandwidth' trace. The 20 dB bandwidth values are
		available for BR bursts (method RsCmwBluetoothMeas.Configure.InputSignal.btype) . \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: obw: float 769 bandwidth results, covering a frequency range [–1.5 MHz, +1.5 MHz], relative to the peak emission within the measured Bluetooth channel. The spacing between adjacent trace points is 3.906 kHz (≅4 MHz/1024) . Range: -99.99 dB to 99.99 dB, Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:SOBW:CURRent?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:SOBW:CURRent \n
		Snippet: value: List[float] = driver.multiEval.trace.soBw.current.fetch() \n
		Returns current, average and maximum results of the 'Spectrum 20 dB Bandwidth' trace. The 20 dB bandwidth values are
		available for BR bursts (method RsCmwBluetoothMeas.Configure.InputSignal.btype) . \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: obw: float 769 bandwidth results, covering a frequency range [–1.5 MHz, +1.5 MHz], relative to the peak emission within the measured Bluetooth channel. The spacing between adjacent trace points is 3.906 kHz (≅4 MHz/1024) . Range: -99.99 dB to 99.99 dB, Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:SOBW:CURRent?', suppressed)
		return response
