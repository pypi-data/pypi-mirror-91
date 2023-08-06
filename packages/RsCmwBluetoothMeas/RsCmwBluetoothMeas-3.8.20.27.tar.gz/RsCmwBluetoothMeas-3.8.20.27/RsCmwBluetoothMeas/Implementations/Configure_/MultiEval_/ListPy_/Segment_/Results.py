from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Results:
	"""Results commands group definition. 7 total commands, 6 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("results", core, parent)

	@property
	def mscalar(self):
		"""mscalar commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mscalar'):
			from .Results_.Mscalar import Mscalar
			self._mscalar = Mscalar(self._core, self._base)
		return self._mscalar

	@property
	def pencoding(self):
		"""pencoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pencoding'):
			from .Results_.Pencoding import Pencoding
			self._pencoding = Pencoding(self._core, self._base)
		return self._pencoding

	@property
	def pscalar(self):
		"""pscalar commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pscalar'):
			from .Results_.Pscalar import Pscalar
			self._pscalar = Pscalar(self._core, self._base)
		return self._pscalar

	@property
	def soBw(self):
		"""soBw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_soBw'):
			from .Results_.SoBw import SoBw
			self._soBw = SoBw(self._core, self._base)
		return self._soBw

	@property
	def sacp(self):
		"""sacp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sacp'):
			from .Results_.Sacp import Sacp
			self._sacp = Sacp(self._core, self._base)
		return self._sacp

	@property
	def sgacp(self):
		"""sgacp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgacp'):
			from .Results_.Sgacp import Sgacp
			self._sgacp = Sgacp(self._core, self._base)
		return self._sgacp

	# noinspection PyTypeChecker
	class ResultsStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Enable_Mod_Scalar: bool: OFF | ON Enable/disable statistical modulation results
			- Enable_Pow_Scalar: bool: OFF | ON Enable/disable statistical power results
			- Enable_Spec_Obw: bool: OFF | ON Enable/disable the spectrum 20 dB bandwidth results (BR)
			- Enable_Spec_Acp: bool: OFF | ON Enable/disable the spectrum ACP results (BR, LE)
			- Enable_Spec_Gat_Acp: bool: OFF | ON Enable/disable the spectrum gated ACP results (EDR)"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Mod_Scalar'),
			ArgStruct.scalar_bool('Enable_Pow_Scalar'),
			ArgStruct.scalar_bool('Enable_Spec_Obw'),
			ArgStruct.scalar_bool('Enable_Spec_Acp'),
			ArgStruct.scalar_bool('Enable_Spec_Gat_Acp')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Mod_Scalar: bool = None
			self.Enable_Pow_Scalar: bool = None
			self.Enable_Spec_Obw: bool = None
			self.Enable_Spec_Acp: bool = None
			self.Enable_Spec_Gat_Acp: bool = None

	def set(self, structure: ResultsStruct, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:RESults \n
		Snippet: driver.configure.multiEval.listPy.segment.results.set(value = [PROPERTY_STRUCT_NAME](), segment = repcap.Segment.Default) \n
		Enables or disables the evaluation of the particular measurement type in the segment. \n
			:param structure: for set value, see the help for ResultsStruct structure arguments.
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:RESults', structure)

	def get(self, segment=repcap.Segment.Default) -> ResultsStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:RESults \n
		Snippet: value: ResultsStruct = driver.configure.multiEval.listPy.segment.results.get(segment = repcap.Segment.Default) \n
		Enables or disables the evaluation of the particular measurement type in the segment. \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for ResultsStruct structure arguments."""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:RESults?', self.__class__.ResultsStruct())

	def clone(self) -> 'Results':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Results(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
