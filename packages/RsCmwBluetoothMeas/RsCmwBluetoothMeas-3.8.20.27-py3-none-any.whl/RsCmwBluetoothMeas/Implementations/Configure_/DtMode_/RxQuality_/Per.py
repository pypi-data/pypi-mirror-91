from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Per:
	"""Per commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("per", core, parent)

	def get_level(self) -> float:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LEVel \n
		Snippet: value: float = driver.configure.dtMode.rxQuality.per.get_level() \n
		Sets the Tx level of ARB generator. \n
			:return: level: numeric
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LEVel \n
		Snippet: driver.configure.dtMode.rxQuality.per.set_level(level = 1.0) \n
		Sets the Tx level of ARB generator. \n
			:param level: numeric
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:DTMode:RXQuality:PER:LEVel {param}')
