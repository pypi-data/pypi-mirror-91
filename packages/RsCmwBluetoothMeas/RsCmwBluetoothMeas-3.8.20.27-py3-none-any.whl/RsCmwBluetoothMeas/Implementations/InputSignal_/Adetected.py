from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adetected:
	"""Adetected commands group definition. 23 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adetected", core, parent)

	@property
	def cte(self):
		"""cte commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cte'):
			from .Adetected_.Cte import Cte
			self._cte = Cte(self._core, self._base)
		return self._cte

	@property
	def coding(self):
		"""coding commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_coding'):
			from .Adetected_.Coding import Coding
			self._coding = Coding(self._core, self._base)
		return self._coding

	@property
	def plength(self):
		"""plength commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_plength'):
			from .Adetected_.Plength import Plength
			self._plength = Plength(self._core, self._base)
		return self._plength

	@property
	def ptype(self):
		"""ptype commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptype'):
			from .Adetected_.Ptype import Ptype
			self._ptype = Ptype(self._core, self._base)
		return self._ptype

	@property
	def pattern(self):
		"""pattern commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pattern'):
			from .Adetected_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def aaddress(self):
		"""aaddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_aaddress'):
			from .Adetected_.Aaddress import Aaddress
			self._aaddress = Aaddress(self._core, self._base)
		return self._aaddress

	@property
	def pduType(self):
		"""pduType commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pduType'):
			from .Adetected_.PduType import PduType
			self._pduType = PduType(self._core, self._base)
		return self._pduType

	@property
	def noSlots(self):
		"""noSlots commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_noSlots'):
			from .Adetected_.NoSlots import NoSlots
			self._noSlots = NoSlots(self._core, self._base)
		return self._noSlots

	def clone(self) -> 'Adetected':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Adetected(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
