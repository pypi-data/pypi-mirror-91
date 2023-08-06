from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Segment:
	"""Segment commands group definition. 14 total commands, 5 Sub-groups, 0 group commands
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
	def pencoding(self):
		"""pencoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pencoding'):
			from .Segment_.Pencoding import Pencoding
			self._pencoding = Pencoding(self._core, self._base)
		return self._pencoding

	@property
	def sacp(self):
		"""sacp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sacp'):
			from .Segment_.Sacp import Sacp
			self._sacp = Sacp(self._core, self._base)
		return self._sacp

	@property
	def soBw(self):
		"""soBw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_soBw'):
			from .Segment_.SoBw import SoBw
			self._soBw = SoBw(self._core, self._base)
		return self._soBw

	@property
	def modulation(self):
		"""modulation commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_modulation'):
			from .Segment_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def powerVsTime(self):
		"""powerVsTime commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_powerVsTime'):
			from .Segment_.PowerVsTime import PowerVsTime
			self._powerVsTime = PowerVsTime(self._core, self._base)
		return self._powerVsTime

	def clone(self) -> 'Segment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Segment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
