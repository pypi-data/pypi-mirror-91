from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AccAddress:
	"""AccAddress commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("accAddress", core, parent)

	def get_low_energy(self) -> str:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:ACCaddress:LENergy \n
		Snippet: value: str = driver.configure.inputSignal.accAddress.get_low_energy() \n
		Specifies the access address of advertiser for standalone LE measurements. \n
			:return: access_address: hex Range: #H0 to #HFFFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:ACCaddress:LENergy?')
		return trim_str_response(response)

	def set_low_energy(self, access_address: str) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:ACCaddress:LENergy \n
		Snippet: driver.configure.inputSignal.accAddress.set_low_energy(access_address = r1) \n
		Specifies the access address of advertiser for standalone LE measurements. \n
			:param access_address: hex Range: #H0 to #HFFFFFFFF
		"""
		param = Conversions.value_to_str(access_address)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:ACCaddress:LENergy {param}')
