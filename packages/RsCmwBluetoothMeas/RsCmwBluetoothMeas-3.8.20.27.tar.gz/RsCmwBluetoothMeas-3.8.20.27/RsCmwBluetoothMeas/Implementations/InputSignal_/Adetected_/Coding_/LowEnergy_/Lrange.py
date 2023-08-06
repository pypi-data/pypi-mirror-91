from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lrange:
	"""Lrange commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lrange", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.CodingScheme:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:ISIGnal:ADETected:CODing:LENergy:LRANge \n
		Snippet: value: enums.CodingScheme = driver.inputSignal.adetected.coding.lowEnergy.lrange.fetch() \n
		Returns the detected forward error correction coding for LE coded PHY. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: coding: S8 | S2 Coding S = 8 or S = 2"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:ISIGnal:ADETected:CODing:LENergy:LRANge?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.CodingScheme)
