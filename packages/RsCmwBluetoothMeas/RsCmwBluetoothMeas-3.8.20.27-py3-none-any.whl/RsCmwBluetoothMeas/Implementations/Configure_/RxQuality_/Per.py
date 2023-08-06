from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Per:
	"""Per commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("per", core, parent)

	def get_level(self) -> float:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:PER:LEVel \n
		Snippet: value: float = driver.configure.rxQuality.per.get_level() \n
		Sets the Tx level of R&S CMW for PER measurements. The allowed value range can be calculated as follows: Range (Level) =
		Range (Output Power) - External Attenuation Range (Output Power) = -130 dBm to 0 dBm (RFx COM) or -120 dBm to 8 dBm (RFx
		OUT) ; please also notice the ranges quoted in the data sheet. \n
			:return: level: numeric Range: see above
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:PER:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:PER:LEVel \n
		Snippet: driver.configure.rxQuality.per.set_level(level = 1.0) \n
		Sets the Tx level of R&S CMW for PER measurements. The allowed value range can be calculated as follows: Range (Level) =
		Range (Output Power) - External Attenuation Range (Output Power) = -130 dBm to 0 dBm (RFx COM) or -120 dBm to 8 dBm (RFx
		OUT) ; please also notice the ranges quoted in the data sheet. \n
			:param level: numeric Range: see above
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:PER:LEVel {param}')

	def get_tx_packets(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:PER:TXPackets \n
		Snippet: value: int = driver.configure.rxQuality.per.get_tx_packets() \n
		Sets number of packets for PER measurements. \n
			:return: packets_to_send: numeric Range: 1 to 100E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:PER:TXPackets?')
		return Conversions.str_to_int(response)

	def set_tx_packets(self, packets_to_send: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:PER:TXPackets \n
		Snippet: driver.configure.rxQuality.per.set_tx_packets(packets_to_send = 1) \n
		Sets number of packets for PER measurements. \n
			:param packets_to_send: numeric Range: 1 to 100E+3
		"""
		param = Conversions.decimal_value_to_str(packets_to_send)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:PER:TXPackets {param}')
