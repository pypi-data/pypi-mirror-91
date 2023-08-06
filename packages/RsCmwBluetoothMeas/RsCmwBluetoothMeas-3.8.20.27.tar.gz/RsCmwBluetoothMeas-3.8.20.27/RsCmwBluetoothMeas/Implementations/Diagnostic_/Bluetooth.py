from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bluetooth:
	"""Bluetooth commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bluetooth", core, parent)

	# noinspection PyTypeChecker
	class SynchroniseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Min_No_Valid_Bursts: int: No parameter help available
			- Syn_Check_Filter: int: No parameter help available
			- Max_Invalid_Burst: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Min_No_Valid_Bursts'),
			ArgStruct.scalar_int('Syn_Check_Filter'),
			ArgStruct.scalar_int('Max_Invalid_Burst')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Min_No_Valid_Bursts: int = None
			self.Syn_Check_Filter: int = None
			self.Max_Invalid_Burst: int = None

	def get_synchronise(self) -> SynchroniseStruct:
		"""SCPI: DIAGnostic:BLUetooth:SYNChronise \n
		Snippet: value: SynchroniseStruct = driver.diagnostic.bluetooth.get_synchronise() \n
		No command help available \n
			:return: structure: for return value, see the help for SynchroniseStruct structure arguments.
		"""
		return self._core.io.query_struct('DIAGnostic:BLUetooth:SYNChronise?', self.__class__.SynchroniseStruct())

	def set_synchronise(self, value: SynchroniseStruct) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SYNChronise \n
		Snippet: driver.diagnostic.bluetooth.set_synchronise(value = SynchroniseStruct()) \n
		No command help available \n
			:param value: see the help for SynchroniseStruct structure arguments.
		"""
		self._core.io.write_struct('DIAGnostic:BLUetooth:SYNChronise', value)
