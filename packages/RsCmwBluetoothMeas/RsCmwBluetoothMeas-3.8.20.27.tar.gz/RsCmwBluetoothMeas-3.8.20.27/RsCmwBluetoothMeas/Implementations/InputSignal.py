from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputSignal:
	"""InputSignal commands group definition. 23 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inputSignal", core, parent)

	@property
	def adetected(self):
		"""adetected commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_adetected'):
			from .InputSignal_.Adetected import Adetected
			self._adetected = Adetected(self._core, self._base)
		return self._adetected

	def clone(self) -> 'InputSignal':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InputSignal(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
