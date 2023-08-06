from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_le_1_m(self) -> enums.LePacketType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy[:LE1M] \n
		Snippet: value: enums.LePacketType = driver.configure.inputSignal.ptype.lowEnergy.get_le_1_m() \n
		Specifies the packet type of the measured signal for LE uncoded PHY (LE 1M and LE 2M) . Data channel packet cannot be
		selected. It is only automatically selected in combined signal path with LE connection tests. \n
			:return: le_packet_type: RFPHytest | ADVertiser | RFCTe RFPHytest: LE test packet ADVertiser: air interface packet with advertising channel PDU RFCTe: LE with CTE test packet
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LE1M?')
		return Conversions.str_to_scalar_enum(response, enums.LePacketType)

	def set_le_1_m(self, le_packet_type: enums.LePacketType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy[:LE1M] \n
		Snippet: driver.configure.inputSignal.ptype.lowEnergy.set_le_1_m(le_packet_type = enums.LePacketType.ADVertiser) \n
		Specifies the packet type of the measured signal for LE uncoded PHY (LE 1M and LE 2M) . Data channel packet cannot be
		selected. It is only automatically selected in combined signal path with LE connection tests. \n
			:param le_packet_type: RFPHytest | ADVertiser | RFCTe RFPHytest: LE test packet ADVertiser: air interface packet with advertising channel PDU RFCTe: LE with CTE test packet
		"""
		param = Conversions.enum_scalar_to_str(le_packet_type, enums.LePacketType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LE1M {param}')

	# noinspection PyTypeChecker
	def get_lrange(self) -> enums.LePacketType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LRANge \n
		Snippet: value: enums.LePacketType = driver.configure.inputSignal.ptype.lowEnergy.get_lrange() \n
		Specifies the packet type of the measured signal for LE coded PHY. Data channel packet cannot be selected. It is only
		automatically selected in combined signal path with LE connection tests. \n
			:return: le_lr_packet_type: RFPHytest | ADVertiser RFPHytest: LE test packet ADVertiser: air interface packet with advertising channel PDU
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.LePacketType)

	def set_lrange(self, le_lr_packet_type: enums.LePacketType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LRANge \n
		Snippet: driver.configure.inputSignal.ptype.lowEnergy.set_lrange(le_lr_packet_type = enums.LePacketType.ADVertiser) \n
		Specifies the packet type of the measured signal for LE coded PHY. Data channel packet cannot be selected. It is only
		automatically selected in combined signal path with LE connection tests. \n
			:param le_lr_packet_type: RFPHytest | ADVertiser RFPHytest: LE test packet ADVertiser: air interface packet with advertising channel PDU
		"""
		param = Conversions.enum_scalar_to_str(le_lr_packet_type, enums.LePacketType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LRANge {param}')

	# noinspection PyTypeChecker
	def get_le_2_m(self) -> enums.LePacketType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LE2M \n
		Snippet: value: enums.LePacketType = driver.configure.inputSignal.ptype.lowEnergy.get_le_2_m() \n
		Specifies the packet type of the measured signal for LE uncoded PHY (LE 1M and LE 2M) . Data channel packet cannot be
		selected. It is only automatically selected in combined signal path with LE connection tests. \n
			:return: ele_packet_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LE2M?')
		return Conversions.str_to_scalar_enum(response, enums.LePacketType)

	def set_le_2_m(self, ele_packet_type: enums.LePacketType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LE2M \n
		Snippet: driver.configure.inputSignal.ptype.lowEnergy.set_le_2_m(ele_packet_type = enums.LePacketType.ADVertiser) \n
		Specifies the packet type of the measured signal for LE uncoded PHY (LE 1M and LE 2M) . Data channel packet cannot be
		selected. It is only automatically selected in combined signal path with LE connection tests. \n
			:param ele_packet_type: RFPHytest | ADVertiser | RFCTe RFPHytest: LE test packet ADVertiser: air interface packet with advertising channel PDU RFCTe: LE with CTE test packet
		"""
		param = Conversions.enum_scalar_to_str(ele_packet_type, enums.LePacketType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:PTYPe:LENergy:LE2M {param}')
