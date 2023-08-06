from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEval:
	"""MultiEval commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiEval", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .MultiEval_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	def get_source(self) -> str:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:SOURce \n
		Snippet: value: str = driver.trigger.multiEval.get_source() \n
		Selects the source of the trigger events. Some values are always available. They are listed below. Depending on the
		installed options, additional values are available. You can query a list of all supported values via TRIGger:...
		:CATalog:SOURce?. \n
			:return: source: string 'Power': power trigger (received RF power)
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:SOURce \n
		Snippet: driver.trigger.multiEval.set_source(source = '1') \n
		Selects the source of the trigger events. Some values are always available. They are listed below. Depending on the
		installed options, additional values are available. You can query a list of all supported values via TRIGger:...
		:CATalog:SOURce?. \n
			:param source: string 'Power': power trigger (received RF power)
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:SOURce {param}')

	def get_threshold(self) -> float or bool:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:THReshold \n
		Snippet: value: float or bool = driver.trigger.multiEval.get_threshold() \n
		Defines the trigger threshold for the power trigger. \n
			:return: power: numeric Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to reference level minus external attenuation)
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:THReshold?')
		return Conversions.str_to_float_or_bool(response)

	def set_threshold(self, power: float or bool) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:THReshold \n
		Snippet: driver.trigger.multiEval.set_threshold(power = 1.0) \n
		Defines the trigger threshold for the power trigger. \n
			:param power: numeric Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to reference level minus external attenuation)
		"""
		param = Conversions.decimal_or_bool_value_to_str(power)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:THReshold {param}')

	def get_timeout(self) -> float or bool:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: value: float or bool = driver.trigger.multiEval.get_timeout() \n
		Selects the maximum time that the measurement waits for a trigger event before it stops in remote control mode or
		indicates a trigger timeout in manual operation mode. \n
			:return: trigger_timeout: numeric | ON | OFF Range: 0.01 s to 167772.15 s Additional parameters: OFF | ON (disables timeout | enables timeout using the previous/default values)
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:TOUT?')
		return Conversions.str_to_float_or_bool(response)

	def set_timeout(self, trigger_timeout: float or bool) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: driver.trigger.multiEval.set_timeout(trigger_timeout = 1.0) \n
		Selects the maximum time that the measurement waits for a trigger event before it stops in remote control mode or
		indicates a trigger timeout in manual operation mode. \n
			:param trigger_timeout: numeric | ON | OFF Range: 0.01 s to 167772.15 s Additional parameters: OFF | ON (disables timeout | enables timeout using the previous/default values)
		"""
		param = Conversions.decimal_or_bool_value_to_str(trigger_timeout)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:MEValuation:TOUT {param}')

	def clone(self) -> 'MultiEval':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEval(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
