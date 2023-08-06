from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trace:
	"""Trace commands group definition. 72 total commands, 13 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trace", core, parent)

	@property
	def frange(self):
		"""frange commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frange'):
			from .Trace_.Frange import Frange
			self._frange = Frange(self._core, self._base)
		return self._frange

	@property
	def soBw(self):
		"""soBw commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_soBw'):
			from .Trace_.SoBw import SoBw
			self._soBw = SoBw(self._core, self._base)
		return self._soBw

	@property
	def sacp(self):
		"""sacp commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sacp'):
			from .Trace_.Sacp import Sacp
			self._sacp = Sacp(self._core, self._base)
		return self._sacp

	@property
	def sgacp(self):
		"""sgacp commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sgacp'):
			from .Trace_.Sgacp import Sgacp
			self._sgacp = Sgacp(self._core, self._base)
		return self._sgacp

	@property
	def devMagnitude(self):
		"""devMagnitude commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_devMagnitude'):
			from .Trace_.DevMagnitude import DevMagnitude
			self._devMagnitude = DevMagnitude(self._core, self._base)
		return self._devMagnitude

	@property
	def pdifference(self):
		"""pdifference commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdifference'):
			from .Trace_.Pdifference import Pdifference
			self._pdifference = Pdifference(self._core, self._base)
		return self._pdifference

	@property
	def iqAbs(self):
		"""iqAbs commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_iqAbs'):
			from .Trace_.IqAbs import IqAbs
			self._iqAbs = IqAbs(self._core, self._base)
		return self._iqAbs

	@property
	def iqDifference(self):
		"""iqDifference commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_iqDifference'):
			from .Trace_.IqDifference import IqDifference
			self._iqDifference = IqDifference(self._core, self._base)
		return self._iqDifference

	@property
	def iqError(self):
		"""iqError commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_iqError'):
			from .Trace_.IqError import IqError
			self._iqError = IqError(self._core, self._base)
		return self._iqError

	@property
	def fdeviation(self):
		"""fdeviation commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Trace_.Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._base)
		return self._fdeviation

	@property
	def spower(self):
		"""spower commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_spower'):
			from .Trace_.Spower import Spower
			self._spower = Spower(self._core, self._base)
		return self._spower

	@property
	def pdeviation(self):
		"""pdeviation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Trace_.Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._base)
		return self._pdeviation

	@property
	def powerVsTime(self):
		"""powerVsTime commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_powerVsTime'):
			from .Trace_.PowerVsTime import PowerVsTime
			self._powerVsTime = PowerVsTime(self._core, self._base)
		return self._powerVsTime

	def clone(self) -> 'Trace':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trace(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
