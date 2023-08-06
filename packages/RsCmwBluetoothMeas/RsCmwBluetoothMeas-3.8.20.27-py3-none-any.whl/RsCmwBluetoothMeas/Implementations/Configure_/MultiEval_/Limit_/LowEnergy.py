from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 35 total commands, 6 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	@property
	def lrange(self):
		"""lrange commands group. 0 Sub-classes, 9 commands."""
		if not hasattr(self, '_lrange'):
			from .LowEnergy_.Lrange import Lrange
			self._lrange = Lrange(self._core, self._base)
		return self._lrange

	@property
	def le2M(self):
		"""le2M commands group. 3 Sub-classes, 7 commands."""
		if not hasattr(self, '_le2M'):
			from .LowEnergy_.Le2M import Le2M
			self._le2M = Le2M(self._core, self._base)
		return self._le2M

	@property
	def le1M(self):
		"""le1M commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_le1M'):
			from .LowEnergy_.Le1M import Le1M
			self._le1M = Le1M(self._core, self._base)
		return self._le1M

	@property
	def daverage(self):
		"""daverage commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_daverage'):
			from .LowEnergy_.Daverage import Daverage
			self._daverage = Daverage(self._core, self._base)
		return self._daverage

	@property
	def dminimum(self):
		"""dminimum commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dminimum'):
			from .LowEnergy_.Dminimum import Dminimum
			self._dminimum = Dminimum(self._core, self._base)
		return self._dminimum

	@property
	def dmaximum(self):
		"""dmaximum commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dmaximum'):
			from .LowEnergy_.Dmaximum import Dmaximum
			self._dmaximum = Dmaximum(self._core, self._base)
		return self._dmaximum

	# noinspection PyTypeChecker
	class DeltaStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Delta_F_2_P_99_P_9: float: numeric Range: 150 kHz to 250 kHz
			- Delta_F_2_P_99_Enabl: bool: OFF | ON Disable/enable limit checking"""
		__meta_args_list = [
			ArgStruct.scalar_float('Delta_F_2_P_99_P_9'),
			ArgStruct.scalar_bool('Delta_F_2_P_99_Enabl')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Delta_F_2_P_99_P_9: float = None
			self.Delta_F_2_P_99_Enabl: bool = None

	def get_delta(self) -> DeltaStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DELTa \n
		Snippet: value: DeltaStruct = driver.configure.multiEval.limit.lowEnergy.get_delta() \n
		Sets/gets the limit for the frequency deviation Δf2 for LE 1M PHY that must be exceeded by 99.9% of the measured samples. \n
			:return: structure: for return value, see the help for DeltaStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DELTa?', self.__class__.DeltaStruct())

	def set_delta(self, value: DeltaStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DELTa \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.set_delta(value = DeltaStruct()) \n
		Sets/gets the limit for the frequency deviation Δf2 for LE 1M PHY that must be exceeded by 99.9% of the measured samples. \n
			:param value: see the help for DeltaStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DELTa', value)

	def clone(self) -> 'LowEnergy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LowEnergy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
