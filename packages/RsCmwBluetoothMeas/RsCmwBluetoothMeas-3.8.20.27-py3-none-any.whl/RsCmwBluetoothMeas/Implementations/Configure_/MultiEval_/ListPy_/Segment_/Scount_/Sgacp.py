from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sgacp:
	"""Sgacp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sgacp", core, parent)

	def set(self, spec_gat_acp_stat_cnt: int, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:SCOunt:SGACp \n
		Snippet: driver.configure.multiEval.listPy.segment.scount.sgacp.set(spec_gat_acp_stat_cnt = 1, segment = repcap.Segment.Default) \n
		Defines the statistic count in the segment. The last mnemonic denotes the measurement type: statistical modulation
		measurement, statistical power measurement, spectrum ACP measurement (BR, LE) , spectrum gated ACP measurement (EDR) ,
		spectrum 20 dB bandwidth (occupied bandwidth) measurement (BR) . \n
			:param spec_gat_acp_stat_cnt: numeric Statistic count Range: 1 to 1000
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		param = Conversions.decimal_value_to_str(spec_gat_acp_stat_cnt)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SCOunt:SGACp {param}')

	def get(self, segment=repcap.Segment.Default) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:SCOunt:SGACp \n
		Snippet: value: int = driver.configure.multiEval.listPy.segment.scount.sgacp.get(segment = repcap.Segment.Default) \n
		Defines the statistic count in the segment. The last mnemonic denotes the measurement type: statistical modulation
		measurement, statistical power measurement, spectrum ACP measurement (BR, LE) , spectrum gated ACP measurement (EDR) ,
		spectrum 20 dB bandwidth (occupied bandwidth) measurement (BR) . \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: spec_gat_acp_stat_cnt: numeric Statistic count Range: 1 to 1000"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SCOunt:SGACp?')
		return Conversions.str_to_int(response)
