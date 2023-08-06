from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nmode:
	"""Nmode commands group definition. 12 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nmode", core, parent)

	@property
	def classic(self):
		"""classic commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_classic'):
			from .Nmode_.Classic import Classic
			self._classic = Classic(self._core, self._base)
		return self._classic

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Nmode_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	def clone(self) -> 'Nmode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nmode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
