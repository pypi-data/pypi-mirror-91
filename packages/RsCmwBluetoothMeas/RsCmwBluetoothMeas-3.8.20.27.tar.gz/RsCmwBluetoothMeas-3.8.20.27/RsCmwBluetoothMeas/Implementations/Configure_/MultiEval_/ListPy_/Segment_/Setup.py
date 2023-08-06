from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setup:
	"""Setup commands group definition. 16 total commands, 15 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setup", core, parent)

	@property
	def btype(self):
		"""btype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_btype'):
			from .Setup_.Btype import Btype
			self._btype = Btype(self._core, self._base)
		return self._btype

	@property
	def ptype(self):
		"""ptype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptype'):
			from .Setup_.Ptype import Ptype
			self._ptype = Ptype(self._core, self._base)
		return self._ptype

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Setup_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def plength(self):
		"""plength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plength'):
			from .Setup_.Plength import Plength
			self._plength = Plength(self._core, self._base)
		return self._plength

	@property
	def oslots(self):
		"""oslots commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oslots'):
			from .Setup_.Oslots import Oslots
			self._oslots = Oslots(self._core, self._base)
		return self._oslots

	@property
	def slength(self):
		"""slength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slength'):
			from .Setup_.Slength import Slength
			self._slength = Slength(self._core, self._base)
		return self._slength

	@property
	def moException(self):
		"""moException commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_moException'):
			from .Setup_.MoException import MoException
			self._moException = MoException(self._core, self._base)
		return self._moException

	@property
	def envelopePower(self):
		"""envelopePower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_envelopePower'):
			from .Setup_.EnvelopePower import EnvelopePower
			self._envelopePower = EnvelopePower(self._core, self._base)
		return self._envelopePower

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Setup_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def filterPy(self):
		"""filterPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .Setup_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def rtrigger(self):
		"""rtrigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rtrigger'):
			from .Setup_.Rtrigger import Rtrigger
			self._rtrigger = Rtrigger(self._core, self._base)
		return self._rtrigger

	@property
	def singleCmw(self):
		"""singleCmw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_singleCmw'):
			from .Setup_.SingleCmw import SingleCmw
			self._singleCmw = SingleCmw(self._core, self._base)
		return self._singleCmw

	@property
	def phy(self):
		"""phy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phy'):
			from .Setup_.Phy import Phy
			self._phy = Phy(self._core, self._base)
		return self._phy

	@property
	def cscheme(self):
		"""cscheme commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cscheme'):
			from .Setup_.Cscheme import Cscheme
			self._cscheme = Cscheme(self._core, self._base)
		return self._cscheme

	@property
	def extended(self):
		"""extended commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_extended'):
			from .Setup_.Extended import Extended
			self._extended = Extended(self._core, self._base)
		return self._extended

	# noinspection PyTypeChecker
	class SetupStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- Burst_Type: enums.BurstType: BR | EDR | LE Burst type expected in the segment
			- Packet_Type: enums.SegmentPacketType: DH1 | DH3 | DH5 | E21P | E23P | E25P | E31P | E33P | E35P | RFPHytest | ADVertiser Packet type expected in the segment DH1, DH3, DH5: BR packet E21P, E23P, E25P, E31P, E33P, E35P: 2-DH1, 2-DH3, 2-DH5, 3-DH1, 3-DH3, 3-DH5 EDR packet RFPHytest: LE test packet ADVertiser: LE advertiser
			- Pattern_Type: enums.MevPatternType: ALL1 | P11 | OTHer | ALTernating | P44 Payload pattern type expected in the segment ALL1: 11111111 P11: 10101010 OTHer: any pattern except P11, P44 and ALL1 ALTernating: the periodical change of the pattern P11, P44 P44: 11110000
			- Payload_Length: int: numeric Payload length expected in the segment Range: 0 Byte(s) to 1021 Byte(s)
			- No_Of_Off_Slots: int: numeric Number of unused slots between any two occupied slots or slot sequences expected in the segment Range: 1 to 9
			- Segment_Length: int: numeric Number of measured bursts in the segment. The sum of the length of all active segments must not exceed 6700 timeslots (1 timeslot = 625 μs duration) . Range: 1 to 1000
			- Meas_On_Exception: bool: OFF | ON Specifies whether the segment results that the R&S CMW identifies as faulty or inaccurate are rejected. ON: include the erroneous bursts OFF: exclude the erroneous bursts
			- Level: float: numeric Expected nominal power in the segment. The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the data sheet. Unit: dBm
			- Frequency: float: numeric Center frequency for the segment Range: 100 MHz to 6 GHz, Unit: Hz
			- Meas_Filter: enums.FilterWidth: NARRow | WIDE Filter bandwidth for the segment NARRow: narrow-band filter WIDE: wide-band filter
			- Re_Trigger: bool: Optional setting parameter. OFF | ON Specifies whether a trigger event is required for the segment or not. The setting is ignored for the first segment of a measurement. OFF: measure the segment without retrigger ON: trigger event required"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Burst_Type', enums.BurstType),
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

	def set(self, structure: SetupStruct, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup] \n
		Snippet: driver.configure.multiEval.listPy.segment.setup.set(value = [PROPERTY_STRUCT_NAME](), segment = repcap.Segment.Default) \n
		Defines the segment length, the signal properties and the analyzer settings for a selected segment. In general, this
		command must be sent for all segments to be measured. \n
			:param structure: for set value, see the help for SetupStruct structure arguments.
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup', structure)

	def get(self, segment=repcap.Segment.Default) -> SetupStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup] \n
		Snippet: value: SetupStruct = driver.configure.multiEval.listPy.segment.setup.get(segment = repcap.Segment.Default) \n
		Defines the segment length, the signal properties and the analyzer settings for a selected segment. In general, this
		command must be sent for all segments to be measured. \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for SetupStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup?', self.__class__.SetupStruct())

	def clone(self) -> 'Setup':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Setup(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
