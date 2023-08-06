from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 34 total commands, 2 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	@property
	def segment(self):
		"""segment commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_segment'):
			from .ListPy_.Segment import Segment
			self._segment = Segment(self._core, self._base)
		return self._segment

	@property
	def singleCmw(self):
		"""singleCmw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_singleCmw'):
			from .ListPy_.SingleCmw import SingleCmw
			self._singleCmw = SingleCmw(self._core, self._base)
		return self._singleCmw

	def get_count(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:COUNt \n
		Snippet: value: int = driver.configure.multiEval.listPy.get_count() \n
		Defines the number of segments in the entire measurement interval. \n
			:return: segments: numeric Range: 1 to 48
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, segments: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:COUNt \n
		Snippet: driver.configure.multiEval.listPy.set_count(segments = 1) \n
		Defines the number of segments in the entire measurement interval. \n
			:param segments: numeric Range: 1 to 48
		"""
		param = Conversions.decimal_value_to_str(segments)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:COUNt {param}')

	# noinspection PyTypeChecker
	def get_malgorithm(self) -> enums.PatternIndependent:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:MALGorithm \n
		Snippet: value: enums.PatternIndependent = driver.configure.multiEval.listPy.get_malgorithm() \n
		No command help available \n
			:return: pattern_independent: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:MALGorithm?')
		return Conversions.str_to_scalar_enum(response, enums.PatternIndependent)

	def set_malgorithm(self, pattern_independent: enums.PatternIndependent) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:MALGorithm \n
		Snippet: driver.configure.multiEval.listPy.set_malgorithm(pattern_independent = enums.PatternIndependent.PINDependent) \n
		No command help available \n
			:param pattern_independent: No help available
		"""
		param = Conversions.enum_scalar_to_str(pattern_independent, enums.PatternIndependent)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST:MALGorithm {param}')

	def get_value(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST \n
		Snippet: value: bool = driver.configure.multiEval.listPy.get_value() \n
		Enables or disables the list mode. \n
			:return: enable: OFF | ON OFF: disable list mode ON: enable list mode
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST?')
		return Conversions.str_to_bool(response)

	def set_value(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST \n
		Snippet: driver.configure.multiEval.listPy.set_value(enable = False) \n
		Enables or disables the list mode. \n
			:param enable: OFF | ON OFF: disable list mode ON: enable list mode
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIST {param}')

	def clone(self) -> 'ListPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ListPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
