from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coding:
	"""Coding commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coding", core, parent)

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Coding_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	def clone(self) -> 'Coding':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Coding(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
