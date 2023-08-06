from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Aaddress:
	"""Aaddress commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aaddress", core, parent)

	def fetch(self) -> str:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:RXQuality:ADETected:AADDress \n
		Snippet: value: str = driver.rxQuality.adetected.aaddress.fetch() \n
		Queries the automatically detected advertiser address of EUT. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: adv_address: string 12-digit hexadecimal number Range: #H0 to #HFFFFFFFFFFFF"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:RXQuality:ADETected:AADDress?', suppressed)
		return trim_str_response(response)
