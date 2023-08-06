from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_lrange(self) -> enums.CodingScheme:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:FEC:LENergy:LRANge \n
		Snippet: value: enums.CodingScheme = driver.configure.inputSignal.fec.lowEnergy.get_lrange() \n
		Defines S coding for LE coded PHY according to the core specification version 5.0 for Bluetooth wireless technology. For
		the combined signal path scenario, use CONFigure:BLUetooth:SIGN<i>:CONNection:FEC:LENergy:LRANge \n
			:return: coding_scheme: S8 | S2 Coding S = 8 or S = 2
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:FEC:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.CodingScheme)

	def set_lrange(self, coding_scheme: enums.CodingScheme) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:FEC:LENergy:LRANge \n
		Snippet: driver.configure.inputSignal.fec.lowEnergy.set_lrange(coding_scheme = enums.CodingScheme.S2) \n
		Defines S coding for LE coded PHY according to the core specification version 5.0 for Bluetooth wireless technology. For
		the combined signal path scenario, use CONFigure:BLUetooth:SIGN<i>:CONNection:FEC:LENergy:LRANge \n
			:param coding_scheme: S8 | S2 Coding S = 8 or S = 2
		"""
		param = Conversions.enum_scalar_to_str(coding_scheme, enums.CodingScheme)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:FEC:LENergy:LRANge {param}')
