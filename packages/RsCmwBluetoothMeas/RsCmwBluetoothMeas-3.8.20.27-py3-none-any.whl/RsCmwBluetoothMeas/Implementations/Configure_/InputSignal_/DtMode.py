from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DtMode:
	"""DtMode commands group definition. 9 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dtMode", core, parent)

	@property
	def rxQuality(self):
		"""rxQuality commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rxQuality'):
			from .DtMode_.RxQuality import RxQuality
			self._rxQuality = RxQuality(self._core, self._base)
		return self._rxQuality

	@property
	def plength(self):
		"""plength commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_plength'):
			from .DtMode_.Plength import Plength
			self._plength = Plength(self._core, self._base)
		return self._plength

	@property
	def pattern(self):
		"""pattern commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pattern'):
			from .DtMode_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	def clone(self) -> 'DtMode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DtMode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
