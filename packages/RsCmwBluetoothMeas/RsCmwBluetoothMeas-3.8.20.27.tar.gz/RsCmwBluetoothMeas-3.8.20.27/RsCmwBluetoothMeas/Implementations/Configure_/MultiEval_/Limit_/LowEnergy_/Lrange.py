from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lrange:
	"""Lrange commands group definition. 9 total commands, 0 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lrange", core, parent)

	# noinspection PyTypeChecker
	class SacpStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ptx_Limit: float: numeric Power limit for 1 MHz channels fTX± 2 MHz Range: -80 dBm to -10 dBm
			- Exc_Ptx_Limit: float: numeric Power limit for 1 MHz channels fTX±3 MHz, fTX±4 MHz, ... Range: -80 dBm to -10 dBm
			- No_Of_Ex_Limit: int: numeric Maximum number of tolerable exceptions, i.e. 1 MHz channels fTX±3 MHz, fTX±4 MHz, ... whose power is above ExcPTxLimit, but below PTxLimit Range: 0 to 16
			- Ptx_Enable: bool: OFF | ON Disables | enables the PTxLimit limit for 1 MHz channels fTX± 2 MHz
			- No_Of_Exc_Enable: bool: OFF | ON Disables | enables the ExcPTxLimit limit for 1 MHz channels fTX±3 MHz, fTX±4 MHz, ... with NoOfExLimit tolerable exceptions (per statistic cycle) ."""
		__meta_args_list = [
			ArgStruct.scalar_float('Ptx_Limit'),
			ArgStruct.scalar_float('Exc_Ptx_Limit'),
			ArgStruct.scalar_int('No_Of_Ex_Limit'),
			ArgStruct.scalar_bool('Ptx_Enable'),
			ArgStruct.scalar_bool('No_Of_Exc_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ptx_Limit: float = None
			self.Exc_Ptx_Limit: float = None
			self.No_Of_Ex_Limit: int = None
			self.Ptx_Enable: bool = None
			self.No_Of_Exc_Enable: bool = None

	def get_sacp(self) -> SacpStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:SACP \n
		Snippet: value: SacpStruct = driver.configure.multiEval.limit.lowEnergy.lrange.get_sacp() \n
		These commands define and enable the 'Spectrum ACP' limits for BR (...:LIMit:SACP) , LE 1M PHY ( ...:LE1M...) , LE 2M PHY
		(...:LE2M...) , and LE coded PHY (...:LRANge...) , respectively. \n
			:return: structure: for return value, see the help for SacpStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:SACP?', self.__class__.SacpStruct())

	def set_sacp(self, value: SacpStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:SACP \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.set_sacp(value = SacpStruct()) \n
		These commands define and enable the 'Spectrum ACP' limits for BR (...:LIMit:SACP) , LE 1M PHY ( ...:LE1M...) , LE 2M PHY
		(...:LE2M...) , and LE coded PHY (...:LRANge...) , respectively. \n
			:param value: see the help for SacpStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:SACP', value)

	# noinspection PyTypeChecker
	class PowerVsTimeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Avg_Pow_Lower: float: numeric Range: -99.99 dBm to 99.99 dBm
			- Avg_Pow_Upper: float: numeric Range: -99.99 dBm to 99.99 dBm
			- Pkm_Avg_Pow_Upper: float: numeric Range: -99.99 dBm to 99.99 dBm
			- Avg_Pow_Enabled: List[bool]: OFF | ON Disables or enables the limit check for the average power, 4 values, corresponding to the current, average, maximum and minimum results.
			- Pkm_Avg_Pow_Enable: List[bool]: OFF | ON Disables or enables the limit check for the 'peak minus average power', 4 values, corresponding to the current, average, maximum and minimum results."""
		__meta_args_list = [
			ArgStruct.scalar_float('Avg_Pow_Lower'),
			ArgStruct.scalar_float('Avg_Pow_Upper'),
			ArgStruct.scalar_float('Pkm_Avg_Pow_Upper'),
			ArgStruct('Avg_Pow_Enabled', DataType.BooleanList, None, False, False, 4),
			ArgStruct('Pkm_Avg_Pow_Enable', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Avg_Pow_Lower: float = None
			self.Avg_Pow_Upper: float = None
			self.Pkm_Avg_Pow_Upper: float = None
			self.Avg_Pow_Enabled: List[bool] = None
			self.Pkm_Avg_Pow_Enable: List[bool] = None

	def get_power_vs_time(self) -> PowerVsTimeStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:PVTime \n
		Snippet: value: PowerVsTimeStruct = driver.configure.multiEval.limit.lowEnergy.lrange.get_power_vs_time() \n
		Defines the power limits: lower and upper average power limits, upper limit for 'peak minus average power', limit check
		enabling. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..
		) are available. \n
			:return: structure: for return value, see the help for PowerVsTimeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:PVTime?', self.__class__.PowerVsTimeStruct())

	def set_power_vs_time(self, value: PowerVsTimeStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:PVTime \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.set_power_vs_time(value = PowerVsTimeStruct()) \n
		Defines the power limits: lower and upper average power limits, upper limit for 'peak minus average power', limit check
		enabling. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..
		) are available. \n
			:param value: see the help for PowerVsTimeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:PVTime', value)

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
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FACCuracy \n
		Snippet: value: FaccuracyStruct = driver.configure.multiEval.limit.lowEnergy.lrange.get_faccuracy() \n
		Defines the limit for the frequency accuracy. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE
		coded PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for FaccuracyStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FACCuracy?', self.__class__.FaccuracyStruct())

	def set_faccuracy(self, value: FaccuracyStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FACCuracy \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.set_faccuracy(value = FaccuracyStruct()) \n
		Defines the limit for the frequency accuracy. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE
		coded PHY (..:LRANge..) are available. \n
			:param value: see the help for FaccuracyStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FACCuracy', value)

	# noinspection PyTypeChecker
	class FreqOffsetStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Freq_Offset: float: numeric Range: 0 Hz to 250 kHz
			- Freq_Offset_Enab: List[bool]: OFF | ON Disable or enable limit checking for current, average, and maximum results (3 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Offset'),
			ArgStruct('Freq_Offset_Enab', DataType.BooleanList, None, False, False, 3)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Offset: float = None
			self.Freq_Offset_Enab: List[bool] = None

	def get_freq_offset(self) -> FreqOffsetStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FOFFset \n
		Snippet: value: FreqOffsetStruct = driver.configure.multiEval.limit.lowEnergy.lrange.get_freq_offset() \n
		Sets/gets the frequency offset limit. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded
		PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for FreqOffsetStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FOFFset?', self.__class__.FreqOffsetStruct())

	def set_freq_offset(self, value: FreqOffsetStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FOFFset \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.set_freq_offset(value = FreqOffsetStruct()) \n
		Sets/gets the frequency offset limit. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded
		PHY (..:LRANge..) are available. \n
			:param value: see the help for FreqOffsetStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FOFFset', value)

	# noinspection PyTypeChecker
	class DeltaStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Delta_F_1_P_99_P_9: float: numeric Range: 150 kHz to 250 kHz
			- Delta_F_1_P_99_Enabl: bool: OFF | ON Disable/enable limit checking"""
		__meta_args_list = [
			ArgStruct.scalar_float('Delta_F_1_P_99_P_9'),
			ArgStruct.scalar_bool('Delta_F_1_P_99_Enabl')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Delta_F_1_P_99_P_9: float = None
			self.Delta_F_1_P_99_Enabl: bool = None

	def get_delta(self) -> DeltaStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DELTa \n
		Snippet: value: DeltaStruct = driver.configure.multiEval.limit.lowEnergy.lrange.get_delta() \n
		Sets/gets the limit for the frequency deviation Δf1 that must be exceeded by 99.9% of the measured samples for LE coded
		PHY. \n
			:return: structure: for return value, see the help for DeltaStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DELTa?', self.__class__.DeltaStruct())

	def set_delta(self, value: DeltaStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DELTa \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.set_delta(value = DeltaStruct()) \n
		Sets/gets the limit for the frequency deviation Δf1 that must be exceeded by 99.9% of the measured samples for LE coded
		PHY. \n
			:param value: see the help for DeltaStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DELTa', value)

	# noinspection PyTypeChecker
	class FdriftStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Frequency_Drift: float: numeric Range: 0 Hz to 250 kHz
			- Max_Drift_Rate: float: numeric Range: 0 Hz to 250 kHz
			- Initl_Freq_Drift: float: numeric Range: 0 Hz to 250 kHz
			- Freq_Drift_Enable: List[bool]: OFF | ON Disable or enable limit checking for current, average, and maximum results (3 values) .
			- Max_Drift_Rate_Enb: List[bool]: OFF | ON Disable or enable limit checking for current, average, and maximum results (3 values) .
			- Init_Freq_Drift_En: List[bool]: OFF | ON Disable or enable limit checking for current, average, and maximum results (3 values) ."""
		__meta_args_list = [
			ArgStruct.scalar_float('Frequency_Drift'),
			ArgStruct.scalar_float('Max_Drift_Rate'),
			ArgStruct.scalar_float('Initl_Freq_Drift'),
			ArgStruct('Freq_Drift_Enable', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Max_Drift_Rate_Enb', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Init_Freq_Drift_En', DataType.BooleanList, None, False, False, 3)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Frequency_Drift: float = None
			self.Max_Drift_Rate: float = None
			self.Initl_Freq_Drift: float = None
			self.Freq_Drift_Enable: List[bool] = None
			self.Max_Drift_Rate_Enb: List[bool] = None
			self.Init_Freq_Drift_En: List[bool] = None

	def get_fdrift(self) -> FdriftStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FDRift \n
		Snippet: value: FdriftStruct = driver.configure.multiEval.limit.lowEnergy.lrange.get_fdrift() \n
		Sets and enables limits for frequency drift, maximum drift rate and initial frequency drift. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for FdriftStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FDRift?', self.__class__.FdriftStruct())

	def set_fdrift(self, value: FdriftStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FDRift \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.set_fdrift(value = FdriftStruct()) \n
		Sets and enables limits for frequency drift, maximum drift rate and initial frequency drift. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:param value: see the help for FdriftStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:FDRift', value)

	# noinspection PyTypeChecker
	class DaverageStruct(StructBase):
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

	def get_daverage(self) -> DaverageStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DAVerage \n
		Snippet: value: DaverageStruct = driver.configure.multiEval.limit.lowEnergy.lrange.get_daverage() \n
		Defines the lower and upper Δf1 frequency deviation limits for LE coded PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:return: structure: for return value, see the help for DaverageStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DAVerage?', self.__class__.DaverageStruct())

	def set_daverage(self, value: DaverageStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DAVerage \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.set_daverage(value = DaverageStruct()) \n
		Defines the lower and upper Δf1 frequency deviation limits for LE coded PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:param value: see the help for DaverageStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DAVerage', value)

	# noinspection PyTypeChecker
	class DminimumStruct(StructBase):
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

	def get_dminimum(self) -> DminimumStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DMINimum \n
		Snippet: value: DminimumStruct = driver.configure.multiEval.limit.lowEnergy.lrange.get_dminimum() \n
		Defines the lower and upper Δf1 frequency deviation limits for LE coded PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:return: structure: for return value, see the help for DminimumStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DMINimum?', self.__class__.DminimumStruct())

	def set_dminimum(self, value: DminimumStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DMINimum \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.set_dminimum(value = DminimumStruct()) \n
		Defines the lower and upper Δf1 frequency deviation limits for LE coded PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:param value: see the help for DminimumStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DMINimum', value)

	# noinspection PyTypeChecker
	class DmaximumStruct(StructBase):
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

	def get_dmaximum(self) -> DmaximumStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DMAXimum \n
		Snippet: value: DmaximumStruct = driver.configure.multiEval.limit.lowEnergy.lrange.get_dmaximum() \n
		Defines the lower and upper Δf1 frequency deviation limits for LE coded PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:return: structure: for return value, see the help for DmaximumStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DMAXimum?', self.__class__.DmaximumStruct())

	def set_dmaximum(self, value: DmaximumStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DMAXimum \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.set_dmaximum(value = DmaximumStruct()) \n
		Defines the lower and upper Δf1 frequency deviation limits for LE coded PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:param value: see the help for DmaximumStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DMAXimum', value)
