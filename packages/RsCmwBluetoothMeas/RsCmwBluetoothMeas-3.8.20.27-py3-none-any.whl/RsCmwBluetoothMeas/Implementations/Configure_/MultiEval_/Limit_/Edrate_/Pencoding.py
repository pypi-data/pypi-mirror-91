from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pencoding:
	"""Pencoding commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pencoding", core, parent)

	# noinspection PyTypeChecker
	class SsequenceStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sync_Bit_Errors: int: numeric Upper limit for sync bit errors. Range: 0 to 1000
			- Trailer_Bit_Errs: int: numeric Upper limit for trailer bit errors. Range: 0 to 1000
			- Sync_Bit_Enable: bool: OFF | ON Disable or enable the limit check.
			- Trailer_Bit_Enab: bool: OFF | ON Disable or enable the limit check."""
		__meta_args_list = [
			ArgStruct.scalar_int('Sync_Bit_Errors'),
			ArgStruct.scalar_int('Trailer_Bit_Errs'),
			ArgStruct.scalar_bool('Sync_Bit_Enable'),
			ArgStruct.scalar_bool('Trailer_Bit_Enab')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sync_Bit_Errors: int = None
			self.Trailer_Bit_Errs: int = None
			self.Sync_Bit_Enable: bool = None
			self.Trailer_Bit_Enab: bool = None

	def get_ssequence(self) -> SsequenceStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PENCoding:SSEQuence \n
		Snippet: value: SsequenceStruct = driver.configure.multiEval.limit.edrate.pencoding.get_ssequence() \n
		Defines the limit for the differential phase encoding measurement in combined signal path. \n
			:return: structure: for return value, see the help for SsequenceStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PENCoding:SSEQuence?', self.__class__.SsequenceStruct())

	def set_ssequence(self, value: SsequenceStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PENCoding:SSEQuence \n
		Snippet: driver.configure.multiEval.limit.edrate.pencoding.set_ssequence(value = SsequenceStruct()) \n
		Defines the limit for the differential phase encoding measurement in combined signal path. \n
			:param value: see the help for SsequenceStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PENCoding:SSEQuence', value)

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Phase_Encoding: float: numeric Lower limit as percentage of received fault free packets. Range: 0 to 1
			- Phase_Encod_Enab: bool: OFF | ON Disable or enable limit check for the phase encoding."""
		__meta_args_list = [
			ArgStruct.scalar_float('Phase_Encoding'),
			ArgStruct.scalar_bool('Phase_Encod_Enab')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Phase_Encoding: float = None
			self.Phase_Encod_Enab: bool = None

	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PENCoding \n
		Snippet: value: ValueStruct = driver.configure.multiEval.limit.edrate.pencoding.get_value() \n
		Defines the limit for the phase encoding measurement. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PENCoding?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PENCoding \n
		Snippet: driver.configure.multiEval.limit.edrate.pencoding.set_value(value = ValueStruct()) \n
		Defines the limit for the phase encoding measurement. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:EDRate:PENCoding', value)
