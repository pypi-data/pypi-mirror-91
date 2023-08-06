from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2M:
	"""Le2M commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le2M", core, parent)

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Le2M_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def units(self):
		"""units commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_units'):
			from .Le2M_.Units import Units
			self._units = Units(self._core, self._base)
		return self._units

	def clone(self) -> 'Le2M':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Le2M(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
