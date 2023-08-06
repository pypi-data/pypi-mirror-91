from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NoSlots:
	"""NoSlots commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("noSlots", core, parent)

	@property
	def edrate(self):
		"""edrate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_edrate'):
			from .NoSlots_.Edrate import Edrate
			self._edrate = Edrate(self._core, self._base)
		return self._edrate

	@property
	def brate(self):
		"""brate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_brate'):
			from .NoSlots_.Brate import Brate
			self._brate = Brate(self._core, self._base)
		return self._brate

	def clone(self) -> 'NoSlots':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NoSlots(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
