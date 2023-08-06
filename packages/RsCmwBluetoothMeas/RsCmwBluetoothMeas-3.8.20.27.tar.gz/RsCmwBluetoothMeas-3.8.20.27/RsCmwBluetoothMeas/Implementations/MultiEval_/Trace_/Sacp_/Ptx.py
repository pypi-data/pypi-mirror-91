from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptx:
	"""Ptx commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptx", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:SACP[:PTX] \n
		Snippet: value: List[float] = driver.multiEval.trace.sacp.ptx.fetch() \n
		Returns the values of the 'Spectrum ACP' table for BR and LE packets in line with Bluetooth test specification.
			INTRO_CMD_HELP: Note that the number of returned values depends on the current burst type. \n
			- For BR bursts, the trace returns 79 values.The number of valid ACP results depends on the ACP measurement mode (method RsCmwBluetoothMeas.Configure.MultiEval.Sacp.Brate.Measurement.mode) :
			Table Header:  \n
			- In CH21 mode, the first 21 ACP values contain results for the relative channels –10, ..., 0, ..., +10; the remaining 58 values are not displayed.
			- In CH79 mode, valid ACP values are available for all 79 Bluetooth channels (2402 MHz, 2403 MHz, ..., 2480 MHz)
			- For LE bursts, the trace returns 81 values.The number of valid ACP results
		depends on the ACP measurement mode (method RsCmwBluetoothMeas.Configure.MultiEval.Sacp.LowEnergy.Le2M.Measurement.mode)
		:
			Table Header:  \n
			- In CH10 ('ACP +/- 5 Channels') mode, the first 21 ACP values contain results for the 1 MHz channels centered at fTX – 10 MHz, fTX – 9 MHz, ..., fTX + 10 MHz. The remaining 58 values are invalid (NAV) . This mode is applicable to all types of LE bursts.
			- In CH40 mode ('LE All Channels') , ACP values 1 to 81 contain results for the 1 MHz channels centered at 2401 MHz, 2402 MHz, ..., 2481 MHz This mode is only applicable to test packets using LE 1M PHY or LE 2M PHY. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: acp: float As explained above, for BR bursts the trace returns N=79, and for LE bursts it returns N=81 values. Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:SACP:PTX?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:SACP[:PTX] \n
		Snippet: value: List[float] = driver.multiEval.trace.sacp.ptx.read() \n
		Returns the values of the 'Spectrum ACP' table for BR and LE packets in line with Bluetooth test specification.
			INTRO_CMD_HELP: Note that the number of returned values depends on the current burst type. \n
			- For BR bursts, the trace returns 79 values.The number of valid ACP results depends on the ACP measurement mode (method RsCmwBluetoothMeas.Configure.MultiEval.Sacp.Brate.Measurement.mode) :
			Table Header:  \n
			- In CH21 mode, the first 21 ACP values contain results for the relative channels –10, ..., 0, ..., +10; the remaining 58 values are not displayed.
			- In CH79 mode, valid ACP values are available for all 79 Bluetooth channels (2402 MHz, 2403 MHz, ..., 2480 MHz)
			- For LE bursts, the trace returns 81 values.The number of valid ACP results
		depends on the ACP measurement mode (method RsCmwBluetoothMeas.Configure.MultiEval.Sacp.LowEnergy.Le2M.Measurement.mode)
		:
			Table Header:  \n
			- In CH10 ('ACP +/- 5 Channels') mode, the first 21 ACP values contain results for the 1 MHz channels centered at fTX – 10 MHz, fTX – 9 MHz, ..., fTX + 10 MHz. The remaining 58 values are invalid (NAV) . This mode is applicable to all types of LE bursts.
			- In CH40 mode ('LE All Channels') , ACP values 1 to 81 contain results for the 1 MHz channels centered at 2401 MHz, 2402 MHz, ..., 2481 MHz This mode is only applicable to test packets using LE 1M PHY or LE 2M PHY. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: acp: float As explained above, for BR bursts the trace returns N=79, and for LE bursts it returns N=81 values. Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:SACP:PTX?', suppressed)
		return response
