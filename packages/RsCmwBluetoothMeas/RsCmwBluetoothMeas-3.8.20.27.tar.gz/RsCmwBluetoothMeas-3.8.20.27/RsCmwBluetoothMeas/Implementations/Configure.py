from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from ..Internal.StructBase import StructBase
from ..Internal.ArgStruct import ArgStruct
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 244 total commands, 7 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	@property
	def dtMode(self):
		"""dtMode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtMode'):
			from .Configure_.DtMode import DtMode
			self._dtMode = DtMode(self._core, self._base)
		return self._dtMode

	@property
	def inputSignal(self):
		"""inputSignal commands group. 11 Sub-classes, 7 commands."""
		if not hasattr(self, '_inputSignal'):
			from .Configure_.InputSignal import InputSignal
			self._inputSignal = InputSignal(self._core, self._base)
		return self._inputSignal

	@property
	def comSettings(self):
		"""comSettings commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_comSettings'):
			from .Configure_.ComSettings import ComSettings
			self._comSettings = ComSettings(self._core, self._base)
		return self._comSettings

	@property
	def rxQuality(self):
		"""rxQuality commands group. 5 Sub-classes, 7 commands."""
		if not hasattr(self, '_rxQuality'):
			from .Configure_.RxQuality import RxQuality
			self._rxQuality = RxQuality(self._core, self._base)
		return self._rxQuality

	@property
	def trx(self):
		"""trx commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trx'):
			from .Configure_.Trx import Trx
			self._trx = Trx(self._core, self._base)
		return self._trx

	@property
	def multiEval(self):
		"""multiEval commands group. 12 Sub-classes, 5 commands."""
		if not hasattr(self, '_multiEval'):
			from .Configure_.MultiEval import MultiEval
			self._multiEval = MultiEval(self._core, self._base)
		return self._multiEval

	@property
	def rfSettings(self):
		"""rfSettings commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Configure_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	# noinspection PyTypeChecker
	def get_hw_interface(self) -> enums.HwInterface:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:HWINterface \n
		Snippet: value: enums.HwInterface = driver.configure.get_hw_interface() \n
		Defines the interface used for the control connection between the DUT and the control computer of the R&S CMW100. \n
			:return: hw_interface: NONE | RS232 | USB RS232: USB connection with USB to RS232 adapter NONE: no control via USB to be used USB: direct USB connection
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:HWINterface?')
		return Conversions.str_to_scalar_enum(response, enums.HwInterface)

	def set_hw_interface(self, hw_interface: enums.HwInterface) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:HWINterface \n
		Snippet: driver.configure.set_hw_interface(hw_interface = enums.HwInterface.NONE) \n
		Defines the interface used for the control connection between the DUT and the control computer of the R&S CMW100. \n
			:param hw_interface: NONE | RS232 | USB RS232: USB connection with USB to RS232 adapter NONE: no control via USB to be used USB: direct USB connection
		"""
		param = Conversions.enum_scalar_to_str(hw_interface, enums.HwInterface)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:HWINterface {param}')

	# noinspection PyTypeChecker
	def get_cprotocol(self) -> enums.CommProtocol:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CPRotocol \n
		Snippet: value: enums.CommProtocol = driver.configure.get_cprotocol() \n
		Specifies the communication protocol for direct test mode. \n
			:return: communication_protocol: HCI | TWO HCI or two-wire UART interface
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CPRotocol?')
		return Conversions.str_to_scalar_enum(response, enums.CommProtocol)

	def set_cprotocol(self, communication_protocol: enums.CommProtocol) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CPRotocol \n
		Snippet: driver.configure.set_cprotocol(communication_protocol = enums.CommProtocol.HCI) \n
		Specifies the communication protocol for direct test mode. \n
			:param communication_protocol: HCI | TWO HCI or two-wire UART interface
		"""
		param = Conversions.enum_scalar_to_str(communication_protocol, enums.CommProtocol)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CPRotocol {param}')

	def get_gdelay(self) -> float:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:GDELay \n
		Snippet: value: float = driver.configure.get_gdelay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:GDELay?')
		return Conversions.str_to_float(response)

	def set_gdelay(self, delay: float) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:GDELay \n
		Snippet: driver.configure.set_gdelay(delay = 1.0) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:GDELay {param}')

	# noinspection PyTypeChecker
	def get_cfilter(self) -> enums.FilterWidth:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CFILter \n
		Snippet: value: enums.FilterWidth = driver.configure.get_cfilter() \n
		No command help available \n
			:return: capture_filter: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CFILter?')
		return Conversions.str_to_scalar_enum(response, enums.FilterWidth)

	def set_cfilter(self, capture_filter: enums.FilterWidth) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CFILter \n
		Snippet: driver.configure.set_cfilter(capture_filter = enums.FilterWidth.NARRow) \n
		No command help available \n
			:param capture_filter: No help available
		"""
		param = Conversions.enum_scalar_to_str(capture_filter, enums.FilterWidth)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CFILter {param}')

	def get_othreshold(self) -> float:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:OTHReshold \n
		Snippet: value: float = driver.configure.get_othreshold() \n
		No command help available \n
			:return: overdriven_threshold: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:OTHReshold?')
		return Conversions.str_to_float(response)

	def set_othreshold(self, overdriven_threshold: float) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:OTHReshold \n
		Snippet: driver.configure.set_othreshold(overdriven_threshold = 1.0) \n
		No command help available \n
			:param overdriven_threshold: No help available
		"""
		param = Conversions.decimal_value_to_str(overdriven_threshold)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:OTHReshold {param}')

	# noinspection PyTypeChecker
	class DisplayStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Measurement: enums.DisplayMeasurement: MEV Multi-evaluation measurement
			- View: enums.DisplayView: OVERview | PVTime | DEVM | PDIFference | IQABs | IQDiff | IQERr | FDEViation | SOBW | SACP | SGACp | MODulation | POWer | FRANge | PENCoding OVERview: 'Overview' (BR, EDR, LE) PVTime: 'Power vs Tim'e (BR, EDR, LE) DEVM: 'DEVM' (EDR) PDIFference: 'Phase Differen'ce (EDR) IQABs: 'IQ Constellation Absolute' (EDR) IQDiff: 'IQ Constellation Differentia'l (EDR) IQERr: 'IQ Constellation Error' (EDR) FDEViation: 'Frequency Deviation' (BR, LE) SOBW: 'Spectrum 20 dB Bandwidth' (BR) SACP: 'Spectrum AC'P (BR, LE) SGACp: 'Spectrum Gated ACP' (EDR) MODulation: 'Modulation Scalars' (BR, EDR, LE) POWer: 'Power Scalars' (BR, EDR, LE) FRANge: 'Frequency Rang'e (BR) PENCoding: 'Differential Phase Encoding' (EDR)"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Measurement', enums.DisplayMeasurement),
			ArgStruct.scalar_enum('View', enums.DisplayView)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Measurement: enums.DisplayMeasurement = None
			self.View: enums.DisplayView = None

	# noinspection PyTypeChecker
	def get_display(self) -> DisplayStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:DISPlay \n
		Snippet: value: DisplayStruct = driver.configure.get_display() \n
		Selects the view to be displayed. \n
			:return: structure: for return value, see the help for DisplayStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:DISPlay?', self.__class__.DisplayStruct())

	def set_display(self, value: DisplayStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:DISPlay \n
		Snippet: driver.configure.set_display(value = DisplayStruct()) \n
		Selects the view to be displayed. \n
			:param value: see the help for DisplayStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:DISPlay', value)

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
