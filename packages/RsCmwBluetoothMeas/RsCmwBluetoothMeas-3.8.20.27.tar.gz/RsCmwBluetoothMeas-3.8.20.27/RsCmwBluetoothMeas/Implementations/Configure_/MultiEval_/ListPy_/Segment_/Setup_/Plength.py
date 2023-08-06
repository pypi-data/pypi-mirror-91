from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Plength:
	"""Plength commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("plength", core, parent)

	def set(self, payload_length: int, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:PLENgth \n
		Snippet: driver.configure.multiEval.listPy.segment.setup.plength.set(payload_length = 1, segment = repcap.Segment.Default) \n
		Specifies the payload length expected in the segment. \n
			:param payload_length: numeric Range: 0 Byte(s) to 1021 Byte(s)
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		param = Conversions.decimal_value_to_str(payload_length)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:PLENgth {param}')

	def get(self, segment=repcap.Segment.Default) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:PLENgth \n
		Snippet: value: int = driver.configure.multiEval.listPy.segment.setup.plength.get(segment = repcap.Segment.Default) \n
		Specifies the payload length expected in the segment. \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: payload_length: numeric Range: 0 Byte(s) to 1021 Byte(s)"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:PLENgth?')
		return Conversions.str_to_int(response)
