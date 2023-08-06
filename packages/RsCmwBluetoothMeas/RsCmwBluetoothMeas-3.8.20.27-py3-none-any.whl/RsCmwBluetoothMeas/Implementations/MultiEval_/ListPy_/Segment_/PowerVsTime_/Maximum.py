from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Seg_Reliability: int: decimal Reliability indicator for the segment. The meaning of the returned values is the same as for the common reliability indicator, see previous parameter.
			- Out_Of_Tol: float: float Percentage of measured bursts with failed limit check Range: 0 % to 100 %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Peak_Power: float: float Peak power Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Leakage_Power: float: float Leakage power (BR, LE) Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Gfsk_Power: float: float Average power within the GFSK modulated part of the burst (EDR) Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Dpsk_Power: float: float Average power within the DPSK modulated part of the burst (EDR) Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Dpsk_Minus_Gfsk: float: float Difference between the 8_DPSKPower and 7_GFSKPower (EDR) Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Guard_Period: float: float Length of the guard band between the packet header and the EDR synchronization sequence (EDR) Range: 0 µs to 9.99 µs, Unit: s
			- Peak_Minus_Avg: float: float Difference between the peak power and the average power in the burst (LE) Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Leakage_Power'),
			ArgStruct.scalar_float('Gfsk_Power'),
			ArgStruct.scalar_float('Dpsk_Power'),
			ArgStruct.scalar_float('Dpsk_Minus_Gfsk'),
			ArgStruct.scalar_float('Guard_Period'),
			ArgStruct.scalar_float('Peak_Minus_Avg')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.Peak_Power: float = None
			self.Leakage_Power: float = None
			self.Gfsk_Power: float = None
			self.Dpsk_Power: float = None
			self.Dpsk_Minus_Gfsk: float = None
			self.Guard_Period: float = None
			self.Peak_Minus_Avg: float = None

	def fetch(self, segment=repcap.Segment.Default) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:PVTime:MAXimum \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.powerVsTime.maximum.fetch(segment = repcap.Segment.Default) \n
		Returns statistical power vs. time single value results for segment<no> in list mode. The command returns all parameters
		listed below, independent of the selected list mode setup. However, only for some of the parameters measured values are
		available. For the other parameters, only an indicator is returned (e.g. NAV) . \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:PVTime:MAXimum?', self.__class__.FetchStruct())
