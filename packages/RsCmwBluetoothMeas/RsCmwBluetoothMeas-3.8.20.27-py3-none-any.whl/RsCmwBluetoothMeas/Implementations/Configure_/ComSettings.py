from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ComSettings:
	"""ComSettings commands group definition. 7 total commands, 1 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("comSettings", core, parent)

	@property
	def ports(self):
		"""ports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ports'):
			from .ComSettings_.Ports import Ports
			self._ports = Ports(self._core, self._base)
		return self._ports

	def get_com_port(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:COMPort \n
		Snippet: value: int = driver.configure.comSettings.get_com_port() \n
		Specifies the virtual COM port of the R&S CMW100 control computer to be used for USB connection with USB to RS232 adapter. \n
			:return: no: integer The number of a virtual COM port
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:COMPort?')
		return Conversions.str_to_int(response)

	def set_com_port(self, no: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:COMPort \n
		Snippet: driver.configure.comSettings.set_com_port(no = 1) \n
		Specifies the virtual COM port of the R&S CMW100 control computer to be used for USB connection with USB to RS232 adapter. \n
			:param no: integer The number of a virtual COM port
		"""
		param = Conversions.decimal_value_to_str(no)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:COMPort {param}')

	# noinspection PyTypeChecker
	def get_baudrate(self) -> enums.BaudRate:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:BAUDrate \n
		Snippet: value: enums.BaudRate = driver.configure.comSettings.get_baudrate() \n
		Specifies the transmission parameters of serial connection. \n
			:return: baud_rate: B110 | B300 | B600 | B12K | B24K | B48K | B96K | B14K | B19K | B28K | B38K | B57K | B115k | B234k | B460k | B500k | B576k | B921k | B1M | B1M5 | B2M | B3M | B3M5 | B4M Data transmission rate in symbol: 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 2000000, 3000000, 3500000, 4000000
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:BAUDrate?')
		return Conversions.str_to_scalar_enum(response, enums.BaudRate)

	def set_baudrate(self, baud_rate: enums.BaudRate) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:BAUDrate \n
		Snippet: driver.configure.comSettings.set_baudrate(baud_rate = enums.BaudRate.B110) \n
		Specifies the transmission parameters of serial connection. \n
			:param baud_rate: B110 | B300 | B600 | B12K | B24K | B48K | B96K | B14K | B19K | B28K | B38K | B57K | B115k | B234k | B460k | B500k | B576k | B921k | B1M | B1M5 | B2M | B3M | B3M5 | B4M Data transmission rate in symbol: 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 2000000, 3000000, 3500000, 4000000
		"""
		param = Conversions.enum_scalar_to_str(baud_rate, enums.BaudRate)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:BAUDrate {param}')

	# noinspection PyTypeChecker
	def get_stop_bits(self) -> enums.StopBits:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:STOPbits \n
		Snippet: value: enums.StopBits = driver.configure.comSettings.get_stop_bits() \n
		Specifies the transmission parameters of serial connection. \n
			:return: stop_bits: S1 | S2 Number of bits used for stop indication
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:STOPbits?')
		return Conversions.str_to_scalar_enum(response, enums.StopBits)

	def set_stop_bits(self, stop_bits: enums.StopBits) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:STOPbits \n
		Snippet: driver.configure.comSettings.set_stop_bits(stop_bits = enums.StopBits.S1) \n
		Specifies the transmission parameters of serial connection. \n
			:param stop_bits: S1 | S2 Number of bits used for stop indication
		"""
		param = Conversions.enum_scalar_to_str(stop_bits, enums.StopBits)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:STOPbits {param}')

	# noinspection PyTypeChecker
	def get_parity(self) -> enums.Parity:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:PARity \n
		Snippet: value: enums.Parity = driver.configure.comSettings.get_parity() \n
		Specifies the transmission parameters of serial connection. \n
			:return: parity: NONE | ODD | EVEN Number of parity bits
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:PARity?')
		return Conversions.str_to_scalar_enum(response, enums.Parity)

	def set_parity(self, parity: enums.Parity) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:PARity \n
		Snippet: driver.configure.comSettings.set_parity(parity = enums.Parity.EVEN) \n
		Specifies the transmission parameters of serial connection. \n
			:param parity: NONE | ODD | EVEN Number of parity bits
		"""
		param = Conversions.enum_scalar_to_str(parity, enums.Parity)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:PARity {param}')

	# noinspection PyTypeChecker
	def get_protocol(self) -> enums.Protocol:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:PROTocol \n
		Snippet: value: enums.Protocol = driver.configure.comSettings.get_protocol() \n
		Specifies the transmission parameters of serial connection. \n
			:return: protocol: XONXoff | CTSRts | NONE Transmit flow control X-ON/X-OFF, RFR/CTS, or none
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:PROTocol?')
		return Conversions.str_to_scalar_enum(response, enums.Protocol)

	def set_protocol(self, protocol: enums.Protocol) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:PROTocol \n
		Snippet: driver.configure.comSettings.set_protocol(protocol = enums.Protocol.CTSRts) \n
		Specifies the transmission parameters of serial connection. \n
			:param protocol: XONXoff | CTSRts | NONE Transmit flow control X-ON/X-OFF, RFR/CTS, or none
		"""
		param = Conversions.enum_scalar_to_str(protocol, enums.Protocol)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:PROTocol {param}')

	# noinspection PyTypeChecker
	def get_dbits(self) -> enums.DataBits:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:DBITs \n
		Snippet: value: enums.DataBits = driver.configure.comSettings.get_dbits() \n
		No command help available \n
			:return: data_bits: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:DBITs?')
		return Conversions.str_to_scalar_enum(response, enums.DataBits)

	def set_dbits(self, data_bits: enums.DataBits) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:DBITs \n
		Snippet: driver.configure.comSettings.set_dbits(data_bits = enums.DataBits.D7) \n
		No command help available \n
			:param data_bits: No help available
		"""
		param = Conversions.enum_scalar_to_str(data_bits, enums.DataBits)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:COMSettings:DBITs {param}')

	def clone(self) -> 'ComSettings':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ComSettings(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
