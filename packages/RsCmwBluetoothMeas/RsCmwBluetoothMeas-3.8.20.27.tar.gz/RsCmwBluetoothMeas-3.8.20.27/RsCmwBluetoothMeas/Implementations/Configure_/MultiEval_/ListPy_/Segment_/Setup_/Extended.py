from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extended:
	"""Extended commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extended", core, parent)

	# noinspection PyTypeChecker
	class ExtendedStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Burst_Type: enums.BurstType: BR | EDR | LE Burst type expected in the segment
			- Phy: enums.LePhysicalType: LE1M | LE2M | LELR Relevant only for LE. Set dummy value for other burst types. LE1M: LE 1 Msymbol/s PHY LE2M: LE 2 Msymbol/s PHY LELR: Long range (LE coded PHY)
			- Coding: enums.CodingScheme: S8 | S2 Coding S = 8 or S = 2 relevant only for LELR PHY Set dummy value for other physical layers.
			- Packet_Type: enums.SegmentPacketType: DH1 | DH3 | DH5 | E21P | E23P | E25P | E31P | E33P | E35P | RFPHytest | ADVertiser Packet type expected in the segment DH1, DH3, DH5: BR packet E21P, E23P, E25P, E31P, E33P, E35P: 2-DH1, 2-DH3, 2-DH5, 3-DH1, 3-DH3, 3-DH5 EDR packet RFPHytest: LE test packet ADVertiser: LE advertiser
			- Pattern_Type: enums.MevPatternType: ALL1 | P11 | OTHer | ALTernating | P44 Payload pattern type expected in the segment ALL1: 11111111 P11: 10101010 OTHer: any pattern except P11, P44 and ALL1 ALTernating: the periodical change of the pattern P11, P44 P44: 11110000
			- Payload_Length: int: numeric Payload length expected in the segment Range: 0 Byte(s) to 1021 Byte(s)
			- No_Of_Off_Slots: int: numeric Number of unused slots between any two occupied slots or slot sequences expected in the segment Range: 1 to 9
			- Segment_Length: int: numeric Number of measured bursts in the segment. The sum of the length of all active segments must not exceed 6700 timeslots (1 timeslot = 625 μs duration) . Range: 1 to 1000
			- Meas_On_Exception: bool: No parameter help available
			- Level: float: numeric Expected nominal power in the segment. The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the data sheet.
			- Frequency: float: numeric Center frequency for the segment Range: 100 MHz to 6 GHz
			- Meas_Filter: enums.FilterWidth: NARRow | WIDE Filter bandwidth for the segment NARRow: narrow-band filter WIDE: wide-band filter
			- Re_Trigger: bool: OFF | ON Specifies whether a trigger event is required for the segment or not. The setting is ignored for the first segment of a measurement. OFF: measure the segment without retrigger ON: trigger event required"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Burst_Type', enums.BurstType),
			ArgStruct.scalar_enum('Phy', enums.LePhysicalType),
			ArgStruct.scalar_enum('Coding', enums.CodingScheme),
			ArgStruct.scalar_enum('Packet_Type', enums.SegmentPacketType),
			ArgStruct.scalar_enum('Pattern_Type', enums.MevPatternType),
			ArgStruct.scalar_int('Payload_Length'),
			ArgStruct.scalar_int('No_Of_Off_Slots'),
			ArgStruct.scalar_int('Segment_Length'),
			ArgStruct.scalar_bool('Meas_On_Exception'),
			ArgStruct.scalar_float('Level'),
			ArgStruct.scalar_float('Frequency'),
			ArgStruct.scalar_enum('Meas_Filter', enums.FilterWidth),
			ArgStruct.scalar_bool('Re_Trigger')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Burst_Type: enums.BurstType = None
			self.Phy: enums.LePhysicalType = None
			self.Coding: enums.CodingScheme = None
			self.Packet_Type: enums.SegmentPacketType = None
			self.Pattern_Type: enums.MevPatternType = None
			self.Payload_Length: int = None
			self.No_Of_Off_Slots: int = None
			self.Segment_Length: int = None
			self.Meas_On_Exception: bool = None
			self.Level: float = None
			self.Frequency: float = None
			self.Meas_Filter: enums.FilterWidth = None
			self.Re_Trigger: bool = None

	def set(self, structure: ExtendedStruct, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:EXTended \n
		Snippet: driver.configure.multiEval.listPy.segment.setup.extended.set(value = [PROPERTY_STRUCT_NAME](), segment = repcap.Segment.Default) \n
		Defines the segment length, the signal properties including Bluetooth version 5 and the analyzer settings for a selected
		segment. In general, this command must be sent for all segments to be measured. \n
			:param structure: for set value, see the help for ExtendedStruct structure arguments.
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:EXTended', structure)

	def get(self, segment=repcap.Segment.Default) -> ExtendedStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:EXTended \n
		Snippet: value: ExtendedStruct = driver.configure.multiEval.listPy.segment.setup.extended.get(segment = repcap.Segment.Default) \n
		Defines the segment length, the signal properties including Bluetooth version 5 and the analyzer settings for a selected
		segment. In general, this command must be sent for all segments to be measured. \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for ExtendedStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:EXTended?', self.__class__.ExtendedStruct())
