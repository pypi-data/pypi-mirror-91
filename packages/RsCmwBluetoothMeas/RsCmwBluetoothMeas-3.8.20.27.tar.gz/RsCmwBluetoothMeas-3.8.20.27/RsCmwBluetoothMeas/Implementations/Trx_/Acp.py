from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Acp:
	"""Acp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("acp", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Nominal_Power: float: float Average power during the carrier-on state Unit: dBm
			- No_Of_Exceptions: int: decimal Number of exceptions (channels ±3, ±4 ... with an ACP above the 'Exception PTx' threshold )"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_int('No_Of_Exceptions')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nominal_Power: float = None
			self.No_Of_Exceptions: int = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:TRX:ACP \n
		Snippet: value: FetchStruct = driver.trx.acp.fetch() \n
		Returns the 'Spectrum ACP' results for Tx-Rx tests on advertiser packets (LE 1M PHY) . Only 'ACP+/-5 channel' mode is
		supported (21 half-channels) . See also 'LE: Spectrum ACP Results '. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:TRX:ACP?', self.__class__.FetchStruct())
