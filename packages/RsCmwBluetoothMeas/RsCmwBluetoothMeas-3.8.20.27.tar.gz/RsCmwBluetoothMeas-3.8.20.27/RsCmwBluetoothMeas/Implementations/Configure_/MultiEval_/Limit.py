from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 61 total commands, 4 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("limit", core, parent)

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Limit_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	@property
	def cte(self):
		"""cte commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cte'):
			from .Limit_.Cte import Cte
			self._cte = Cte(self._core, self._base)
		return self._cte

	@property
	def edrate(self):
		"""edrate commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_edrate'):
			from .Limit_.Edrate import Edrate
			self._edrate = Edrate(self._core, self._base)
		return self._edrate

	@property
	def brate(self):
		"""brate commands group. 1 Sub-classes, 7 commands."""
		if not hasattr(self, '_brate'):
			from .Limit_.Brate import Brate
			self._brate = Brate(self._core, self._base)
		return self._brate

	# noinspection PyTypeChecker
	class FrangeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Flx_Lower: float: numeric Lower limit for the lowest frequency fL relative to center frequency Range: -5 MHz to 0 MHz, Unit: Hz
			- Fhx_Upper: float: numeric Upper limit for the highest frequency fH relative to center frequency Range: 0 MHz to 5 MHz, Unit: Hz
			- Flx_Lower_Enable: bool: OFF | ON Disable or enable limit check for the lowest frequency fL
			- Fhx_Upper_Enable: bool: OFF | ON Disable or enable limit check for the highest frequency fH"""
		__meta_args_list = [
			ArgStruct.scalar_float('Flx_Lower'),
			ArgStruct.scalar_float('Fhx_Upper'),
			ArgStruct.scalar_bool('Flx_Lower_Enable'),
			ArgStruct.scalar_bool('Fhx_Upper_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Flx_Lower: float = None
			self.Fhx_Upper: float = None
			self.Flx_Lower_Enable: bool = None
			self.Fhx_Upper_Enable: bool = None

	def get_frange(self) -> FrangeStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:FRANge \n
		Snippet: value: FrangeStruct = driver.configure.multiEval.limit.get_frange() \n
		Defines the limit for the frequency range measurement. \n
			:return: structure: for return value, see the help for FrangeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:FRANge?', self.__class__.FrangeStruct())

	def set_frange(self, value: FrangeStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:FRANge \n
		Snippet: driver.configure.multiEval.limit.set_frange(value = FrangeStruct()) \n
		Defines the limit for the frequency range measurement. \n
			:param value: see the help for FrangeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:FRANge', value)

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
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SACP \n
		Snippet: value: SacpStruct = driver.configure.multiEval.limit.get_sacp() \n
		These commands define and enable the 'Spectrum ACP' limits for BR (...:LIMit:SACP) , LE 1M PHY ( ...:LE1M...) , LE 2M PHY
		(...:LE2M...) , and LE coded PHY (...:LRANge...) , respectively. \n
			:return: structure: for return value, see the help for SacpStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SACP?', self.__class__.SacpStruct())

	def set_sacp(self, value: SacpStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SACP \n
		Snippet: driver.configure.multiEval.limit.set_sacp(value = SacpStruct()) \n
		These commands define and enable the 'Spectrum ACP' limits for BR (...:LIMit:SACP) , LE 1M PHY ( ...:LE1M...) , LE 2M PHY
		(...:LE2M...) , and LE coded PHY (...:LRANge...) , respectively. \n
			:param value: see the help for SacpStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SACP', value)

	# noinspection PyTypeChecker
	class SoBwStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Limit_Threshold: float: numeric Threshold value for 'high' vs 'low' peak emission bursts Range: -80 dBm to 40 dBm
			- Eq_High_Peak_Upper: float: numeric 20 dB bandwidth limit for 'high' peak emission bursts (≥LimitThreshold) Range: 1E-3 MHz to 4 MHz
			- Low_Peak_Upper: float: numeric 20 dB bandwidth limit for 'low' peak emission bursts ( LimitThreshold) Range: 1E-3 MHz to 4 MHz
			- Eq_High_Peak_Enab: bool: OFF | ON Disable or enable the 20 dB bandwidth limit for 'high' peak emission bursts
			- Low_Peak_Enab: bool: OFF | ON Disable or enable the 20 dB bandwidth limit for 'low' peak emission bursts"""
		__meta_args_list = [
			ArgStruct.scalar_float('Limit_Threshold'),
			ArgStruct.scalar_float('Eq_High_Peak_Upper'),
			ArgStruct.scalar_float('Low_Peak_Upper'),
			ArgStruct.scalar_bool('Eq_High_Peak_Enab'),
			ArgStruct.scalar_bool('Low_Peak_Enab')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit_Threshold: float = None
			self.Eq_High_Peak_Upper: float = None
			self.Low_Peak_Upper: float = None
			self.Eq_High_Peak_Enab: bool = None
			self.Low_Peak_Enab: bool = None

	def get_so_bw(self) -> SoBwStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SOBW \n
		Snippet: value: SoBwStruct = driver.configure.multiEval.limit.get_so_bw() \n
		Defines and enables the limits for the 20 dB bandwidth measurement (BR only) . \n
			:return: structure: for return value, see the help for SoBwStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SOBW?', self.__class__.SoBwStruct())

	def set_so_bw(self, value: SoBwStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SOBW \n
		Snippet: driver.configure.multiEval.limit.set_so_bw(value = SoBwStruct()) \n
		Defines and enables the limits for the 20 dB bandwidth measurement (BR only) . \n
			:param value: see the help for SoBwStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SOBW', value)

	# noinspection PyTypeChecker
	class SgacpStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ptx_Limit: float: numeric Range: -80 dBm to -10 dBm
			- Exc_Ptx_Limit: float: numeric Range: -80 dBm to -10 dBm
			- No_Of_Ex_Limit: int: numeric Range: 0 to 16
			- Ptxm_26_N_1_Rel_Lim: float: numeric Range: -80 dB to 0 dB
			- Ptxm_26_P_1_Rel_Lim: float: numeric Range: -80 dB to 0 dB
			- Ptx_Enable: bool: OFF | ON
			- No_Of_Exc_Enable: bool: OFF | ON
			- Ptxm_26_N_1_Rel_Enab: bool: OFF | ON
			- Ptxm_26_P_1_Rel_Enab: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ptx_Limit'),
			ArgStruct.scalar_float('Exc_Ptx_Limit'),
			ArgStruct.scalar_int('No_Of_Ex_Limit'),
			ArgStruct.scalar_float('Ptxm_26_N_1_Rel_Lim'),
			ArgStruct.scalar_float('Ptxm_26_P_1_Rel_Lim'),
			ArgStruct.scalar_bool('Ptx_Enable'),
			ArgStruct.scalar_bool('No_Of_Exc_Enable'),
			ArgStruct.scalar_bool('Ptxm_26_N_1_Rel_Enab'),
			ArgStruct.scalar_bool('Ptxm_26_P_1_Rel_Enab')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ptx_Limit: float = None
			self.Exc_Ptx_Limit: float = None
			self.No_Of_Ex_Limit: int = None
			self.Ptxm_26_N_1_Rel_Lim: float = None
			self.Ptxm_26_P_1_Rel_Lim: float = None
			self.Ptx_Enable: bool = None
			self.No_Of_Exc_Enable: bool = None
			self.Ptxm_26_N_1_Rel_Enab: bool = None
			self.Ptxm_26_P_1_Rel_Enab: bool = None

	def get_sgacp(self) -> SgacpStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SGACp \n
		Snippet: value: SgacpStruct = driver.configure.multiEval.limit.get_sgacp() \n
		Defines and enables the upper limits for the 'Spectrum Gated ACP' measurement for EDR packets: 'PTx', 'Exceptions PTx',
		'No. of Exceptions', PTx–26 dB–1 (rel) , PTx–26 dB +1 (rel) , and limit check enabling. \n
			:return: structure: for return value, see the help for SgacpStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SGACp?', self.__class__.SgacpStruct())

	def set_sgacp(self, value: SgacpStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SGACp \n
		Snippet: driver.configure.multiEval.limit.set_sgacp(value = SgacpStruct()) \n
		Defines and enables the upper limits for the 'Spectrum Gated ACP' measurement for EDR packets: 'PTx', 'Exceptions PTx',
		'No. of Exceptions', PTx–26 dB–1 (rel) , PTx–26 dB +1 (rel) , and limit check enabling. \n
			:param value: see the help for SgacpStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:SGACp', value)

	# noinspection PyTypeChecker
	class PowerVsTimeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pack_Time_Lower: float: numeric Range: -15 µs to 15 µs
			- Pack_Time_Upper: float: numeric Range: -15 µs to 15 µs
			- Pack_Time_Enable: List[bool]: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_float('Pack_Time_Lower'),
			ArgStruct.scalar_float('Pack_Time_Upper'),
			ArgStruct('Pack_Time_Enable', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pack_Time_Lower: float = None
			self.Pack_Time_Upper: float = None
			self.Pack_Time_Enable: List[bool] = None

	def get_power_vs_time(self) -> PowerVsTimeStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:PVTime \n
		Snippet: value: PowerVsTimeStruct = driver.configure.multiEval.limit.get_power_vs_time() \n
		Sets and enables/disables a lower and upper timing error limit for PVT measurements. \n
			:return: structure: for return value, see the help for PowerVsTimeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:PVTime?', self.__class__.PowerVsTimeStruct())

	def set_power_vs_time(self, value: PowerVsTimeStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:PVTime \n
		Snippet: driver.configure.multiEval.limit.set_power_vs_time(value = PowerVsTimeStruct()) \n
		Sets and enables/disables a lower and upper timing error limit for PVT measurements. \n
			:param value: see the help for PowerVsTimeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:PVTime', value)

	def clone(self) -> 'Limit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Limit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
