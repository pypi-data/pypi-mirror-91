from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Edrate:
	"""Edrate commands group definition. 6 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("edrate", core, parent)

	@property
	def pencoding(self):
		"""pencoding commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pencoding'):
			from .Edrate_.Pencoding import Pencoding
			self._pencoding = Pencoding(self._core, self._base)
		return self._pencoding

	@property
	def dpsk(self):
		"""dpsk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpsk'):
			from .Edrate_.Dpsk import Dpsk
			self._dpsk = Dpsk(self._core, self._base)
		return self._dpsk

	@property
	def dqpsk(self):
		"""dqpsk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dqpsk'):
			from .Edrate_.Dqpsk import Dqpsk
			self._dqpsk = Dqpsk(self._core, self._base)
		return self._dqpsk

	# noinspection PyTypeChecker
	class PowerVsTimeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Dpsk_Minus_Gfsk_Low: float: numeric Range: -99.99 dB to 99.99 dB
			- Dpsk_Minus_Gfsk_Upp: float: numeric Range: -99.99 dB to 99.99 dB
			- Guard_Period_Low: float: numeric Range: -9.99 µs to 9.99 µs
			- Guard_Period_Upp: float: numeric Range: -9.99 µs to 9.99 µs
			- Dpsk_Minus_Gfsk_Enab: List[bool]: OFF | ON Disables or enables the limit check for the DPSK minus GFSK power, 4 values, corresponding to the current, average, maximum and minimum results.
			- Guard_Period_Enab: List[bool]: OFF | ON Disables or enables the limit check for the guard period, 4 values, corresponding to the current, average, maximum and minimum results."""
		__meta_args_list = [
			ArgStruct.scalar_float('Dpsk_Minus_Gfsk_Low'),
			ArgStruct.scalar_float('Dpsk_Minus_Gfsk_Upp'),
			ArgStruct.scalar_float('Guard_Period_Low'),
			ArgStruct.scalar_float('Guard_Period_Upp'),
			ArgStruct('Dpsk_Minus_Gfsk_Enab', DataType.BooleanList, None, False, False, 4),
			ArgStruct('Guard_Period_Enab', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dpsk_Minus_Gfsk_Low: float = None
			self.Dpsk_Minus_Gfsk_Upp: float = None
			self.Guard_Period_Low: float = None
			self.Guard_Period_Upp: float = None
			self.Dpsk_Minus_Gfsk_Enab: List[bool] = None
			self.Guard_Period_Enab: List[bool] = None

	def get_power_vs_time(self) -> PowerVsTimeStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PVTime \n
		Snippet: value: PowerVsTimeStruct = driver.configure.multiEval.limit.edrate.get_power_vs_time() \n
		Defines the power limits for EDR: lower and upper limits for DPSK minus GFSK power and for guard period, limit check
		enabling. \n
			:return: structure: for return value, see the help for PowerVsTimeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PVTime?', self.__class__.PowerVsTimeStruct())

	def set_power_vs_time(self, value: PowerVsTimeStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PVTime \n
		Snippet: driver.configure.multiEval.limit.edrate.set_power_vs_time(value = PowerVsTimeStruct()) \n
		Defines the power limits for EDR: lower and upper limits for DPSK minus GFSK power and for guard period, limit check
		enabling. \n
			:param value: see the help for PowerVsTimeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PVTime', value)

	# noinspection PyTypeChecker
	class FstabilityStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Wi: float: numeric Limit for the initial center frequency error Range: 0 Hz to 250 kHz
			- Wiplus_W_0_Max: float: numeric Limit for the overall uncompensated frequency error Range: 0 Hz to 250 kHz
			- W_0_Max: float: numeric Limit for the maximum compensated frequency error in the DPSK portion of the packet Range: 0 Hz to 250 kHz
			- Wi_Enabled: List[bool]: OFF | ON Enable limits for current, average, and maximum results (3 values)
			- Wi_W_0_Max_Enabled: List[bool]: OFF | ON Enable limits for current, average, and maximum results (3 values)
			- W_0_Max_Enabled: List[bool]: OFF | ON Enable limits for current, average, and maximum results (3 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Wi'),
			ArgStruct.scalar_float('Wiplus_W_0_Max'),
			ArgStruct.scalar_float('W_0_Max'),
			ArgStruct('Wi_Enabled', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Wi_W_0_Max_Enabled', DataType.BooleanList, None, False, False, 3),
			ArgStruct('W_0_Max_Enabled', DataType.BooleanList, None, False, False, 3)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Wi: float = None
			self.Wiplus_W_0_Max: float = None
			self.W_0_Max: float = None
			self.Wi_Enabled: List[bool] = None
			self.Wi_W_0_Max_Enabled: List[bool] = None
			self.W_0_Max_Enabled: List[bool] = None

	def get_fstability(self) -> FstabilityStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:FSTability \n
		Snippet: value: FstabilityStruct = driver.configure.multiEval.limit.edrate.get_fstability() \n
		Defines and activates upper limits for the frequency stability. \n
			:return: structure: for return value, see the help for FstabilityStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:FSTability?', self.__class__.FstabilityStruct())

	def set_fstability(self, value: FstabilityStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:FSTability \n
		Snippet: driver.configure.multiEval.limit.edrate.set_fstability(value = FstabilityStruct()) \n
		Defines and activates upper limits for the frequency stability. \n
			:param value: see the help for FstabilityStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:FSTability', value)

	def clone(self) -> 'Edrate':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Edrate(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
