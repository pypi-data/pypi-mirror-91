from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Oslots:
	"""Oslots commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("oslots", core, parent)

	def set(self, no_of_off_slots: int, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:OSLots \n
		Snippet: driver.configure.multiEval.listPy.segment.setup.oslots.set(no_of_off_slots = 1, segment = repcap.Segment.Default) \n
		Specifies the number of unused slots between any two occupied slots or slot sequences expected in the segment. \n
			:param no_of_off_slots: numeric Range: 1 to 9
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')"""
		param = Conversions.decimal_value_to_str(no_of_off_slots)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:OSLots {param}')

	def get(self, segment=repcap.Segment.Default) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:SETup]:OSLots \n
		Snippet: value: int = driver.configure.multiEval.listPy.segment.setup.oslots.get(segment = repcap.Segment.Default) \n
		Specifies the number of unused slots between any two occupied slots or slot sequences expected in the segment. \n
			:param segment: optional repeated capability selector. Default value: S1 (settable in the interface 'Segment')
			:return: no_of_off_slots: numeric Range: 1 to 9"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SETup:OSLots?')
		return Conversions.str_to_int(response)
