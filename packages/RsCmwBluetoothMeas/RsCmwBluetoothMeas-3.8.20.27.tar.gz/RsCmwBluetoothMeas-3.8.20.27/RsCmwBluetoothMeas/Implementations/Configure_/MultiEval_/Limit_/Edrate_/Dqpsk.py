from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dqpsk:
	"""Dqpsk commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dqpsk", core, parent)

	# noinspection PyTypeChecker
	class DevmStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rms: float: numeric Limit for RMS DEVM (π/4 DQPSK) Range: 0 to 1
			- Peak: float: numeric Limit for peak DEVM (π/4 DQPSK) Range: 0 to 1
			- P_99: float: numeric Limit for 99% DEVM (π/4 DQPSK) Range: 0 to 1
			- Rms_Enabled: List[bool]: OFF | ON Disable or enable limit check for current, average, and maximum results (3 values)
			- Peak_Enabled: List[bool]: OFF | ON Disable or enable limit check for current, average, and maximum results (3 values)
			- P_99_Enabled: bool: OFF | ON Disable or enable limit check for current result (1 value)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Rms'),
			ArgStruct.scalar_float('Peak'),
			ArgStruct.scalar_float('P_99'),
			ArgStruct('Rms_Enabled', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Peak_Enabled', DataType.BooleanList, None, False, False, 3),
			ArgStruct.scalar_bool('P_99_Enabled')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rms: float = None
			self.Peak: float = None
			self.P_99: float = None
			self.Rms_Enabled: List[bool] = None
			self.Peak_Enabled: List[bool] = None
			self.P_99_Enabled: bool = None

	def get_devm(self) -> DevmStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:DQPSk:DEVM \n
		Snippet: value: DevmStruct = driver.configure.multiEval.limit.edrate.dqpsk.get_devm() \n
		Defines and activates upper limits for the differential error vector magnitude for π/4 DQPSK modulated packets (2-DHx) . \n
			:return: structure: for return value, see the help for DevmStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:DQPSk:DEVM?', self.__class__.DevmStruct())

	def set_devm(self, value: DevmStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:DQPSk:DEVM \n
		Snippet: driver.configure.multiEval.limit.edrate.dqpsk.set_devm(value = DevmStruct()) \n
		Defines and activates upper limits for the differential error vector magnitude for π/4 DQPSK modulated packets (2-DHx) . \n
			:param value: see the help for DevmStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:DQPSk:DEVM', value)
