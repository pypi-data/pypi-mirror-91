from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pscalar:
	"""Pscalar commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pscalar", core, parent)

	def set(self, enable_pow_scalar: bool, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:RESults:PSCalar \n
		Snippet: driver.configure.multiEval.listPy.segment.results.pscalar.set(enable_pow_scalar = False, segment = repcap.Segment.Default) \n
		Enables or disables the evaluation of results for the segment<no> in list mode. The last mnemonic denotes the measurement
		type: statistical modulation results, statistical power results, spectrum ACP (BR, LE) , spectrum gated ACP (EDR) ,
		occupied bandwidth (BR) . \n
			:param enable_pow_scalar: No help available
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		param = Conversions.bool_to_str(enable_pow_scalar)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:RESults:PSCalar {param}')

	def get(self, segment=repcap.Segment.Default) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:RESults:PSCalar \n
		Snippet: value: bool = driver.configure.multiEval.listPy.segment.results.pscalar.get(segment = repcap.Segment.Default) \n
		Enables or disables the evaluation of results for the segment<no> in list mode. The last mnemonic denotes the measurement
		type: statistical modulation results, statistical power results, spectrum ACP (BR, LE) , spectrum gated ACP (EDR) ,
		occupied bandwidth (BR) . \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: enable_pow_scalar: No help available"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:RESults:PSCalar?')
		return Conversions.str_to_bool(response)
