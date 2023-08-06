from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2M:
	"""Le2M commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le2M", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Per: float: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Packets_Received: int: decimal Number of correct packets received and reported by the DUT. Range: 0 to 30E+3"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_int('Packets_Received')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Packets_Received: int = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LENergy:LE2M \n
		Snippet: value: ResultData = driver.dtMode.rxQuality.per.lowEnergy.le2M.read() \n
		Return all results of the non-signaling LE Rx measurement for LE direct test. Commands for uncoded LE 1M PHY (..:LE1M..) ,
		LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LENergy:LE2M?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LENergy:LE2M \n
		Snippet: value: ResultData = driver.dtMode.rxQuality.per.lowEnergy.le2M.fetch() \n
		Return all results of the non-signaling LE Rx measurement for LE direct test. Commands for uncoded LE 1M PHY (..:LE1M..) ,
		LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LENergy:LE2M?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Per: float: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Packets_Received: float: decimal Number of correct packets received and reported by the DUT. Range: 0 to 30E+3"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_float('Packets_Received')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Packets_Received: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LENergy:LE2M \n
		Snippet: value: CalculateStruct = driver.dtMode.rxQuality.per.lowEnergy.le2M.calculate() \n
		Return all results of the non-signaling LE Rx measurement for LE direct test. Commands for uncoded LE 1M PHY (..:LE1M..) ,
		LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LENergy:LE2M?', self.__class__.CalculateStruct())
