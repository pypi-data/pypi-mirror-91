from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sacp:
	"""Sacp commands group definition. 3 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sacp", core, parent)

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Sacp_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	@property
	def brate(self):
		"""brate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_brate'):
			from .Sacp_.Brate import Brate
			self._brate = Brate(self._core, self._base)
		return self._brate

	def clone(self) -> 'Sacp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sacp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
