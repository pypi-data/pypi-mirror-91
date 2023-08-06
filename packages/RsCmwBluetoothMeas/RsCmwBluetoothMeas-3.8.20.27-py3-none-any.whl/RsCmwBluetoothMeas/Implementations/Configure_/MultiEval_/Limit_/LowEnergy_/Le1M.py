from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le1M:
	"""Le1M commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le1M", core, parent)

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
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:SACP \n
		Snippet: value: SacpStruct = driver.configure.multiEval.limit.lowEnergy.le1M.get_sacp() \n
		These commands define and enable the 'Spectrum ACP' limits for BR (...:LIMit:SACP) , LE 1M PHY ( ...:LE1M...) , LE 2M PHY
		(...:LE2M...) , and LE coded PHY (...:LRANge...) , respectively. \n
			:return: structure: for return value, see the help for SacpStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:SACP?', self.__class__.SacpStruct())

	def set_sacp(self, value: SacpStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:SACP \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.le1M.set_sacp(value = SacpStruct()) \n
		These commands define and enable the 'Spectrum ACP' limits for BR (...:LIMit:SACP) , LE 1M PHY ( ...:LE1M...) , LE 2M PHY
		(...:LE2M...) , and LE coded PHY (...:LRANge...) , respectively. \n
			:param value: see the help for SacpStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:SACP', value)

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
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:PVTime \n
		Snippet: value: PowerVsTimeStruct = driver.configure.multiEval.limit.lowEnergy.le1M.get_power_vs_time() \n
		Defines the power limits: lower and upper average power limits, upper limit for 'peak minus average power', limit check
		enabling. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..
		) are available. \n
			:return: structure: for return value, see the help for PowerVsTimeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:PVTime?', self.__class__.PowerVsTimeStruct())

	def set_power_vs_time(self, value: PowerVsTimeStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:PVTime \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.le1M.set_power_vs_time(value = PowerVsTimeStruct()) \n
		Defines the power limits: lower and upper average power limits, upper limit for 'peak minus average power', limit check
		enabling. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..
		) are available. \n
			:param value: see the help for PowerVsTimeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:PVTime', value)

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
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:FACCuracy \n
		Snippet: value: FaccuracyStruct = driver.configure.multiEval.limit.lowEnergy.le1M.get_faccuracy() \n
		Defines the limit for the frequency accuracy. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE
		coded PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for FaccuracyStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:FACCuracy?', self.__class__.FaccuracyStruct())

	def set_faccuracy(self, value: FaccuracyStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:FACCuracy \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.le1M.set_faccuracy(value = FaccuracyStruct()) \n
		Defines the limit for the frequency accuracy. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE
		coded PHY (..:LRANge..) are available. \n
			:param value: see the help for FaccuracyStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:FACCuracy', value)

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
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:FOFFset \n
		Snippet: value: FreqOffsetStruct = driver.configure.multiEval.limit.lowEnergy.le1M.get_freq_offset() \n
		Sets/gets the frequency offset limit. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded
		PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for FreqOffsetStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:FOFFset?', self.__class__.FreqOffsetStruct())

	def set_freq_offset(self, value: FreqOffsetStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:FOFFset \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.le1M.set_freq_offset(value = FreqOffsetStruct()) \n
		Sets/gets the frequency offset limit. Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded
		PHY (..:LRANge..) are available. \n
			:param value: see the help for FreqOffsetStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:FOFFset', value)

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
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:MRATio \n
		Snippet: value: MratioStruct = driver.configure.multiEval.limit.lowEnergy.le1M.get_mratio() \n
		Sets or queries the modulation ratio limit Δf2 avg / Δf1 avg for LE 1M PHY (...:LE1M...) and LE 2M PHY (...:LE2M...) . \n
			:return: structure: for return value, see the help for MratioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:MRATio?', self.__class__.MratioStruct())

	def set_mratio(self, value: MratioStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:MRATio \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.le1M.set_mratio(value = MratioStruct()) \n
		Sets or queries the modulation ratio limit Δf2 avg / Δf1 avg for LE 1M PHY (...:LE1M...) and LE 2M PHY (...:LE2M...) . \n
			:param value: see the help for MratioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:MRATio', value)

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
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:FDRift \n
		Snippet: value: FdriftStruct = driver.configure.multiEval.limit.lowEnergy.le1M.get_fdrift() \n
		Sets and enables limits for frequency drift, maximum drift rate and initial frequency drift. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for FdriftStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:FDRift?', self.__class__.FdriftStruct())

	def set_fdrift(self, value: FdriftStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:FDRift \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.le1M.set_fdrift(value = FdriftStruct()) \n
		Sets and enables limits for frequency drift, maximum drift rate and initial frequency drift. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:param value: see the help for FdriftStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:FDRift', value)
