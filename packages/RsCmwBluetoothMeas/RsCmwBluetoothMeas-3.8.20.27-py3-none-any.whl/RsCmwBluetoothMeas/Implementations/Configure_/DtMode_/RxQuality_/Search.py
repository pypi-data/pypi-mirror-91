from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Search:
	"""Search commands group definition. 8 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("search", core, parent)

	@property
	def rintegrity(self):
		"""rintegrity commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rintegrity'):
			from .Search_.Rintegrity import Rintegrity
			self._rintegrity = Rintegrity(self._core, self._base)
		return self._rintegrity

	@property
	def limit(self):
		"""limit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Search_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	def get_start_level(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:SEARch:STARtlevel \n
		Snippet: value: float or bool = driver.configure.dtMode.rxQuality.search.get_start_level() \n
		Specifies the initial Tx power for the LE search iteration of PER search measurements with ARB generator. \n
			:return: start_level: numeric Range: -100 dBm to 0 dBm
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:SEARch:STARtlevel?')
		return Conversions.str_to_float_or_bool(response)

	def set_start_level(self, start_level: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:SEARch:STARtlevel \n
		Snippet: driver.configure.dtMode.rxQuality.search.set_start_level(start_level = 1.0) \n
		Specifies the initial Tx power for the LE search iteration of PER search measurements with ARB generator. \n
			:param start_level: numeric Range: -100 dBm to 0 dBm
		"""
		param = Conversions.decimal_or_bool_value_to_str(start_level)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:SEARch:STARtlevel {param}')

	def get_step(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:SEARch:STEP \n
		Snippet: value: float or bool = driver.configure.dtMode.rxQuality.search.get_step() \n
		Specifies the power step for the LE search iteration of PER search measurements with ARB generator. \n
			:return: level_step: numeric Range: 0.01 dB to 5 dB
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:SEARch:STEP?')
		return Conversions.str_to_float_or_bool(response)

	def set_step(self, level_step: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:SEARch:STEP \n
		Snippet: driver.configure.dtMode.rxQuality.search.set_step(level_step = 1.0) \n
		Specifies the power step for the LE search iteration of PER search measurements with ARB generator. \n
			:param level_step: numeric Range: 0.01 dB to 5 dB
		"""
		param = Conversions.decimal_or_bool_value_to_str(level_step)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:SEARch:STEP {param}')

	def clone(self) -> 'Search':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Search(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
