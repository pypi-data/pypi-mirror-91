from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaProtocol:
	"""MaProtocol commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maProtocol", core, parent)

	def set(self) -> None:
		"""SCPI: ROUTe:BLUetooth:MEASurement<Instance>:SCENario:MAPRotocol \n
		Snippet: driver.route.scenario.maProtocol.set() \n
		No command help available \n
		"""
		self._core.io.write(f'ROUTe:BLUetooth:MEASurement<Instance>:SCENario:MAPRotocol')

	def set_with_opc(self) -> None:
		"""SCPI: ROUTe:BLUetooth:MEASurement<Instance>:SCENario:MAPRotocol \n
		Snippet: driver.route.scenario.maProtocol.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ROUTe:BLUetooth:MEASurement<Instance>:SCENario:MAPRotocol')
