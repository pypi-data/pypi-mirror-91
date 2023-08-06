from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 14 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	@property
	def segment(self):
		"""segment commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_segment'):
			from .ListPy_.Segment import Segment
			self._segment = Segment(self._core, self._base)
		return self._segment

	def clone(self) -> 'ListPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ListPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
