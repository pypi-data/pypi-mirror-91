from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmaximum:
	"""Dmaximum commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmaximum", core, parent)

	# noinspection PyTypeChecker
	class Df2SStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Freq_Dev_F_2_Lower: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_2_Upper: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_2_Enable: List[bool]: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Dev_F_2_Lower'),
			ArgStruct.scalar_float('Freq_Dev_F_2_Upper'),
			ArgStruct('Freq_Dev_F_2_Enable', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Dev_F_2_Lower: float = None
			self.Freq_Dev_F_2_Upper: float = None
			self.Freq_Dev_F_2_Enable: List[bool] = None

	def get_df_2_s(self) -> Df2SStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum:DF2S \n
		Snippet: value: Df2SStruct = driver.configure.multiEval.limit.lowEnergy.dmaximum.get_df_2_s() \n
		Defines the lower and upper Δf2 frequency deviation limits for uncoded LE 1M PHY. The mnemonics DAVerage, DMINimum,
		DMAXimum distinguish average, minimum and maximum frequency deviations. \n
			:return: structure: for return value, see the help for Df2SStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum:DF2S?', self.__class__.Df2SStruct())

	def set_df_2_s(self, value: Df2SStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum:DF2S \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.dmaximum.set_df_2_s(value = Df2SStruct()) \n
		Defines the lower and upper Δf2 frequency deviation limits for uncoded LE 1M PHY. The mnemonics DAVerage, DMINimum,
		DMAXimum distinguish average, minimum and maximum frequency deviations. \n
			:param value: see the help for Df2SStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum:DF2S', value)

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Freq_Dev_F_1_Lower: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_1_Upper: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_1_Enable: List[bool]: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Dev_F_1_Lower'),
			ArgStruct.scalar_float('Freq_Dev_F_1_Upper'),
			ArgStruct('Freq_Dev_F_1_Enable', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Dev_F_1_Lower: float = None
			self.Freq_Dev_F_1_Upper: float = None
			self.Freq_Dev_F_1_Enable: List[bool] = None

	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum \n
		Snippet: value: ValueStruct = driver.configure.multiEval.limit.lowEnergy.dmaximum.get_value() \n
		Defines the lower and upper Δf1 frequency deviation limits for LE 1M PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.dmaximum.set_value(value = ValueStruct()) \n
		Defines the lower and upper Δf1 frequency deviation limits for LE 1M PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum', value)
