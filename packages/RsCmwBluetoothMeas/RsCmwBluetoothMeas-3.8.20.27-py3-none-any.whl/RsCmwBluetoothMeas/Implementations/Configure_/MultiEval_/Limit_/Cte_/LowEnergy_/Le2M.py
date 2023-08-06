from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2M:
	"""Le2M commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le2M", core, parent)

	# noinspection PyTypeChecker
	class PdeviationStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ref_Dev: float: numeric Upper CTE power limit for reference antenna. Range: 0.01 to 1
			- Tx_Dev: float: numeric Upper limit for power deviation in a slot. Range: 0.01 to 1
			- Ref_Dev_Enable: bool: OFF | ON Enables/disables the CTE power limit check for reference antenna.
			- Tx_Dev_Enable: bool: OFF | ON Enables/disables the limit check for power deviation in a slot."""
		__meta_args_list = [
			ArgStruct.scalar_float('Ref_Dev'),
			ArgStruct.scalar_float('Tx_Dev'),
			ArgStruct.scalar_bool('Ref_Dev_Enable'),
			ArgStruct.scalar_bool('Tx_Dev_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ref_Dev: float = None
			self.Tx_Dev: float = None
			self.Ref_Dev_Enable: bool = None
			self.Tx_Dev_Enable: bool = None

	def get_pdeviation(self) -> PdeviationStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:PDEViation \n
		Snippet: value: PdeviationStruct = driver.configure.multiEval.limit.cte.lowEnergy.le2M.get_pdeviation() \n
		Defines the upper CTE power limits and enables/disables the limit check. Commands for uncoded LE 1M PHY (..:LE1M..) and
		LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for PdeviationStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:PDEViation?', self.__class__.PdeviationStruct())

	def set_pdeviation(self, value: PdeviationStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:PDEViation \n
		Snippet: driver.configure.multiEval.limit.cte.lowEnergy.le2M.set_pdeviation(value = PdeviationStruct()) \n
		Defines the upper CTE power limits and enables/disables the limit check. Commands for uncoded LE 1M PHY (..:LE1M..) and
		LE 2M PHY (..:LE2M..) are available. \n
			:param value: see the help for PdeviationStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:PDEViation', value)

	# noinspection PyTypeChecker
	class FdriftStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Frequency_Drift: float: numeric Range: 0 Hz to 500 kHz
			- Max_Drift_Rate: float: numeric Range: 0 Hz to 500 kHz
			- Initl_Freq_Drift: float: numeric Range: 0 Hz to 500 kHz
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
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:FDRift \n
		Snippet: value: FdriftStruct = driver.configure.multiEval.limit.cte.lowEnergy.le2M.get_fdrift() \n
		Sets and enables limits for frequency drift, maximum drift rate and initial frequency drift for the CTE portion. Commands
		for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for FdriftStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:FDRift?', self.__class__.FdriftStruct())

	def set_fdrift(self, value: FdriftStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:FDRift \n
		Snippet: driver.configure.multiEval.limit.cte.lowEnergy.le2M.set_fdrift(value = FdriftStruct()) \n
		Sets and enables limits for frequency drift, maximum drift rate and initial frequency drift for the CTE portion. Commands
		for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param value: see the help for FdriftStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:FDRift', value)

	# noinspection PyTypeChecker
	class FreqOffsetStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Freq_Offset: float: numeric Range: 0 Hz to 500 kHz
			- Freq_Offset_Enab: List[bool]: OFF | ON Disable or enable limit checking for current, average, and maximum results (3 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Offset'),
			ArgStruct('Freq_Offset_Enab', DataType.BooleanList, None, False, False, 3)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Offset: float = None
			self.Freq_Offset_Enab: List[bool] = None

	def get_freq_offset(self) -> FreqOffsetStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:FOFFset \n
		Snippet: value: FreqOffsetStruct = driver.configure.multiEval.limit.cte.lowEnergy.le2M.get_freq_offset() \n
		Sets/gets the frequency offset limit for the CTE portion. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..
		:LE2M..) are available. \n
			:return: structure: for return value, see the help for FreqOffsetStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:FOFFset?', self.__class__.FreqOffsetStruct())

	def set_freq_offset(self, value: FreqOffsetStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:FOFFset \n
		Snippet: driver.configure.multiEval.limit.cte.lowEnergy.le2M.set_freq_offset(value = FreqOffsetStruct()) \n
		Sets/gets the frequency offset limit for the CTE portion. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..
		:LE2M..) are available. \n
			:param value: see the help for FreqOffsetStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:CTE:LENergy:LE2M:FOFFset', value)
