from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Diagnostic:
	"""Diagnostic commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("diagnostic", core, parent)

	@property
	def rfControl(self):
		"""rfControl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfControl'):
			from .Diagnostic_.RfControl import RfControl
			self._rfControl = RfControl(self._core, self._base)
		return self._rfControl

	@property
	def bluetooth(self):
		"""bluetooth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bluetooth'):
			from .Diagnostic_.Bluetooth import Bluetooth
			self._bluetooth = Bluetooth(self._core, self._base)
		return self._bluetooth

	def clone(self) -> 'Diagnostic':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Diagnostic(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
