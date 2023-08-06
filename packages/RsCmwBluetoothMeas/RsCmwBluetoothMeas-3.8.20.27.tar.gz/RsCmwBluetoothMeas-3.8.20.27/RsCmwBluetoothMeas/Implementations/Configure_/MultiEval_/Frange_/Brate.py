from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Brate:
	"""Brate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("brate", core, parent)

	# noinspection PyTypeChecker
	class MeasurementStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Left_Channel: int: numeric Left adjacent channel relative to the EUT center TX channel Range: 1 to 5
			- Right_Channel: int: numeric Right adjacent channel relative to the EUT center TX channel Range: 1 to 5
			- Threshold: float: numeric Threshold for the spectral power density drop to search the frequencies fL and fH Specification defines - 80 dBm/Hz for equivalent isotropically radiated power or - 30 dBm if measured in a 100 kHz bandwidth. Range: -80 dBm to 40 dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Left_Channel'),
			ArgStruct.scalar_int('Right_Channel'),
			ArgStruct.scalar_float('Threshold')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left_Channel: int = None
			self.Right_Channel: int = None
			self.Threshold: float = None

	def get_measurement(self) -> MeasurementStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:FRANge:BRATe:MEASurement \n
		Snippet: value: MeasurementStruct = driver.configure.multiEval.frange.brate.get_measurement() \n
		Specifies the number of 1 MHz channels to be measured below and above the current measured channel. The threshold is the
		level that needs to be crossed to search the frequencies fL and fH. \n
			:return: structure: for return value, see the help for MeasurementStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:FRANge:BRATe:MEASurement?', self.__class__.MeasurementStruct())

	def set_measurement(self, value: MeasurementStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:FRANge:BRATe:MEASurement \n
		Snippet: driver.configure.multiEval.frange.brate.set_measurement(value = MeasurementStruct()) \n
		Specifies the number of 1 MHz channels to be measured below and above the current measured channel. The threshold is the
		level that needs to be crossed to search the frequencies fL and fH. \n
			:param value: see the help for MeasurementStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:FRANge:BRATe:MEASurement', value)
