from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputSignal:
	"""InputSignal commands group definition. 45 total commands, 11 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inputSignal", core, parent)

	@property
	def dtMode(self):
		"""dtMode commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtMode'):
			from .InputSignal_.DtMode import DtMode
			self._dtMode = DtMode(self._core, self._base)
		return self._dtMode

	@property
	def cte(self):
		"""cte commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cte'):
			from .InputSignal_.Cte import Cte
			self._cte = Cte(self._core, self._base)
		return self._cte

	@property
	def oslots(self):
		"""oslots commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_oslots'):
			from .InputSignal_.Oslots import Oslots
			self._oslots = Oslots(self._core, self._base)
		return self._oslots

	@property
	def plength(self):
		"""plength commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_plength'):
			from .InputSignal_.Plength import Plength
			self._plength = Plength(self._core, self._base)
		return self._plength

	@property
	def ptype(self):
		"""ptype commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_ptype'):
			from .InputSignal_.Ptype import Ptype
			self._ptype = Ptype(self._core, self._base)
		return self._ptype

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .InputSignal_.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	@property
	def accAddress(self):
		"""accAddress commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_accAddress'):
			from .InputSignal_.AccAddress import AccAddress
			self._accAddress = AccAddress(self._core, self._base)
		return self._accAddress

	@property
	def synWord(self):
		"""synWord commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_synWord'):
			from .InputSignal_.SynWord import SynWord
			self._synWord = SynWord(self._core, self._base)
		return self._synWord

	@property
	def pattern(self):
		"""pattern commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .InputSignal_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def cscheme(self):
		"""cscheme commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cscheme'):
			from .InputSignal_.Cscheme import Cscheme
			self._cscheme = Cscheme(self._core, self._base)
		return self._cscheme

	@property
	def fec(self):
		"""fec commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fec'):
			from .InputSignal_.Fec import Fec
			self._fec = Fec(self._core, self._base)
		return self._fec

	# noinspection PyTypeChecker
	def get_dmode(self) -> enums.AutoManualMode:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DMODe \n
		Snippet: value: enums.AutoManualMode = driver.configure.inputSignal.get_dmode() \n
		Selects an algorithm which the R&S CMW uses to detect the measured burst. \n
			:return: detection_mode: MANual | AUTO
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DMODe?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_dmode(self, detection_mode: enums.AutoManualMode) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DMODe \n
		Snippet: driver.configure.inputSignal.set_dmode(detection_mode = enums.AutoManualMode.AUTO) \n
		Selects an algorithm which the R&S CMW uses to detect the measured burst. \n
			:param detection_mode: MANual | AUTO
		"""
		param = Conversions.enum_scalar_to_str(detection_mode, enums.AutoManualMode)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:DMODe {param}')

	# noinspection PyTypeChecker
	def get_btype(self) -> enums.BurstType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:BTYPe \n
		Snippet: value: enums.BurstType = driver.configure.inputSignal.get_btype() \n
		Specifies the measured burst / packet type.
		For the combined signal path scenario, use CONFigure:BLUetooth:SIGN<i>:CONNection:BTYPe. \n
			:return: burst_type: BR | EDR | LE BR: 'Basic Rate' EDR: 'Enhanced Data Rate' LE: 'Low Energy'
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:BTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BurstType)

	def set_btype(self, burst_type: enums.BurstType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:BTYPe \n
		Snippet: driver.configure.inputSignal.set_btype(burst_type = enums.BurstType.BR) \n
		Specifies the measured burst / packet type.
		For the combined signal path scenario, use CONFigure:BLUetooth:SIGN<i>:CONNection:BTYPe. \n
			:param burst_type: BR | EDR | LE BR: 'Basic Rate' EDR: 'Enhanced Data Rate' LE: 'Low Energy'
		"""
		param = Conversions.enum_scalar_to_str(burst_type, enums.BurstType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:BTYPe {param}')

	def get_nap(self) -> str:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:NAP \n
		Snippet: value: str = driver.configure.inputSignal.get_nap() \n
		Specifies the non-specific address part of the EUT's Bluetooth device address. \n
			:return: bd_address_nap: hex Four-digit hex number Range: #H0 to #HFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:NAP?')
		return trim_str_response(response)

	def set_nap(self, bd_address_nap: str) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:NAP \n
		Snippet: driver.configure.inputSignal.set_nap(bd_address_nap = r1) \n
		Specifies the non-specific address part of the EUT's Bluetooth device address. \n
			:param bd_address_nap: hex Four-digit hex number Range: #H0 to #HFFFF
		"""
		param = Conversions.value_to_str(bd_address_nap)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:NAP {param}')

	def get_uap(self) -> str:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:UAP \n
		Snippet: value: str = driver.configure.inputSignal.get_uap() \n
		Specifies the upper address part of the DUT's Bluetooth device address. \n
			:return: bd_address_uap: hex Two-digit hex number Range: #H0 to #HFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:UAP?')
		return trim_str_response(response)

	def set_uap(self, bd_address_uap: str) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:UAP \n
		Snippet: driver.configure.inputSignal.set_uap(bd_address_uap = r1) \n
		Specifies the upper address part of the DUT's Bluetooth device address. \n
			:param bd_address_uap: hex Two-digit hex number Range: #H0 to #HFF
		"""
		param = Conversions.value_to_str(bd_address_uap)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:UAP {param}')

	def get_lap(self) -> str:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:LAP \n
		Snippet: value: str = driver.configure.inputSignal.get_lap() \n
		Specifies the lower address part of the DUT's Bluetooth device address. \n
			:return: bd_address_lap: hex Six-digit hex number Range: #H0 to #HFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:LAP?')
		return trim_str_response(response)

	def set_lap(self, bd_address_lap: str) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:LAP \n
		Snippet: driver.configure.inputSignal.set_lap(bd_address_lap = r1) \n
		Specifies the lower address part of the DUT's Bluetooth device address. \n
			:param bd_address_lap: hex Six-digit hex number Range: #H0 to #HFFFFFF
		"""
		param = Conversions.value_to_str(bd_address_lap)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:LAP {param}')

	def get_bd_address(self) -> str:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:BDADdress \n
		Snippet: value: str = driver.configure.inputSignal.get_bd_address() \n
		Specifies the Bluetooth device address that the R&S CMW expects the EUT to use to generate its access code. \n
			:return: bd_address: hex 12-digit hex number Range: #H0 to #HFFFFFFFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:BDADdress?')
		return trim_str_response(response)

	def set_bd_address(self, bd_address: str) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:BDADdress \n
		Snippet: driver.configure.inputSignal.set_bd_address(bd_address = r1) \n
		Specifies the Bluetooth device address that the R&S CMW expects the EUT to use to generate its access code. \n
			:param bd_address: hex 12-digit hex number Range: #H0 to #HFFFFFFFFFFFF
		"""
		param = Conversions.value_to_str(bd_address)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:BDADdress {param}')

	def get_asynchronize(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:ASYNchronize \n
		Snippet: value: bool = driver.configure.inputSignal.get_asynchronize() \n
		Disables / enables automatic synchronization to the captured signal for an unspecified Bluetooth device address. \n
			:return: auto_synch: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:ASYNchronize?')
		return Conversions.str_to_bool(response)

	def set_asynchronize(self, auto_synch: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:ASYNchronize \n
		Snippet: driver.configure.inputSignal.set_asynchronize(auto_synch = False) \n
		Disables / enables automatic synchronization to the captured signal for an unspecified Bluetooth device address. \n
			:param auto_synch: OFF | ON
		"""
		param = Conversions.bool_to_str(auto_synch)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:ASYNchronize {param}')

	def clone(self) -> 'InputSignal':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InputSignal(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
