from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Edrate:
	"""Edrate commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("edrate", core, parent)

	@property
	def ptx(self):
		"""ptx commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_ptx'):
			from .Edrate_.Ptx import Ptx
			self._ptx = Ptx(self._core, self._base)
		return self._ptx

	def clone(self) -> 'Edrate':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Edrate(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
