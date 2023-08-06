from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Brate:
	"""Brate commands group definition. 9 total commands, 1 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("brate", core, parent)

	@property
	def fdrift(self):
		"""fdrift commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fdrift'):
			from .Brate_.Fdrift import Fdrift
			self._fdrift = Fdrift(self._core, self._base)
		return self._fdrift

	# noinspection PyTypeChecker
	class PowerVsTimeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nom_Pow_Lower: float: numeric Range: -99.99 dBm to 99.99 dBm
			- Nom_Pow_Upper: float: numeric Range: -99.99 dBm to 99.99 dBm
			- Peak_Pow_Upper: float: numeric Range: -99.99 dBm to 99.99 dBm
			- Nom_Pow_Enabled: List[bool]: OFF | ON Disables or enables the limit check for the average power, 4 values, corresponding to the current, average, maximum and minimum results.
			- Peak_Pow_Enabled: List[bool]: OFF | ON Disables or enables the limit check for the peak power, 4 values, corresponding to the current, average, maximum and minimum results."""
		__meta_args_list = [
			ArgStruct.scalar_float('Nom_Pow_Lower'),
			ArgStruct.scalar_float('Nom_Pow_Upper'),
			ArgStruct.scalar_float('Peak_Pow_Upper'),
			ArgStruct('Nom_Pow_Enabled', DataType.BooleanList, None, False, False, 4),
			ArgStruct('Peak_Pow_Enabled', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nom_Pow_Lower: float = None
			self.Nom_Pow_Upper: float = None
			self.Peak_Pow_Upper: float = None
			self.Nom_Pow_Enabled: List[bool] = None
			self.Peak_Pow_Enabled: List[bool] = None

	def get_power_vs_time(self) -> PowerVsTimeStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:PVTime \n
		Snippet: value: PowerVsTimeStruct = driver.configure.multiEval.limit.brate.get_power_vs_time() \n
		Defines the power limits for BR: lower and upper average power limits, upper peak power limit, limit check enabling. \n
			:return: structure: for return value, see the help for PowerVsTimeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:PVTime?', self.__class__.PowerVsTimeStruct())

	def set_power_vs_time(self, value: PowerVsTimeStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:PVTime \n
		Snippet: driver.configure.multiEval.limit.brate.set_power_vs_time(value = PowerVsTimeStruct()) \n
		Defines the power limits for BR: lower and upper average power limits, upper peak power limit, limit check enabling. \n
			:param value: see the help for PowerVsTimeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:PVTime', value)

	# noinspection PyTypeChecker
	class MratioStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Mod_Ratio: float: numeric Range: 0 to 2
			- Mod_Ratio_Enabled: bool: OFF | ON Disable/enable limit checking"""
		__meta_args_list = [
			ArgStruct.scalar_float('Mod_Ratio'),
			ArgStruct.scalar_bool('Mod_Ratio_Enabled')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mod_Ratio: float = None
			self.Mod_Ratio_Enabled: bool = None

	def get_mratio(self) -> MratioStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:MRATio \n
		Snippet: value: MratioStruct = driver.configure.multiEval.limit.brate.get_mratio() \n
		Specifies the modulation ratio limit Δf2 avg / Δf1 avg for BR bursts. \n
			:return: structure: for return value, see the help for MratioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:MRATio?', self.__class__.MratioStruct())

	def set_mratio(self, value: MratioStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:MRATio \n
		Snippet: driver.configure.multiEval.limit.brate.set_mratio(value = MratioStruct()) \n
		Specifies the modulation ratio limit Δf2 avg / Δf1 avg for BR bursts. \n
			:param value: see the help for MratioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:MRATio', value)

	# noinspection PyTypeChecker
	class DeltaStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Delta_F_2_P_99_P_9: float: numeric Range: 100 kHz to 200 kHz
			- Delta_F_2_P_99_Enabl: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_float('Delta_F_2_P_99_P_9'),
			ArgStruct.scalar_bool('Delta_F_2_P_99_Enabl')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Delta_F_2_P_99_P_9: float = None
			self.Delta_F_2_P_99_Enabl: bool = None

	def get_delta(self) -> DeltaStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DELTa \n
		Snippet: value: DeltaStruct = driver.configure.multiEval.limit.brate.get_delta() \n
		Defines the lower limit for the frequency deviation Δf2 that must be exceeded by 99.9% of the measured bits. \n
			:return: structure: for return value, see the help for DeltaStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DELTa?', self.__class__.DeltaStruct())

	def set_delta(self, value: DeltaStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DELTa \n
		Snippet: driver.configure.multiEval.limit.brate.set_delta(value = DeltaStruct()) \n
		Defines the lower limit for the frequency deviation Δf2 that must be exceeded by 99.9% of the measured bits. \n
			:param value: see the help for DeltaStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DELTa', value)

	# noinspection PyTypeChecker
	class DaverageStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Freq_Dev_F_1_Lower: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_1_Upper: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_2_Lower: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_2_Upper: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_1_Enable: List[bool]: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)
			- Freq_Dev_F_2_Enable: List[bool]: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Dev_F_1_Lower'),
			ArgStruct.scalar_float('Freq_Dev_F_1_Upper'),
			ArgStruct.scalar_float('Freq_Dev_F_2_Lower'),
			ArgStruct.scalar_float('Freq_Dev_F_2_Upper'),
			ArgStruct('Freq_Dev_F_1_Enable', DataType.BooleanList, None, False, False, 4),
			ArgStruct('Freq_Dev_F_2_Enable', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Dev_F_1_Lower: float = None
			self.Freq_Dev_F_1_Upper: float = None
			self.Freq_Dev_F_2_Lower: float = None
			self.Freq_Dev_F_2_Upper: float = None
			self.Freq_Dev_F_1_Enable: List[bool] = None
			self.Freq_Dev_F_2_Enable: List[bool] = None

	def get_daverage(self) -> DaverageStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DAVerage \n
		Snippet: value: DaverageStruct = driver.configure.multiEval.limit.brate.get_daverage() \n
		Defines the lower and upper frequency deviation limits for BR bursts. The mnemonics DAVerage, DMAXimum, DMINimum
		distinguish average, maximum, and minimum frequency deviations. \n
			:return: structure: for return value, see the help for DaverageStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DAVerage?', self.__class__.DaverageStruct())

	def set_daverage(self, value: DaverageStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DAVerage \n
		Snippet: driver.configure.multiEval.limit.brate.set_daverage(value = DaverageStruct()) \n
		Defines the lower and upper frequency deviation limits for BR bursts. The mnemonics DAVerage, DMAXimum, DMINimum
		distinguish average, maximum, and minimum frequency deviations. \n
			:param value: see the help for DaverageStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DAVerage', value)

	# noinspection PyTypeChecker
	class DminimumStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Freq_Dev_F_1_Lower: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_1_Upper: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_2_Lower: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_2_Upper: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_1_Enable: List[bool]: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)
			- Freq_Dev_F_2_Enable: List[bool]: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Dev_F_1_Lower'),
			ArgStruct.scalar_float('Freq_Dev_F_1_Upper'),
			ArgStruct.scalar_float('Freq_Dev_F_2_Lower'),
			ArgStruct.scalar_float('Freq_Dev_F_2_Upper'),
			ArgStruct('Freq_Dev_F_1_Enable', DataType.BooleanList, None, False, False, 4),
			ArgStruct('Freq_Dev_F_2_Enable', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Dev_F_1_Lower: float = None
			self.Freq_Dev_F_1_Upper: float = None
			self.Freq_Dev_F_2_Lower: float = None
			self.Freq_Dev_F_2_Upper: float = None
			self.Freq_Dev_F_1_Enable: List[bool] = None
			self.Freq_Dev_F_2_Enable: List[bool] = None

	def get_dminimum(self) -> DminimumStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DMINimum \n
		Snippet: value: DminimumStruct = driver.configure.multiEval.limit.brate.get_dminimum() \n
		Defines the lower and upper frequency deviation limits for BR bursts. The mnemonics DAVerage, DMAXimum, DMINimum
		distinguish average, maximum, and minimum frequency deviations. \n
			:return: structure: for return value, see the help for DminimumStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DMINimum?', self.__class__.DminimumStruct())

	def set_dminimum(self, value: DminimumStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DMINimum \n
		Snippet: driver.configure.multiEval.limit.brate.set_dminimum(value = DminimumStruct()) \n
		Defines the lower and upper frequency deviation limits for BR bursts. The mnemonics DAVerage, DMAXimum, DMINimum
		distinguish average, maximum, and minimum frequency deviations. \n
			:param value: see the help for DminimumStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DMINimum', value)

	# noinspection PyTypeChecker
	class DmaximumStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Freq_Dev_F_1_Lower: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_1_Upper: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_2_Lower: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_2_Upper: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Dev_F_1_Enable: List[bool]: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)
			- Freq_Dev_F_2_Enable: List[bool]: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Dev_F_1_Lower'),
			ArgStruct.scalar_float('Freq_Dev_F_1_Upper'),
			ArgStruct.scalar_float('Freq_Dev_F_2_Lower'),
			ArgStruct.scalar_float('Freq_Dev_F_2_Upper'),
			ArgStruct('Freq_Dev_F_1_Enable', DataType.BooleanList, None, False, False, 4),
			ArgStruct('Freq_Dev_F_2_Enable', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Dev_F_1_Lower: float = None
			self.Freq_Dev_F_1_Upper: float = None
			self.Freq_Dev_F_2_Lower: float = None
			self.Freq_Dev_F_2_Upper: float = None
			self.Freq_Dev_F_1_Enable: List[bool] = None
			self.Freq_Dev_F_2_Enable: List[bool] = None

	def get_dmaximum(self) -> DmaximumStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DMAXimum \n
		Snippet: value: DmaximumStruct = driver.configure.multiEval.limit.brate.get_dmaximum() \n
		Defines the lower and upper frequency deviation limits for BR bursts. The mnemonics DAVerage, DMAXimum, DMINimum
		distinguish average, maximum, and minimum frequency deviations. \n
			:return: structure: for return value, see the help for DmaximumStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DMAXimum?', self.__class__.DmaximumStruct())

	def set_dmaximum(self, value: DmaximumStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DMAXimum \n
		Snippet: driver.configure.multiEval.limit.brate.set_dmaximum(value = DmaximumStruct()) \n
		Defines the lower and upper frequency deviation limits for BR bursts. The mnemonics DAVerage, DMAXimum, DMINimum
		distinguish average, maximum, and minimum frequency deviations. \n
			:param value: see the help for DmaximumStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DMAXimum', value)

	# noinspection PyTypeChecker
	class FaccuracyStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Freq_Accuracy: float: numeric Range: 0 Hz to 250 kHz
			- Freq_Acc_Enabled: List[bool]: OFF | ON Disable or enable limit check for current, average, and maximum results (3 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Accuracy'),
			ArgStruct('Freq_Acc_Enabled', DataType.BooleanList, None, False, False, 3)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Accuracy: float = None
			self.Freq_Acc_Enabled: List[bool] = None

	def get_faccuracy(self) -> FaccuracyStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FACCuracy \n
		Snippet: value: FaccuracyStruct = driver.configure.multiEval.limit.brate.get_faccuracy() \n
		Defines the limit for the frequency accuracy. \n
			:return: structure: for return value, see the help for FaccuracyStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FACCuracy?', self.__class__.FaccuracyStruct())

	def set_faccuracy(self, value: FaccuracyStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FACCuracy \n
		Snippet: driver.configure.multiEval.limit.brate.set_faccuracy(value = FaccuracyStruct()) \n
		Defines the limit for the frequency accuracy. \n
			:param value: see the help for FaccuracyStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FACCuracy', value)

	def clone(self) -> 'Brate':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Brate(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
