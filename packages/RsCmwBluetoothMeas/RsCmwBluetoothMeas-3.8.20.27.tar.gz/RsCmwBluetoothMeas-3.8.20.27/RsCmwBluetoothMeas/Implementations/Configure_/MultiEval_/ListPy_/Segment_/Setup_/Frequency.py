from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def set(self, frequency: float, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:FREQuency \n
		Snippet: driver.configure.multiEval.listPy.segment.setup.frequency.set(frequency = 1.0, segment = repcap.Segment.Default) \n
		Specifies the center frequency of the signal expected in the segment. \n
			:param frequency: numeric Range: 100 MHz to 6 GHz, Unit: Hz
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		param = Conversions.decimal_value_to_str(frequency)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:FREQuency {param}')

	def get(self, segment=repcap.Segment.Default) -> float:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:FREQuency \n
		Snippet: value: float = driver.configure.multiEval.listPy.segment.setup.frequency.get(segment = repcap.Segment.Default) \n
		Specifies the center frequency of the signal expected in the segment. \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: frequency: numeric Range: 100 MHz to 6 GHz, Unit: Hz"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:FREQuency?')
		return Conversions.str_to_float(response)
