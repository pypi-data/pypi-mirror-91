from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 5 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	@property
	def extended(self):
		"""extended commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_extended'):
			from .Current_.Extended import Extended
			self._extended = Extended(self._core, self._base)
		return self._extended

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Omega_I: float: float Initial center frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Omega_Iplus_Omega_0_Max: float: float Maximum compensated frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Omega_0_Max: float: float Maximum compensated frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Rms_Devm: float: float Differential EVM results Range: 0 to 1
			- Peak_Devm: float: float Range: 0 to 1
			- P_99_Devm: float: float Range: 0 to 1
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Omega_I'),
			ArgStruct.scalar_float('Omega_Iplus_Omega_0_Max'),
			ArgStruct.scalar_float('Omega_0_Max'),
			ArgStruct.scalar_float('Rms_Devm'),
			ArgStruct.scalar_float('Peak_Devm'),
			ArgStruct.scalar_float('P_99_Devm'),
			ArgStruct.scalar_float('Nominal_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Omega_I: float = None
			self.Omega_Iplus_Omega_0_Max: float = None
			self.Omega_0_Max: float = None
			self.Rms_Devm: float = None
			self.Peak_Devm: float = None
			self.P_99_Devm: float = None
			self.Nominal_Power: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:CURRent \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.edrate.current.calculate() \n
		Returns the modulation results for EDR packets. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:CURRent?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:BLUetooth:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Omega_I: float: float Initial center frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Omega_Iplus_Omega_0_Max: float: float Maximum compensated frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Omega_0_Max: float: float Maximum compensated frequency error Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Rms_Devm: float: float Differential EVM results Range: 0 to 1
			- Peak_Devm: float: float Range: 0 to 1
			- P_99_Devm: float: float Range: 0 to 1
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Omega_I'),
			ArgStruct.scalar_float('Omega_Iplus_Omega_0_Max'),
			ArgStruct.scalar_float('Omega_0_Max'),
			ArgStruct.scalar_float('Rms_Devm'),
			ArgStruct.scalar_float('Peak_Devm'),
			ArgStruct.scalar_float('P_99_Devm'),
			ArgStruct.scalar_float('Nominal_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Omega_I: float = None
			self.Omega_Iplus_Omega_0_Max: float = None
			self.Omega_0_Max: float = None
			self.Rms_Devm: float = None
			self.Peak_Devm: float = None
			self.P_99_Devm: float = None
			self.Nominal_Power: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:CURRent \n
		Snippet: value: ResultData = driver.multiEval.modulation.edrate.current.fetch() \n
		Returns the modulation results for EDR packets. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:CURRent?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:CURRent \n
		Snippet: value: ResultData = driver.multiEval.modulation.edrate.current.read() \n
		Returns the modulation results for EDR packets. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:EDRate:CURRent?', self.__class__.ResultData())

	def clone(self) -> 'Current':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Current(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
