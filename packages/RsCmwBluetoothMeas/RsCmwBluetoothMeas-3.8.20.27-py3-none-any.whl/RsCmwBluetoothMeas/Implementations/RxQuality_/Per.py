from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ...Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Per:
	"""Per commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("per", core, parent)

	@property
	def rxPackets(self):
		"""rxPackets commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rxPackets'):
			from .Per_.RxPackets import RxPackets
			self._rxPackets = RxPackets(self._core, self._base)
		return self._rxPackets

	def fetch(self) -> float:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:RXQuality:PER \n
		Snippet: value: float = driver.rxQuality.per.fetch() \n
		Queries the PER results for the specified Tx level of R&S CMW. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: result: float Packet error rate"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:RXQuality:PER?', suppressed)
		return Conversions.str_to_float(response)

	def clone(self) -> 'Per':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Per(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
