from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rdevices:
	"""Rdevices commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rdevices", core, parent)

	def set(self) -> None:
		"""SCPI: CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RDEVices \n
		Snippet: driver.call.dtMode.lowEnergy.rdevices.set() \n
		Discovers the DUTs connected to USB ports via a USB-to-RS232 adapter. \n
		"""
		self._core.io.write(f'CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RDEVices')

	def set_with_opc(self) -> None:
		"""SCPI: CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RDEVices \n
		Snippet: driver.call.dtMode.lowEnergy.rdevices.set_with_opc() \n
		Discovers the DUTs connected to USB ports via a USB-to-RS232 adapter. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CALL:BLUetooth:MEASurement<Instance>:DTMode:LENergy:RDEVices')
