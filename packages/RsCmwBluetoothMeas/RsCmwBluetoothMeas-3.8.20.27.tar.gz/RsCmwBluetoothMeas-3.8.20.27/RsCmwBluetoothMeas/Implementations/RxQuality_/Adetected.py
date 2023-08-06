from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adetected:
	"""Adetected commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adetected", core, parent)

	@property
	def aaddress(self):
		"""aaddress commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aaddress'):
			from .Adetected_.Aaddress import Aaddress
			self._aaddress = Aaddress(self._core, self._base)
		return self._aaddress

	def clone(self) -> 'Adetected':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Adetected(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
