from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxQuality:
	"""RxQuality commands group definition. 17 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxQuality", core, parent)

	@property
	def smIndex(self):
		"""smIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smIndex'):
			from .RxQuality_.SmIndex import SmIndex
			self._smIndex = SmIndex(self._core, self._base)
		return self._smIndex

	@property
	def eattenuation(self):
		"""eattenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eattenuation'):
			from .RxQuality_.Eattenuation import Eattenuation
			self._eattenuation = Eattenuation(self._core, self._base)
		return self._eattenuation

	@property
	def search(self):
		"""search commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_search'):
			from .RxQuality_.Search import Search
			self._search = Search(self._core, self._base)
		return self._search

	@property
	def rintegrity(self):
		"""rintegrity commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rintegrity'):
			from .RxQuality_.Rintegrity import Rintegrity
			self._rintegrity = Rintegrity(self._core, self._base)
		return self._rintegrity

	@property
	def per(self):
		"""per commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_per'):
			from .RxQuality_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	@property
	def limit(self):
		"""limit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .RxQuality_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	def clone(self) -> 'RxQuality':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxQuality(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
