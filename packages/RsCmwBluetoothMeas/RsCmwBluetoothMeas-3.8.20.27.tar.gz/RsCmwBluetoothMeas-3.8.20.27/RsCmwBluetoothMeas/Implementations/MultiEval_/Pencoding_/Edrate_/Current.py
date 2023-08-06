from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	@property
	def c(self):
		"""c commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_c'):
			from .Current_.C import C
			self._c = C(self._core, self._base)
		return self._c

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: float 'Reliability Indicator'
			- Nominal_Power: float: float Average power during the carrier-on state Range: -128 dBm to 30 dBm , Unit: dBm
			- Bit_Error_Rate: float: float Number of bit errors in the received burst, as a percentage of the total number of bits received Range: 0 % to 100 %, Unit: %
			- Packets_0_Errors: float: float Number of bit error free packets received, as a percentage of all the bursts received Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Bit_Error_Rate'),
			ArgStruct.scalar_float('Packets_0_Errors')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nominal_Power: float = None
			self.Bit_Error_Rate: float = None
			self.Packets_0_Errors: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:PENCoding:EDRate:CURRent \n
		Snippet: value: ResultData = driver.multiEval.pencoding.edrate.current.read() \n
		Returns the 'Differential Phase Encoding' results for EDR packets (single values) . The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:PENCoding:EDRate:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:PENCoding:EDRate:CURRent \n
		Snippet: value: ResultData = driver.multiEval.pencoding.edrate.current.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:PENCoding:EDRate:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: float 'Reliability Indicator'
			- Nominal_Power: float: float Average power during the carrier-on state Range: -128 dBm to 30 dBm , Unit: dBm
			- Bit_Error_Rate: float: float Number of bit errors in the received burst, as a percentage of the total number of bits received Range: 0 % to 100 %, Unit: %
			- Packets_0_Errors: float: float Number of bit error free packets received, as a percentage of all the bursts received Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Bit_Error_Rate'),
			ArgStruct.scalar_float('Packets_0_Errors')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nominal_Power: float = None
			self.Bit_Error_Rate: float = None
			self.Packets_0_Errors: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:PENCoding:EDRate:CURRent \n
		Snippet: value: CalculateStruct = driver.multiEval.pencoding.edrate.current.calculate() \n
		Returns the 'Differential Phase Encoding' results for EDR packets (single values) . The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:PENCoding:EDRate:CURRent?', self.__class__.CalculateStruct())

	def clone(self) -> 'Current':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Current(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
