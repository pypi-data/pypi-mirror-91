from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxQuality:
	"""RxQuality commands group definition. 26 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxQuality", core, parent)

	@property
	def search(self):
		"""search commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_search'):
			from .RxQuality_.Search import Search
			self._search = Search(self._core, self._base)
		return self._search

	@property
	def per(self):
		"""per commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_per'):
			from .RxQuality_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	def clone(self) -> 'RxQuality':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxQuality(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
