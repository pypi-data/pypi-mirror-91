from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	@property
	def lrange(self):
		"""lrange commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lrange'):
			from .LowEnergy_.Lrange import Lrange
			self._lrange = Lrange(self._core, self._base)
		return self._lrange

	@property
	def le2M(self):
		"""le2M commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_le2M'):
			from .LowEnergy_.Le2M import Le2M
			self._le2M = Le2M(self._core, self._base)
		return self._le2M

	@property
	def le1M(self):
		"""le1M commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_le1M'):
			from .LowEnergy_.Le1M import Le1M
			self._le1M = Le1M(self._core, self._base)
		return self._le1M

	def clone(self) -> 'LowEnergy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LowEnergy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
