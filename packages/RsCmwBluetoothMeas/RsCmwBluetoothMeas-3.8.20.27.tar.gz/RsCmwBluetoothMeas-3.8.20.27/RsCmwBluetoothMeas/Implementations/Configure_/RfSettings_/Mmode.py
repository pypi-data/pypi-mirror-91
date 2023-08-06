from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mmode:
	"""Mmode commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mmode", core, parent)

	@property
	def nmode(self):
		"""nmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nmode'):
			from .Mmode_.Nmode import Nmode
			self._nmode = Nmode(self._core, self._base)
		return self._nmode

	# noinspection PyTypeChecker
	def get_value(self) -> enums.MeasureScope:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:MMODe \n
		Snippet: value: enums.MeasureScope = driver.configure.rfSettings.mmode.get_value() \n
		Sets measure mode for BR/EDR test mode in combined signal path scenario during hopping enabled. \n
			:return: measure_mode: ALL | SINGle ALL: multi-evaluation TX measurements on all channels SINGle: multi-evaluation TX measurements on specified channel, see CONFigure:BLUetooth:MEASi:RFSettings
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:MMODe?')
		return Conversions.str_to_scalar_enum(response, enums.MeasureScope)

	def set_value(self, measure_mode: enums.MeasureScope) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:MMODe \n
		Snippet: driver.configure.rfSettings.mmode.set_value(measure_mode = enums.MeasureScope.ALL) \n
		Sets measure mode for BR/EDR test mode in combined signal path scenario during hopping enabled. \n
			:param measure_mode: ALL | SINGle ALL: multi-evaluation TX measurements on all channels SINGle: multi-evaluation TX measurements on specified channel, see CONFigure:BLUetooth:MEASi:RFSettings
		"""
		param = Conversions.enum_scalar_to_str(measure_mode, enums.MeasureScope)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:RFSettings:MMODe {param}')

	def clone(self) -> 'Mmode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mmode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
