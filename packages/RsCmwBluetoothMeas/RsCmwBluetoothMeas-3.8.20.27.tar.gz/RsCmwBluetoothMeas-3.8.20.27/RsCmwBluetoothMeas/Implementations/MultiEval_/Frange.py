from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frange:
	"""Frange commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frange", core, parent)

	@property
	def brate(self):
		"""brate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_brate'):
			from .Frange_.Brate import Brate
			self._brate = Brate(self._core, self._base)
		return self._brate

	def clone(self) -> 'Frange':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frange(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
