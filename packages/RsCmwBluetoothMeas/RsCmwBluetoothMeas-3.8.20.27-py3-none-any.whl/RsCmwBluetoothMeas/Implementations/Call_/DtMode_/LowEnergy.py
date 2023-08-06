from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	@property
	def rdevices(self):
		"""rdevices commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rdevices'):
			from .LowEnergy_.Rdevices import Rdevices
			self._rdevices = Rdevices(self._core, self._base)
		return self._rdevices

	# noinspection PyTypeChecker
	def get_rresult(self) -> enums.Result:
		"""SCPI: CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RRESult \n
		Snippet: value: enums.Result = driver.call.dtMode.lowEnergy.get_rresult() \n
		Returns the result of reset DUT command. Refer tomethod RsCmwBluetoothMeas.Call.DtMode.LowEnergy.reset. \n
			:return: result: FAIL | PASS
		"""
		response = self._core.io.query_str('CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RRESult?')
		return Conversions.str_to_scalar_enum(response, enums.Result)

	def reset(self) -> None:
		"""SCPI: CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RESet \n
		Snippet: driver.call.dtMode.lowEnergy.reset() \n
		Sends the HCI reset command to the EUT via USB. Check the execution via method RsCmwBluetoothMeas.Call.DtMode.LowEnergy.
		rresult. \n
		"""
		self._core.io.write(f'CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RESet \n
		Snippet: driver.call.dtMode.lowEnergy.reset_with_opc() \n
		Sends the HCI reset command to the EUT via USB. Check the execution via method RsCmwBluetoothMeas.Call.DtMode.LowEnergy.
		rresult. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RESet')

	def clone(self) -> 'LowEnergy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LowEnergy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
