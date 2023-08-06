from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerVsTime:
	"""PowerVsTime commands group definition. 108 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("powerVsTime", core, parent)

	@property
	def nmode(self):
		"""nmode commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmode'):
			from .PowerVsTime_.Nmode import Nmode
			self._nmode = Nmode(self._core, self._base)
		return self._nmode

	@property
	def edrate(self):
		"""edrate commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_edrate'):
			from .PowerVsTime_.Edrate import Edrate
			self._edrate = Edrate(self._core, self._base)
		return self._edrate

	@property
	def brate(self):
		"""brate commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_brate'):
			from .PowerVsTime_.Brate import Brate
			self._brate = Brate(self._core, self._base)
		return self._brate

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .PowerVsTime_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	def clone(self) -> 'PowerVsTime':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PowerVsTime(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
