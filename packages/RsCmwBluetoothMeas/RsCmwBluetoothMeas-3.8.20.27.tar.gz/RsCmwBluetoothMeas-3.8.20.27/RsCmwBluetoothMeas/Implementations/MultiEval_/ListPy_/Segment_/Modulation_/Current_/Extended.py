from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extended:
	"""Extended commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extended", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Seg_Reliability: int: decimal Reliability indicator for the segment. The meaning of the returned values is the same as for the common reliability indicator, see previous parameter.
			- Out_Of_Tol: float: float Percentage of measured bursts with failed limit check Range: 0 % to 100 % , Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Freq_Acc_Or_Omegai: float: float Frequency accuracy (BR, LE) or initial center frequency error ωi (EDR) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Drift: float: float Frequency drift (BR, LE) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Max_Drift_Rate: float: float Maximal drift rate (BR, LE) Range: -0.99999 MHz/50 μs to 0.99999 MHz/50 μs , Unit: Hz/50 μs
			- Delta_F_1_Avg: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_1_Min: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_1_Max: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_2_Avg: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_2_Min: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_2_Max: float: float Frequency deviation results (BR, LE) Range: 0 Hz to 250 kHz , Unit: Hz
			- Delta_F_299_P: float: float Frequency deviation value Δf2 above which 99.9% of all measured Δf2 values occur (BR, LE) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Omegai_Omega_0: float: No parameter help available
			- Omega_0_Max: float: float Maximum compensated frequency error (EDR) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Rms_Devm: float: RMS DEVM (EDR) Range: 0 to 1
			- Peak_Devm: float: float Peak DEVM (EDR) Range: 0 to 1
			- P_99_Devm: float: float DEVM value below which 99% of all measured DEVM values occur (EDR) Range: 0 to 1
			- Freq_Offset: float: float Frequency offset (LE) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Initial_Freq_Drift: float: float Initial frequency drift (LE) Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- P_99_Devm_Per: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Freq_Acc_Or_Omegai'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift_Rate'),
			ArgStruct.scalar_float('Delta_F_1_Avg'),
			ArgStruct.scalar_float('Delta_F_1_Min'),
			ArgStruct.scalar_float('Delta_F_1_Max'),
			ArgStruct.scalar_float('Delta_F_2_Avg'),
			ArgStruct.scalar_float('Delta_F_2_Min'),
			ArgStruct.scalar_float('Delta_F_2_Max'),
			ArgStruct.scalar_float('Delta_F_299_P'),
			ArgStruct.scalar_float('Omegai_Omega_0'),
			ArgStruct.scalar_float('Omega_0_Max'),
			ArgStruct.scalar_float('Rms_Devm'),
			ArgStruct.scalar_float('Peak_Devm'),
			ArgStruct.scalar_float('P_99_Devm'),
			ArgStruct.scalar_float('Freq_Offset'),
			ArgStruct.scalar_float('Initial_Freq_Drift'),
			ArgStruct.scalar_float('P_99_Devm_Per')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Seg_Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.Freq_Acc_Or_Omegai: float = None
			self.Freq_Drift: float = None
			self.Max_Drift_Rate: float = None
			self.Delta_F_1_Avg: float = None
			self.Delta_F_1_Min: float = None
			self.Delta_F_1_Max: float = None
			self.Delta_F_2_Avg: float = None
			self.Delta_F_2_Min: float = None
			self.Delta_F_2_Max: float = None
			self.Delta_F_299_P: float = None
			self.Omegai_Omega_0: float = None
			self.Omega_0_Max: float = None
			self.Rms_Devm: float = None
			self.Peak_Devm: float = None
			self.P_99_Devm: float = None
			self.Freq_Offset: float = None
			self.Initial_Freq_Drift: float = None
			self.P_99_Devm_Per: float = None

	def fetch(self, segment=repcap.Segment.Default) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:MODulation:CURRent:EXTended \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.modulation.current.extended.fetch(segment = repcap.Segment.Default) \n
		Returns modulation single value results for segment<no> in list mode including Bluetooth version 5.0. The command returns
		all parameters listed below, independent of the selected list mode setup. However, only for some of the parameters
		measured values are available. For the other parameters, only an indicator is returned (e.g. NAV) . \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:MODulation:CURRent:EXTended?', self.__class__.FetchStruct())
