from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .State_.All import All
			self._all = All(self._core, self._base)
		return self._all

	# noinspection PyTypeChecker
	def fetch(self) -> enums.ResourceState:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:RXQuality:STATe \n
		Snippet: value: enums.ResourceState = driver.rxQuality.state.fetch() \n
		Queries the main measurement state. Use FETCh:...:STATe:ALL? to query the measurement state including the substates. Use
		INITiate..., STOP..., ABORt... to change the measurement state. \n
			:return: meas_state: OFF | RDY | RUN OFF: measurement switched off, no resources allocated, no results available (when entered after ABORt...) RDY: measurement has been terminated, valid results are available RUN: measurement running (after INITiate..., READ...) , synchronization pending or adjusted, resources active or queued"""
		response = self._core.io.query_str(f'FETCh:BLUetooth:MEASurement<Instance>:RXQuality:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.ResourceState)

	def clone(self) -> 'State':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = State(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
