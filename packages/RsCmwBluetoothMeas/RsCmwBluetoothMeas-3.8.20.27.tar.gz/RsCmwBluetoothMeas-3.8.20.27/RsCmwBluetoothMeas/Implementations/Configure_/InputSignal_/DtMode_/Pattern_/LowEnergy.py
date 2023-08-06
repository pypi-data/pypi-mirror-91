from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_le_1_m(self) -> enums.PatternType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LE1M \n
		Snippet: value: enums.PatternType = driver.configure.inputSignal.dtMode.pattern.lowEnergy.get_le_1_m() \n
		Specifies the data pattern type that the EUT transmits as user payload data in its LE packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 ALL0: '00000000' P11: '10101010' in transmission order (LSB first) P44: '11110000' in transmission order (LSB first) ALL1: '11111111' PRBS9: pseudorandom binary sequence of length 9
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LE1M?')
		return Conversions.str_to_scalar_enum(response, enums.PatternType)

	def set_le_1_m(self, pattern_type: enums.PatternType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LE1M \n
		Snippet: driver.configure.inputSignal.dtMode.pattern.lowEnergy.set_le_1_m(pattern_type = enums.PatternType.ALL0) \n
		Specifies the data pattern type that the EUT transmits as user payload data in its LE packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:param pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 ALL0: '00000000' P11: '10101010' in transmission order (LSB first) P44: '11110000' in transmission order (LSB first) ALL1: '11111111' PRBS9: pseudorandom binary sequence of length 9
		"""
		param = Conversions.enum_scalar_to_str(pattern_type, enums.PatternType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LE1M {param}')

	# noinspection PyTypeChecker
	def get_le_2_m(self) -> enums.PatternType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LE2M \n
		Snippet: value: enums.PatternType = driver.configure.inputSignal.dtMode.pattern.lowEnergy.get_le_2_m() \n
		Specifies the data pattern type that the EUT transmits as user payload data in its LE packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 ALL0: '00000000' P11: '10101010' in transmission order (LSB first) P44: '11110000' in transmission order (LSB first) ALL1: '11111111' PRBS9: pseudorandom binary sequence of length 9
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LE2M?')
		return Conversions.str_to_scalar_enum(response, enums.PatternType)

	def set_le_2_m(self, pattern_type: enums.PatternType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LE2M \n
		Snippet: driver.configure.inputSignal.dtMode.pattern.lowEnergy.set_le_2_m(pattern_type = enums.PatternType.ALL0) \n
		Specifies the data pattern type that the EUT transmits as user payload data in its LE packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:param pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 ALL0: '00000000' P11: '10101010' in transmission order (LSB first) P44: '11110000' in transmission order (LSB first) ALL1: '11111111' PRBS9: pseudorandom binary sequence of length 9
		"""
		param = Conversions.enum_scalar_to_str(pattern_type, enums.PatternType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LE2M {param}')

	# noinspection PyTypeChecker
	def get_lrange(self) -> enums.PatternType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LRANge \n
		Snippet: value: enums.PatternType = driver.configure.inputSignal.dtMode.pattern.lowEnergy.get_lrange() \n
		Specifies the data pattern type that the EUT transmits as user payload data in its LE packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 ALL0: '00000000' P11: '10101010' in transmission order (LSB first) P44: '11110000' in transmission order (LSB first) ALL1: '11111111' PRBS9: pseudorandom binary sequence of length 9
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.PatternType)

	def set_lrange(self, pattern_type: enums.PatternType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LRANge \n
		Snippet: driver.configure.inputSignal.dtMode.pattern.lowEnergy.set_lrange(pattern_type = enums.PatternType.ALL0) \n
		Specifies the data pattern type that the EUT transmits as user payload data in its LE packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:param pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 ALL0: '00000000' P11: '10101010' in transmission order (LSB first) P44: '11110000' in transmission order (LSB first) ALL1: '11111111' PRBS9: pseudorandom binary sequence of length 9
		"""
		param = Conversions.enum_scalar_to_str(pattern_type, enums.PatternType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DTMode:PATTern:LENergy:LRANge {param}')
