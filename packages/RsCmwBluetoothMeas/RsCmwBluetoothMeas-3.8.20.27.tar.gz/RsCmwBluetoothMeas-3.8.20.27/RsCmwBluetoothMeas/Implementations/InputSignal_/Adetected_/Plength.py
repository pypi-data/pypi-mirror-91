from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Plength:
	"""Plength commands group definition. 5 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("plength", core, parent)

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Plength_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	@property
	def edrate(self):
		"""edrate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_edrate'):
			from .Plength_.Edrate import Edrate
			self._edrate = Edrate(self._core, self._base)
		return self._edrate

	@property
	def brate(self):
		"""brate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_brate'):
			from .Plength_.Brate import Brate
			self._brate = Brate(self._core, self._base)
		return self._brate

	def clone(self) -> 'Plength':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Plength(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
