from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fdrift:
	"""Fdrift commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fdrift", core, parent)

	# noinspection PyTypeChecker
	class ApacketsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Freq_Drift_Dh_1: float: numeric Range: 0 Hz to 250 kHz
			- Freq_Drift_Dh_3: float: numeric Range: 0 Hz to 250 kHz
			- Freq_Drift_Dh_5: float: numeric Range: 0 Hz to 250 kHz
			- Max_Drift_Rate: float: numeric Range: 0 Hz to 250 kHz
			- Freq_Drift_Dh_1_Enb: List[bool]: OFF | ON Disable or enable limit check for current, average, and maximum results (3 values) .
			- Freq_Drift_Dh_3_Enb: List[bool]: OFF | ON Disable or enable limit check for current, average, and maximum results (3 values) .
			- Freq_Drift_Dh_5_Enb: List[bool]: OFF | ON Disable or enable limit check for current, average, and maximum results (3 values) .
			- Max_Drift_Rate_Enb: List[bool]: OFF | ON Disable or enable limit check for current, average, and maximum results (3 values) ."""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Drift_Dh_1'),
			ArgStruct.scalar_float('Freq_Drift_Dh_3'),
			ArgStruct.scalar_float('Freq_Drift_Dh_5'),
			ArgStruct.scalar_float('Max_Drift_Rate'),
			ArgStruct('Freq_Drift_Dh_1_Enb', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Freq_Drift_Dh_3_Enb', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Freq_Drift_Dh_5_Enb', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Max_Drift_Rate_Enb', DataType.BooleanList, None, False, False, 3)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Drift_Dh_1: float = None
			self.Freq_Drift_Dh_3: float = None
			self.Freq_Drift_Dh_5: float = None
			self.Max_Drift_Rate: float = None
			self.Freq_Drift_Dh_1_Enb: List[bool] = None
			self.Freq_Drift_Dh_3_Enb: List[bool] = None
			self.Freq_Drift_Dh_5_Enb: List[bool] = None
			self.Max_Drift_Rate_Enb: List[bool] = None

	def get_apackets(self) -> ApacketsStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FDRift:APACkets \n
		Snippet: value: ApacketsStruct = driver.configure.multiEval.limit.brate.fdrift.get_apackets() \n
		Defines the limits for the frequency drift and the maximum drift rate for BR. For each packet type (DH1, DH3, DH5) a
		different frequency drift limit can be specified. \n
			:return: structure: for return value, see the help for ApacketsStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FDRift:APACkets?', self.__class__.ApacketsStruct())

	def set_apackets(self, value: ApacketsStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FDRift:APACkets \n
		Snippet: driver.configure.multiEval.limit.brate.fdrift.set_apackets(value = ApacketsStruct()) \n
		Defines the limits for the frequency drift and the maximum drift rate for BR. For each packet type (DH1, DH3, DH5) a
		different frequency drift limit can be specified. \n
			:param value: see the help for ApacketsStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FDRift:APACkets', value)

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Frequency_Drift: float: numeric Range: 0 Hz to 250 kHz
			- Max_Drift_Rate: float: numeric Range: 0 Hz to 250 kHz
			- Freq_Drift_Enable: List[bool]: OFF | ON Disable or enable limit check for current, average, and maximum results (3 values) .
			- Max_Drift_Rate_Enb: List[bool]: OFF | ON Disable or enable limit check for current, average, and maximum results (3 values) ."""
		__meta_args_list = [
			ArgStruct.scalar_float('Frequency_Drift'),
			ArgStruct.scalar_float('Max_Drift_Rate'),
			ArgStruct('Freq_Drift_Enable', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Max_Drift_Rate_Enb', DataType.BooleanList, None, False, False, 3)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Frequency_Drift: float = None
			self.Max_Drift_Rate: float = None
			self.Freq_Drift_Enable: List[bool] = None
			self.Max_Drift_Rate_Enb: List[bool] = None

	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FDRift \n
		Snippet: value: ValueStruct = driver.configure.multiEval.limit.brate.fdrift.get_value() \n
		Defines the frequency drift limit for DH1 packets and the maximum drift rate limit for all BR packets. Since V2.1.
		20, this command is superseded by the command method RsCmwBluetoothMeas.Configure.MultiEval.Limit.Brate.Fdrift.apackets
		that allows to set different limits for different packet types. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FDRift?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FDRift \n
		Snippet: driver.configure.multiEval.limit.brate.fdrift.set_value(value = ValueStruct()) \n
		Defines the frequency drift limit for DH1 packets and the maximum drift rate limit for all BR packets. Since V2.1.
		20, this command is superseded by the command method RsCmwBluetoothMeas.Configure.MultiEval.Limit.Brate.Fdrift.apackets
		that allows to set different limits for different packet types. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:FDRift', value)
