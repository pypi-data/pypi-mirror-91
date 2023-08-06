from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Segment:
	"""Segment commands group definition. 30 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: Segment, default value after init: Segment.S1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("segment", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_segment_get', 'repcap_segment_set', repcap.Segment.S1)

	def repcap_segment_set(self, enum_value: repcap.Segment) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Segment.Default
		Default value after init: Segment.S1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_segment_get(self) -> repcap.Segment:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def setup(self):
		"""setup commands group. 15 Sub-classes, 1 commands."""
		if not hasattr(self, '_setup'):
			from .Segment_.Setup import Setup
			self._setup = Setup(self._core, self._base)
		return self._setup

	@property
	def scount(self):
		"""scount commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_scount'):
			from .Segment_.Scount import Scount
			self._scount = Scount(self._core, self._base)
		return self._scount

	@property
	def results(self):
		"""results commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_results'):
			from .Segment_.Results import Results
			self._results = Results(self._core, self._base)
		return self._results

	def clone(self) -> 'Segment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Segment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
