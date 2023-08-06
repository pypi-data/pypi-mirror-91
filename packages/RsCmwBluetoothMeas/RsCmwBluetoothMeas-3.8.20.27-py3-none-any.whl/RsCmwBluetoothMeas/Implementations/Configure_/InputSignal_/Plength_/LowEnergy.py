from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy[:LE1M] \n
		Snippet: value: int = driver.configure.inputSignal.plength.lowEnergy.get_le_1_m() \n
		Specifies the number of bytes (octets) in the payload data of the measured LE test packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LE2M
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LRANge \n
			:return: payload_length: numeric Payload lengths for LE packets Range: 0 Byte(s) to 255 Byte(s) , Unit: byte
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LE1M?')
		return Conversions.str_to_int(response)

	def set_le_1_m(self, payload_length: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy[:LE1M] \n
		Snippet: driver.configure.inputSignal.plength.lowEnergy.set_le_1_m(payload_length = 1) \n
		Specifies the number of bytes (octets) in the payload data of the measured LE test packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LE2M
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LRANge \n
			:param payload_length: numeric Payload lengths for LE packets Range: 0 Byte(s) to 255 Byte(s) , Unit: byte
		"""
		param = Conversions.decimal_value_to_str(payload_length)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LE1M {param}')

	def get_lrange(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LRANge \n
		Snippet: value: int = driver.configure.inputSignal.plength.lowEnergy.get_lrange() \n
		Specifies the number of bytes (octets) in the payload data of the measured LE test packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LE2M
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LRANge \n
			:return: payload_length: numeric Payload lengths for LE packets Range: 0 Byte(s) to 255 Byte(s) , Unit: byte
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LRANge?')
		return Conversions.str_to_int(response)

	def set_lrange(self, payload_length: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LRANge \n
		Snippet: driver.configure.inputSignal.plength.lowEnergy.set_lrange(payload_length = 1) \n
		Specifies the number of bytes (octets) in the payload data of the measured LE test packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LE2M
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LRANge \n
			:param payload_length: numeric Payload lengths for LE packets Range: 0 Byte(s) to 255 Byte(s) , Unit: byte
		"""
		param = Conversions.decimal_value_to_str(payload_length)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LRANge {param}')

	def get_le_2_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LE2M \n
		Snippet: value: int = driver.configure.inputSignal.plength.lowEnergy.get_le_2_m() \n
		Specifies the number of bytes (octets) in the payload data of the measured LE test packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LE2M
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LRANge \n
			:return: payload_length: numeric Payload lengths for LE packets Range: 0 Byte(s) to 255 Byte(s) , Unit: byte
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LE2M?')
		return Conversions.str_to_int(response)

	def set_le_2_m(self, payload_length: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LE2M \n
		Snippet: driver.configure.inputSignal.plength.lowEnergy.set_le_2_m(payload_length = 1) \n
		Specifies the number of bytes (octets) in the payload data of the measured LE test packets. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LE2M
			- CONFigure:BLUetooth:SIGN<i>:CONNection:PACKets:PLENgth:LENergy:LRANge \n
			:param payload_length: numeric Payload lengths for LE packets Range: 0 Byte(s) to 255 Byte(s) , Unit: byte
		"""
		param = Conversions.decimal_value_to_str(payload_length)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PLENgth:LENergy:LE2M {param}')
