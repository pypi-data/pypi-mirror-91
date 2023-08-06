from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Main_State: enums.ResourceState: OFF | RDY | RUN OFF: Measurement switched off, no resources allocated, no results available (when entered after STOP...) RDY: Measurement has been terminated, valid results are available RUN: Measurement running (after INITiate..., READ...) , synchronization pending or adjusted, resources active or queued
			- Sync_State: enums.ResourceState: PEND | ADJ | INV PEND: Waiting for resource allocation, adjustment, hardware switching ('pending') ADJ: All necessary adjustments finished, measurement running ('adjusted') INV: Not applicable because main_state: OFF or RDY ('invalid')
			- Resource_State: enums.ResourceState: QUE | ACT | INV QUE: Measurement without resources, no results available ('queued') ACT: Resources allocated, acquisition of results in progress but not complete ('active') INV: Not applicable because main_state: OFF or RDY ('invalid')"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Main_State', enums.ResourceState),
			ArgStruct.scalar_enum('Sync_State', enums.ResourceState),
			ArgStruct.scalar_enum('Resource_State', enums.ResourceState)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Main_State: enums.ResourceState = None
			self.Sync_State: enums.ResourceState = None
			self.Resource_State: enums.ResourceState = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:STATe:ALL \n
		Snippet: value: FetchStruct = driver.multiEval.state.all.fetch() \n
		Queries the main measurement state and the measurement substates. Both measurement substates are relevant for running
		measurements only. Use FETCh:...:STATe? to query the main measurement state only. Use INITiate..., STOP..., ABORt...
		to change the measurement state. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:STATe:ALL?', self.__class__.FetchStruct())
