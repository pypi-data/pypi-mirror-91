from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pencoding:
	"""Pencoding commands group definition. 7 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pencoding", core, parent)

	@property
	def ssequence(self):
		"""ssequence commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ssequence'):
			from .Pencoding_.Ssequence import Ssequence
			self._ssequence = Ssequence(self._core, self._base)
		return self._ssequence

	@property
	def edrate(self):
		"""edrate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_edrate'):
			from .Pencoding_.Edrate import Edrate
			self._edrate = Edrate(self._core, self._base)
		return self._edrate

	def clone(self) -> 'Pencoding':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pencoding(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
