from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scount:
	"""Scount commands group definition. 7 total commands, 6 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scount", core, parent)

	@property
	def mscalar(self):
		"""mscalar commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mscalar'):
			from .Scount_.Mscalar import Mscalar
			self._mscalar = Mscalar(self._core, self._base)
		return self._mscalar

	@property
	def pencoding(self):
		"""pencoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pencoding'):
			from .Scount_.Pencoding import Pencoding
			self._pencoding = Pencoding(self._core, self._base)
		return self._pencoding

	@property
	def pscalar(self):
		"""pscalar commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pscalar'):
			from .Scount_.Pscalar import Pscalar
			self._pscalar = Pscalar(self._core, self._base)
		return self._pscalar

	@property
	def soBw(self):
		"""soBw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_soBw'):
			from .Scount_.SoBw import SoBw
			self._soBw = SoBw(self._core, self._base)
		return self._soBw

	@property
	def sacp(self):
		"""sacp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sacp'):
			from .Scount_.Sacp import Sacp
			self._sacp = Sacp(self._core, self._base)
		return self._sacp

	@property
	def sgacp(self):
		"""sgacp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgacp'):
			from .Scount_.Sgacp import Sgacp
			self._sgacp = Sgacp(self._core, self._base)
		return self._sgacp

	# noinspection PyTypeChecker
	class ScountStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Mod_Stat_Count: int: numeric Statistic count for the statistical modulation measurement Range: 1 to 1000
			- Power_Stat_Count: int: numeric Statistic count for the statistical power measurement Range: 1 to 1000
			- Spec_Obw_Stat_Cnt: int: numeric Statistic count for the spectrum 20 dB bandwidth measurement (BR) Range: 1 to 1000
			- Spec_Acp_Stat_Cnt: int: numeric Statistic count for the spectrum ACP measurement (BR, LE) Range: 1 to 1000
			- Spec_Gat_Acp_Stat_Cnt: int: numeric Statistic count for the spectrum gated ACP measurement (EDR) Range: 1 to 1000"""
		__meta_args_list = [
			ArgStruct.scalar_int('Mod_Stat_Count'),
			ArgStruct.scalar_int('Power_Stat_Count'),
			ArgStruct.scalar_int('Spec_Obw_Stat_Cnt'),
			ArgStruct.scalar_int('Spec_Acp_Stat_Cnt'),
			ArgStruct.scalar_int('Spec_Gat_Acp_Stat_Cnt')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mod_Stat_Count: int = None
			self.Power_Stat_Count: int = None
			self.Spec_Obw_Stat_Cnt: int = None
			self.Spec_Acp_Stat_Cnt: int = None
			self.Spec_Gat_Acp_Stat_Cnt: int = None

	def set(self, structure: ScountStruct, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:SCOunt \n
		Snippet: driver.configure.multiEval.listPy.segment.scount.set(value = [PROPERTY_STRUCT_NAME](), segment = repcap.Segment.Default) \n
		Defines the statistic count for the particular measurement type in the segment. \n
			:param structure: for set value, see the help for ScountStruct structure arguments.
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SCOunt', structure)

	def get(self, segment=repcap.Segment.Default) -> ScountStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:SCOunt \n
		Snippet: value: ScountStruct = driver.configure.multiEval.listPy.segment.scount.get(segment = repcap.Segment.Default) \n
		Defines the statistic count for the particular measurement type in the segment. \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for ScountStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SCOunt?', self.__class__.ScountStruct())

	def clone(self) -> 'Scount':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scount(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
