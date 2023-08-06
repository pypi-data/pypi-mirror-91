from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trx:
	"""Trx commands group definition. 9 total commands, 5 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trx", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Trx_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def spot(self):
		"""spot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spot'):
			from .Trx_.Spot import Spot
			self._spot = Spot(self._core, self._base)
		return self._spot

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Trx_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Trx_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def acp(self):
		"""acp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acp'):
			from .Trx_.Acp import Acp
			self._acp = Acp(self._core, self._base)
		return self._acp

	def initiate(self) -> None:
		"""SCPI: INITiate:BLUetooth:MEASurement<Instance>:TRX \n
		Snippet: driver.trx.initiate() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'INITiate:BLUetooth:MEASurement<Instance>:TRX')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:BLUetooth:MEASurement<Instance>:TRX \n
		Snippet: driver.trx.initiate_with_opc() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:BLUetooth:MEASurement<Instance>:TRX')

	def stop(self) -> None:
		"""SCPI: STOP:BLUetooth:MEASurement<Instance>:TRX \n
		Snippet: driver.trx.stop() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'STOP:BLUetooth:MEASurement<Instance>:TRX')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:BLUetooth:MEASurement<Instance>:TRX \n
		Snippet: driver.trx.stop_with_opc() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:BLUetooth:MEASurement<Instance>:TRX')

	def abort(self) -> None:
		"""SCPI: ABORt:BLUetooth:MEASurement<Instance>:TRX \n
		Snippet: driver.trx.abort() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'ABORt:BLUetooth:MEASurement<Instance>:TRX')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:BLUetooth:MEASurement<Instance>:TRX \n
		Snippet: driver.trx.abort_with_opc() \n
			INTRO_CMD_HELP: Starts, stops, or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:BLUetooth:MEASurement<Instance>:TRX')

	def clone(self) -> 'Trx':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trx(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
