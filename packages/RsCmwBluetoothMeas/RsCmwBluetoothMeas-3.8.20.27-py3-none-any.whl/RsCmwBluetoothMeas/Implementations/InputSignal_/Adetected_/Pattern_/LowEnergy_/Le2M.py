from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2M:
	"""Le2M commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le2M", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> enums.DetectedPatternType:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:ISIGnal:ADETected:PATTern:LENergy:LE2M \n
		Snippet: value: enums.DetectedPatternType = driver.inputSignal.adetected.pattern.lowEnergy.le2M.fetch() \n
		Returns the detected payload pattern type. Commands for LE 1M PHY (...:LE1M...) and LE 2M PHY (...:LE2M...) are available.
		A result is available after the R&S CMW has auto-detected a packet (method RsCmwBluetoothMeas.Configure.InputSignal.dmode
		AUTO) . \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: pattern_type: P44 | P11 | OTHer | ALTernating P11: 10101010 P44: 11110000 OTHer: any pattern except P11, P44 ALTernating: the periodical change of the pattern P11 and P44"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:ISIGnal:ADETected:PATTern:LENergy:LE2M?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.DetectedPatternType)
