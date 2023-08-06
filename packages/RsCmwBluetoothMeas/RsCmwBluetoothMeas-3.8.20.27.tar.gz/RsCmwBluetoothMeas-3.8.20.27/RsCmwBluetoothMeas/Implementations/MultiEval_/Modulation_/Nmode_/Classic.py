from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Classic:
	"""Classic commands group definition. 21 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("classic", core, parent)

	@property
	def xmaximum(self):
		"""xmaximum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_xmaximum'):
			from .Classic_.Xmaximum import Xmaximum
			self._xmaximum = Xmaximum(self._core, self._base)
		return self._xmaximum

	@property
	def xminimum(self):
		"""xminimum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_xminimum'):
			from .Classic_.Xminimum import Xminimum
			self._xminimum = Xminimum(self._core, self._base)
		return self._xminimum

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_maximum'):
			from .Classic_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .Classic_.Average import Average
			self._average = Average(self._core, self._base)
		return self._average

	@property
	def minimum(self):
		"""minimum commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_minimum'):
			from .Classic_.Minimum import Minimum
			self._minimum = Minimum(self._core, self._base)
		return self._minimum

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .Classic_.Current import Current
			self._current = Current(self._core, self._base)
		return self._current

	@property
	def standardDev(self):
		"""standardDev commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_standardDev'):
			from .Classic_.StandardDev import StandardDev
			self._standardDev = StandardDev(self._core, self._base)
		return self._standardDev

	def clone(self) -> 'Classic':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Classic(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
