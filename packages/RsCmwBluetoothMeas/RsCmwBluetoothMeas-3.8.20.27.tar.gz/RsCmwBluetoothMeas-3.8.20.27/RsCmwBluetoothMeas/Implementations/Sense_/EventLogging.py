from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Types import DataType
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EventLogging:
	"""EventLogging commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eventLogging", core, parent)

	# noinspection PyTypeChecker
	class LastStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Timestamp: str: string Timestamp of the entry as string in the format 'hh:mm:ss'
			- Category: enums.LogCategory: INFO | WARNing | ERRor | CONTinue Category of the entry, as indicated in the main view by an icon CONTinue means the continuation of previous entry.
			- Event: str: string Text string describing the event"""
		__meta_args_list = [
			ArgStruct.scalar_str('Timestamp'),
			ArgStruct.scalar_enum('Category', enums.LogCategory),
			ArgStruct.scalar_str('Event')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Timestamp: str = None
			self.Category: enums.LogCategory = None
			self.Event: str = None

	def get_last(self) -> LastStruct:
		"""SCPI: SENSe:BLUetooth:MEASurement<Instance>:ELOGging:LAST \n
		Snippet: value: LastStruct = driver.sense.eventLogging.get_last() \n
		Queries the latest entry of the event log. \n
			:return: structure: for return value, see the help for LastStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:MEASurement<Instance>:ELOGging:LAST?', self.__class__.LastStruct())

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Timestamp: List[str]: string Timestamp of the entry as string in the format 'hh:mm:ss'
			- Category: List[enums.LogCategory]: INFO | WARNing | ERRor | CONTinue Category of the entry, as indicated in the main view by an icon CONTinue means the continuation of previous entry.
			- Event: List[str]: string Text string describing the event"""
		__meta_args_list = [
			ArgStruct('Timestamp', DataType.StringList, None, False, True, 1),
			ArgStruct('Category', DataType.EnumList, enums.LogCategory, False, True, 1),
			ArgStruct('Event', DataType.StringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Timestamp: List[str] = None
			self.Category: List[enums.LogCategory] = None
			self.Event: List[str] = None

	def get_all(self) -> AllStruct:
		"""SCPI: SENSe:BLUetooth:MEASurement<Instance>:ELOGging:ALL \n
		Snippet: value: AllStruct = driver.sense.eventLogging.get_all() \n
		Queries all entries of the event log. For each entry three parameters are returned, from oldest to latest entry:
		{<Timestamp>, <Category>, <Event>}entry 1, {<Timestamp>, <Category>, <Event>}entry 2, ... \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:MEASurement<Instance>:ELOGging:ALL?', self.__class__.AllStruct())
