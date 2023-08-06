from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEval:
	"""MultiEval commands group definition. 137 total commands, 12 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiEval", core, parent)

	@property
	def measurement(self):
		"""measurement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_measurement'):
			from .MultiEval_.Measurement import Measurement
			self._measurement = Measurement(self._core, self._base)
		return self._measurement

	@property
	def listPy(self):
		"""listPy commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_listPy'):
			from .MultiEval_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	@property
	def malgorithm(self):
		"""malgorithm commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_malgorithm'):
			from .MultiEval_.Malgorithm import Malgorithm
			self._malgorithm = Malgorithm(self._core, self._base)
		return self._malgorithm

	@property
	def limit(self):
		"""limit commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_limit'):
			from .MultiEval_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .MultiEval_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	@property
	def edrate(self):
		"""edrate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_edrate'):
			from .MultiEval_.Edrate import Edrate
			self._edrate = Edrate(self._core, self._base)
		return self._edrate

	@property
	def brate(self):
		"""brate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_brate'):
			from .MultiEval_.Brate import Brate
			self._brate = Brate(self._core, self._base)
		return self._brate

	@property
	def scount(self):
		"""scount commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_scount'):
			from .MultiEval_.Scount import Scount
			self._scount = Scount(self._core, self._base)
		return self._scount

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 17 commands."""
		if not hasattr(self, '_result'):
			from .MultiEval_.Result import Result
			self._result = Result(self._core, self._base)
		return self._result

	@property
	def sacp(self):
		"""sacp commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sacp'):
			from .MultiEval_.Sacp import Sacp
			self._sacp = Sacp(self._core, self._base)
		return self._sacp

	@property
	def frange(self):
		"""frange commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frange'):
			from .MultiEval_.Frange import Frange
			self._frange = Frange(self._core, self._base)
		return self._frange

	@property
	def sgacp(self):
		"""sgacp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sgacp'):
			from .MultiEval_.Sgacp import Sgacp
			self._sgacp = Sgacp(self._core, self._base)
		return self._sgacp

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: value: float = driver.configure.multiEval.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually ([ON | OFF] key or [RESTART | STOP] key) .
		When the measurement has completed the first measurement cycle (first single shot) , the statistical depth is reached and
		the timer is reset. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped. The measurement state changes to RDY. The reliability indicator is set to 1, indicating that a measurement
		timeout occurred. Still running READ, FETCh or CALCulate commands are completed, returning the available results.
		At least for some results, there are no values at all or the statistical depth has not been reached. A timeout of 0 s
		corresponds to an infinite measurement timeout. \n
			:return: timeout: numeric Unit: s
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, timeout: float) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: driver.configure.multiEval.set_timeout(timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually ([ON | OFF] key or [RESTART | STOP] key) .
		When the measurement has completed the first measurement cycle (first single shot) , the statistical depth is reached and
		the timer is reset. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped. The measurement state changes to RDY. The reliability indicator is set to 1, indicating that a measurement
		timeout occurred. Still running READ, FETCh or CALCulate commands are completed, returning the available results.
		At least for some results, there are no values at all or the statistical depth has not been reached. A timeout of 0 s
		corresponds to an infinite measurement timeout. \n
			:param timeout: numeric Unit: s
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:TOUT {param}')

	def get_mo_exception(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:MOEXception \n
		Snippet: value: bool = driver.configure.multiEval.get_mo_exception() \n
		Specifies whether measurement results that are identified as faulty or inaccurate are rejected. \n
			:return: meas_on_exception: OFF | ON ON: Results are never rejected OFF: Faulty results are rejected
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:MOEXception?')
		return Conversions.str_to_bool(response)

	def set_mo_exception(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:MOEXception \n
		Snippet: driver.configure.multiEval.set_mo_exception(meas_on_exception = False) \n
		Specifies whether measurement results that are identified as faulty or inaccurate are rejected. \n
			:param meas_on_exception: OFF | ON ON: Results are never rejected OFF: Faulty results are rejected
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:MOEXception {param}')

	# noinspection PyTypeChecker
	def get_scondition(self) -> enums.StopCondition:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:SCONdition \n
		Snippet: value: enums.StopCondition = driver.configure.multiEval.get_scondition() \n
		Qualifies whether the measurement is stopped after a failed limit check or continued. SLFail means that the measurement
		is stopped and reaches the RDY state when one of the results exceeds the limits. \n
			:return: stop_condition: NONE | SLFail NONE: Continue measurement irrespective of the limit check SLFail: Stop measurement on limit failure
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:SCONdition?')
		return Conversions.str_to_scalar_enum(response, enums.StopCondition)

	def set_scondition(self, stop_condition: enums.StopCondition) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:SCONdition \n
		Snippet: driver.configure.multiEval.set_scondition(stop_condition = enums.StopCondition.NONE) \n
		Qualifies whether the measurement is stopped after a failed limit check or continued. SLFail means that the measurement
		is stopped and reaches the RDY state when one of the results exceeds the limits. \n
			:param stop_condition: NONE | SLFail NONE: Continue measurement irrespective of the limit check SLFail: Stop measurement on limit failure
		"""
		param = Conversions.enum_scalar_to_str(stop_condition, enums.StopCondition)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:SCONdition {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.multiEval.get_repetition() \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot: Single-shot measurement CONTinuous: Continuous measurement
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:REPetition \n
		Snippet: driver.configure.multiEval.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot: Single-shot measurement CONTinuous: Continuous measurement
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:REPetition {param}')

	# noinspection PyTypeChecker
	class SynchroniseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Min_No_Valid_Bursts: int: No parameter help available
			- Syn_Check_Filter: int: No parameter help available
			- Max_Invalid_Burst: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Min_No_Valid_Bursts'),
			ArgStruct.scalar_int('Syn_Check_Filter'),
			ArgStruct.scalar_int('Max_Invalid_Burst')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Min_No_Valid_Bursts: int = None
			self.Syn_Check_Filter: int = None
			self.Max_Invalid_Burst: int = None

	def get_synchronise(self) -> SynchroniseStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:SYNChronise \n
		Snippet: value: SynchroniseStruct = driver.configure.multiEval.get_synchronise() \n
		No command help available \n
			:return: structure: for return value, see the help for SynchroniseStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:SYNChronise?', self.__class__.SynchroniseStruct())

	def set_synchronise(self, value: SynchroniseStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:SYNChronise \n
		Snippet: driver.configure.multiEval.set_synchronise(value = SynchroniseStruct()) \n
		No command help available \n
			:param value: see the help for SynchroniseStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:SYNChronise', value)

	def clone(self) -> 'MultiEval':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEval(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
