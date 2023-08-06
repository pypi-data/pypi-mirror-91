from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy[:LE1M] \n
		Snippet: value: int = driver.configure.inputSignal.oslots.lowEnergy.get_le_1_m() \n
		Specifies the number of unused slots between any two occupied slots or slot sequences. Commands for LE 1M PHY (...:LE1M...
		) and LE 2M PHY (...:LE2M...) are available. \n
			:return: no_of_off_slots: numeric Range: 1 to 9, Unit: Multiplies of 625 µs
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LE1M?')
		return Conversions.str_to_int(response)

	def set_le_1_m(self, no_of_off_slots: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy[:LE1M] \n
		Snippet: driver.configure.inputSignal.oslots.lowEnergy.set_le_1_m(no_of_off_slots = 1) \n
		Specifies the number of unused slots between any two occupied slots or slot sequences. Commands for LE 1M PHY (...:LE1M...
		) and LE 2M PHY (...:LE2M...) are available. \n
			:param no_of_off_slots: numeric Range: 1 to 9, Unit: Multiplies of 625 µs
		"""
		param = Conversions.decimal_value_to_str(no_of_off_slots)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LE1M {param}')

	def get_lrange(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LRANge \n
		Snippet: value: int = driver.configure.inputSignal.oslots.lowEnergy.get_lrange() \n
		No command help available \n
			:return: no_of_off_slots: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LRANge?')
		return Conversions.str_to_int(response)

	def set_lrange(self, no_of_off_slots: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LRANge \n
		Snippet: driver.configure.inputSignal.oslots.lowEnergy.set_lrange(no_of_off_slots = 1) \n
		No command help available \n
			:param no_of_off_slots: No help available
		"""
		param = Conversions.decimal_value_to_str(no_of_off_slots)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LRANge {param}')

	def get_le_2_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LE2M \n
		Snippet: value: int = driver.configure.inputSignal.oslots.lowEnergy.get_le_2_m() \n
		Specifies the number of unused slots between any two occupied slots or slot sequences. Commands for LE 1M PHY (...:LE1M...
		) and LE 2M PHY (...:LE2M...) are available. \n
			:return: no_of_off_slots: numeric Range: 1 to 9, Unit: Multiplies of 625 µs
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LE2M?')
		return Conversions.str_to_int(response)

	def set_le_2_m(self, no_of_off_slots: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LE2M \n
		Snippet: driver.configure.inputSignal.oslots.lowEnergy.set_le_2_m(no_of_off_slots = 1) \n
		Specifies the number of unused slots between any two occupied slots or slot sequences. Commands for LE 1M PHY (...:LE1M...
		) and LE 2M PHY (...:LE2M...) are available. \n
			:param no_of_off_slots: numeric Range: 1 to 9, Unit: Multiplies of 625 µs
		"""
		param = Conversions.decimal_value_to_str(no_of_off_slots)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:OSLots:LENergy:LE2M {param}')
