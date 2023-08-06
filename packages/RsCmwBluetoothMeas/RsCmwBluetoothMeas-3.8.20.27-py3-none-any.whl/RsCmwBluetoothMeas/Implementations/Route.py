from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal.StructBase import StructBase
from ..Internal.ArgStruct import ArgStruct
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Route:
	"""Route commands group definition. 6 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("route", core, parent)

	@property
	def scenario(self):
		"""scenario commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_scenario'):
			from .Route_.Scenario import Scenario
			self._scenario = Scenario(self._core, self._base)
		return self._scenario

	@property
	def rfSettings(self):
		"""rfSettings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Route_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Scenario: enums.TestScenario: SALone | CSPath SALone: standalone (non-signaling) CSPath: combined signal path
			- Master: str: string Master application for scenario CSPath
			- Rf_Connector: enums.RxConnector: RF connector for the input path
			- Rf_Converter: enums.RxConverter: RX module for the input path"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Scenario', enums.TestScenario),
			ArgStruct.scalar_str('Master'),
			ArgStruct.scalar_enum('Rf_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rf_Converter', enums.RxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Scenario: enums.TestScenario = None
			self.Master: str = None
			self.Rf_Connector: enums.RxConnector = None
			self.Rf_Converter: enums.RxConverter = None

	# noinspection PyTypeChecker
	def get_value(self) -> ValueStruct:
		"""SCPI: ROUTe:BLUetooth:MEASurement<Instance> \n
		Snippet: value: ValueStruct = driver.route.get_value() \n
		Returns the configured routing settings. For possible connector and converter values, see 'Values for RF Path Selection'. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('ROUTe:BLUetooth:MEASurement<Instance>?', self.__class__.ValueStruct())

	def clone(self) -> 'Route':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Route(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
