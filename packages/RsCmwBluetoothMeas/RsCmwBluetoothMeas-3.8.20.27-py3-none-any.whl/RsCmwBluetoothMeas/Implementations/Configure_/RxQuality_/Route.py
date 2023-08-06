from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Route:
	"""Route commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("route", core, parent)

	@property
	def usage(self):
		"""usage commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_usage'):
			from .Route_.Usage import Usage
			self._usage = Usage(self._core, self._base)
		return self._usage

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Tx_Connector: enums.TxConnector: RF connector for the output path
			- Rf_Converter: enums.TxConverter: TX module for the output path"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Tx_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Rf_Converter', enums.TxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tx_Connector: enums.TxConnector = None
			self.Rf_Converter: enums.TxConverter = None

	# noinspection PyTypeChecker
	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:ROUTe \n
		Snippet: value: ValueStruct = driver.configure.rxQuality.route.get_value() \n
		Selects the RF output path for the RF signal generated using ARB files. For possible TX module values, see 'Values for RF
		Path Selection'. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:ROUTe?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:ROUTe \n
		Snippet: driver.configure.rxQuality.route.set_value(value = ValueStruct()) \n
		Selects the RF output path for the RF signal generated using ARB files. For possible TX module values, see 'Values for RF
		Path Selection'. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:RXQuality:ROUTe', value)

	def clone(self) -> 'Route':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Route(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
