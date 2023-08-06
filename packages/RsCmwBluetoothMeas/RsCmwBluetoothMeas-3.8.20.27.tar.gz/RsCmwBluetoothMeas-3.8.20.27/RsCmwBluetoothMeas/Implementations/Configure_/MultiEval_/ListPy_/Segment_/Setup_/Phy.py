from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phy:
	"""Phy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phy", core, parent)

	def set(self, le_phy_type: enums.LePhysicalType, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:PHY \n
		Snippet: driver.configure.multiEval.listPy.segment.setup.phy.set(le_phy_type = enums.LePhysicalType.LE1M, segment = repcap.Segment.Default) \n
		Defines physical layer ( PHY) for segment according to the core specification version 5.0 for Bluetooth wireless
		technology. \n
			:param le_phy_type: LE1M | LE2M | LELR LE1M: LE 1 Msymbol/s uncoded PHY LE2M: LE 2 Msymbol/s uncoded PHY LELR: LE 1 Msymbol/s long range (LE coded PHY)
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		param = Conversions.enum_scalar_to_str(le_phy_type, enums.LePhysicalType)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:PHY {param}')

	# noinspection PyTypeChecker
	def get(self, segment=repcap.Segment.Default) -> enums.LePhysicalType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:PHY \n
		Snippet: value: enums.LePhysicalType = driver.configure.multiEval.listPy.segment.setup.phy.get(segment = repcap.Segment.Default) \n
		Defines physical layer ( PHY) for segment according to the core specification version 5.0 for Bluetooth wireless
		technology. \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: le_phy_type: LE1M | LE2M | LELR LE1M: LE 1 Msymbol/s uncoded PHY LE2M: LE 2 Msymbol/s uncoded PHY LELR: LE 1 Msymbol/s long range (LE coded PHY)"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:PHY?')
		return Conversions.str_to_scalar_enum(response, enums.LePhysicalType)
