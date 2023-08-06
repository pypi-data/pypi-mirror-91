from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("result", core, parent)

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Spot_Check: bool: OFF | ON Spot check ON: Evaluate results OFF: Do not evaluate results
			- Power: bool: OFF | ON Statistical power results
			- Modulation: bool: OFF | ON Statistical modulation results
			- Spectrum_Acp: bool: OFF | ON Spectrum ACP results Only ACP+/-5 channel mode supported (21 half-channels)"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Spot_Check'),
			ArgStruct.scalar_bool('Power'),
			ArgStruct.scalar_bool('Modulation'),
			ArgStruct.scalar_bool('Spectrum_Acp')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Spot_Check: bool = None
			self.Power: bool = None
			self.Modulation: bool = None
			self.Spectrum_Acp: bool = None

	def get_all(self) -> AllStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:TRX:RESult[:ALL] \n
		Snippet: value: AllStruct = driver.configure.trx.result.get_all() \n
		Enables or disables the evaluation of results. \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:TRX:RESult:ALL?', self.__class__.AllStruct())

	def set_all(self, value: AllStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:TRX:RESult[:ALL] \n
		Snippet: driver.configure.trx.result.set_all(value = AllStruct()) \n
		Enables or disables the evaluation of results. \n
			:param value: see the help for AllStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:TRX:RESult:ALL', value)
