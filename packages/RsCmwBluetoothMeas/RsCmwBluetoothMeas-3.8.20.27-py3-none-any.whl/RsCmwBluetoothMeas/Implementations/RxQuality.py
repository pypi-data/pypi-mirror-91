from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxQuality:
	"""RxQuality commands group definition. 10 total commands, 5 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rxQuality", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .RxQuality_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def sensitivity(self):
		"""sensitivity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sensitivity'):
			from .RxQuality_.Sensitivity import Sensitivity
			self._sensitivity = Sensitivity(self._core, self._base)
		return self._sensitivity

	@property
	def spotCheck(self):
		"""spotCheck commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spotCheck'):
			from .RxQuality_.SpotCheck import SpotCheck
			self._spotCheck = SpotCheck(self._core, self._base)
		return self._spotCheck

	@property
	def per(self):
		"""per commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_per'):
			from .RxQuality_.Per import Per
			self._per = Per(self._core, self._base)
		return self._per

	@property
	def adetected(self):
		"""adetected commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adetected'):
			from .RxQuality_.Adetected import Adetected
			self._adetected = Adetected(self._core, self._base)
		return self._adetected

	def initiate(self) -> None:
		"""SCPI: INITiate:BLUetooth:MEASurement<Instance>:RXQuality \n
		Snippet: driver.rxQuality.initiate() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'INITiate:BLUetooth:MEASurement<Instance>:RXQuality')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:BLUetooth:MEASurement<Instance>:RXQuality \n
		Snippet: driver.rxQuality.initiate_with_opc() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:BLUetooth:MEASurement<Instance>:RXQuality')

	def stop(self) -> None:
		"""SCPI: STOP:BLUetooth:MEASurement<Instance>:RXQuality \n
		Snippet: driver.rxQuality.stop() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'STOP:BLUetooth:MEASurement<Instance>:RXQuality')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:BLUetooth:MEASurement<Instance>:RXQuality \n
		Snippet: driver.rxQuality.stop_with_opc() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:BLUetooth:MEASurement<Instance>:RXQuality')

	def abort(self) -> None:
		"""SCPI: ABORt:BLUetooth:MEASurement<Instance>:RXQuality \n
		Snippet: driver.rxQuality.abort() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'ABORt:BLUetooth:MEASurement<Instance>:RXQuality')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:BLUetooth:MEASurement<Instance>:RXQuality \n
		Snippet: driver.rxQuality.abort_with_opc() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:BLUetooth:MEASurement<Instance>:RXQuality')

	def clone(self) -> 'RxQuality':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxQuality(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
