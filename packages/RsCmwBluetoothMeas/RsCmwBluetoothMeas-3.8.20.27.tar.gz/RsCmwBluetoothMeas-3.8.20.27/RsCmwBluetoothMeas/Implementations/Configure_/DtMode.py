from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DtMode:
	"""DtMode commands group definition. 17 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dtMode", core, parent)

	@property
	def rxQuality(self):
		"""rxQuality commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rxQuality'):
			from .DtMode_.RxQuality import RxQuality
			self._rxQuality = RxQuality(self._core, self._base)
		return self._rxQuality

	def clone(self) -> 'DtMode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DtMode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
