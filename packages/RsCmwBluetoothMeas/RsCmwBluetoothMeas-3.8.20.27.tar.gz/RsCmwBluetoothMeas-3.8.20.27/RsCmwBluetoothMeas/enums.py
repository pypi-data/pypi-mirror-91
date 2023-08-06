from enum import Enum


# noinspection SpellCheckingInspection
class AddressType(Enum):
	"""2 Members, PUBLic ... RANDom"""
	PUBLic = 0
	RANDom = 1


# noinspection SpellCheckingInspection
class AutoManualMode(Enum):
	"""2 Members, AUTO ... MANual"""
	AUTO = 0
	MANual = 1


# noinspection SpellCheckingInspection
class BaudRate(Enum):
	"""24 Members, B110 ... B96K"""
	B110 = 0
	B115k = 1
	B12K = 2
	B14K = 3
	B19K = 4
	B1M = 5
	B1M5 = 6
	B234k = 7
	B24K = 8
	B28K = 9
	B2M = 10
	B300 = 11
	B38K = 12
	B3M = 13
	B3M5 = 14
	B460k = 15
	B48K = 16
	B4M = 17
	B500k = 18
	B576k = 19
	B57K = 20
	B600 = 21
	B921k = 22
	B96K = 23


# noinspection SpellCheckingInspection
class BrEdrChannelsRange(Enum):
	"""2 Members, CH21 ... CH79"""
	CH21 = 0
	CH79 = 1


# noinspection SpellCheckingInspection
class BrPacketType(Enum):
	"""3 Members, DH1 ... DH5"""
	DH1 = 0
	DH3 = 1
	DH5 = 2


# noinspection SpellCheckingInspection
class BurstType(Enum):
	"""3 Members, BR ... LE"""
	BR = 0
	EDR = 1
	LE = 2


# noinspection SpellCheckingInspection
class CmwSingleConnector(Enum):
	"""48 Members, R11 ... RB8"""
	R11 = 0
	R12 = 1
	R13 = 2
	R14 = 3
	R15 = 4
	R16 = 5
	R17 = 6
	R18 = 7
	R21 = 8
	R22 = 9
	R23 = 10
	R24 = 11
	R25 = 12
	R26 = 13
	R27 = 14
	R28 = 15
	R31 = 16
	R32 = 17
	R33 = 18
	R34 = 19
	R35 = 20
	R36 = 21
	R37 = 22
	R38 = 23
	R41 = 24
	R42 = 25
	R43 = 26
	R44 = 27
	R45 = 28
	R46 = 29
	R47 = 30
	R48 = 31
	RA1 = 32
	RA2 = 33
	RA3 = 34
	RA4 = 35
	RA5 = 36
	RA6 = 37
	RA7 = 38
	RA8 = 39
	RB1 = 40
	RB2 = 41
	RB3 = 42
	RB4 = 43
	RB5 = 44
	RB6 = 45
	RB7 = 46
	RB8 = 47


# noinspection SpellCheckingInspection
class CodingScheme(Enum):
	"""2 Members, S2 ... S8"""
	S2 = 0
	S8 = 1


# noinspection SpellCheckingInspection
class CommProtocol(Enum):
	"""2 Members, HCI ... TWO"""
	HCI = 0
	TWO = 1


# noinspection SpellCheckingInspection
class CtePacketType(Enum):
	"""5 Members, AOA1us ... AOD2us"""
	AOA1us = 0
	AOA2us = 1
	AOAus = 2
	AOD1us = 3
	AOD2us = 4


# noinspection SpellCheckingInspection
class DataBits(Enum):
	"""2 Members, D7 ... D8"""
	D7 = 0
	D8 = 1


# noinspection SpellCheckingInspection
class DetectedPatternType(Enum):
	"""4 Members, ALTernating ... P44"""
	ALTernating = 0
	OTHer = 1
	P11 = 2
	P44 = 3


# noinspection SpellCheckingInspection
class DisplayMeasurement(Enum):
	"""1 Members, MEV ... MEV"""
	MEV = 0


# noinspection SpellCheckingInspection
class DisplayView(Enum):
	"""15 Members, DEVM ... SOBW"""
	DEVM = 0
	FDEViation = 1
	FRANge = 2
	IQABs = 3
	IQDiff = 4
	IQERr = 5
	MODulation = 6
	OVERview = 7
	PDIFference = 8
	PENCoding = 9
	POWer = 10
	PVTime = 11
	SACP = 12
	SGACp = 13
	SOBW = 14


# noinspection SpellCheckingInspection
class EdrPacketType(Enum):
	"""6 Members, E21P ... E35P"""
	E21P = 0
	E23P = 1
	E25P = 2
	E31P = 3
	E33P = 4
	E35P = 5


# noinspection SpellCheckingInspection
class FilterWidth(Enum):
	"""2 Members, NARRow ... WIDE"""
	NARRow = 0
	WIDE = 1


# noinspection SpellCheckingInspection
class HwInterface(Enum):
	"""3 Members, NONE ... USB"""
	NONE = 0
	RS232 = 1
	USB = 2


# noinspection SpellCheckingInspection
class LeChannelsRange(Enum):
	"""2 Members, CH10 ... CH40"""
	CH10 = 0
	CH40 = 1


# noinspection SpellCheckingInspection
class LePacketType(Enum):
	"""3 Members, ADVertiser ... RFPHytest"""
	ADVertiser = 0
	RFCTe = 1
	RFPHytest = 2


# noinspection SpellCheckingInspection
class LePatternType(Enum):
	"""3 Members, OTHer ... P44"""
	OTHer = 0
	P11 = 1
	P44 = 2


# noinspection SpellCheckingInspection
class LePhysicalType(Enum):
	"""3 Members, LE1M ... LELR"""
	LE1M = 0
	LE2M = 1
	LELR = 2


# noinspection SpellCheckingInspection
class LeRangePaternType(Enum):
	"""6 Members, ALL0 ... PRBS9"""
	ALL0 = 0
	ALL1 = 1
	OTHer = 2
	P11 = 3
	P44 = 4
	PRBS9 = 5


# noinspection SpellCheckingInspection
class LeSymolTimeError(Enum):
	"""3 Members, NEG50 ... POS50"""
	NEG50 = 0
	OFF = 1
	POS50 = 2


# noinspection SpellCheckingInspection
class LogCategory(Enum):
	"""4 Members, CONTinue ... WARNing"""
	CONTinue = 0
	ERRor = 1
	INFO = 2
	WARNing = 3


# noinspection SpellCheckingInspection
class MeasureScope(Enum):
	"""2 Members, ALL ... SINGle"""
	ALL = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class MevPatternType(Enum):
	"""5 Members, ALL1 ... P44"""
	ALL1 = 0
	ALTernating = 1
	OTHer = 2
	P11 = 3
	P44 = 4


# noinspection SpellCheckingInspection
class ParameterSetMode(Enum):
	"""2 Members, GLOBal ... LIST"""
	GLOBal = 0
	LIST = 1


# noinspection SpellCheckingInspection
class Parity(Enum):
	"""3 Members, EVEN ... ODD"""
	EVEN = 0
	NONE = 1
	ODD = 2


# noinspection SpellCheckingInspection
class PatternIndependent(Enum):
	"""2 Members, PINDependent ... SPECconform"""
	PINDependent = 0
	SPECconform = 1


# noinspection SpellCheckingInspection
class PatternType(Enum):
	"""5 Members, ALL0 ... PRBS9"""
	ALL0 = 0
	ALL1 = 1
	P11 = 2
	P44 = 3
	PRBS9 = 4


# noinspection SpellCheckingInspection
class PayloadLength(Enum):
	"""2 Members, _255 ... _37"""
	_255 = 0
	_37 = 1


# noinspection SpellCheckingInspection
class PduType(Enum):
	"""7 Members, ADVDirect ... SCRSp"""
	ADVDirect = 0
	ADVind = 1
	ADVNonconn = 2
	ADVScan = 3
	CONReq = 4
	SCReq = 5
	SCRSp = 6


# noinspection SpellCheckingInspection
class Protocol(Enum):
	"""3 Members, CTSRts ... XONXoff"""
	CTSRts = 0
	NONE = 1
	XONXoff = 2


# noinspection SpellCheckingInspection
class Repeat(Enum):
	"""2 Members, CONTinuous ... SINGleshot"""
	CONTinuous = 0
	SINGleshot = 1


# noinspection SpellCheckingInspection
class ResourceState(Enum):
	"""8 Members, ACTive ... RUN"""
	ACTive = 0
	ADJusted = 1
	INValid = 2
	OFF = 3
	PENDing = 4
	QUEued = 5
	RDY = 6
	RUN = 7


# noinspection SpellCheckingInspection
class Result(Enum):
	"""2 Members, FAIL ... PASS"""
	FAIL = 0
	PASS = 1


# noinspection SpellCheckingInspection
class ResultStatus2(Enum):
	"""10 Members, DC ... ULEU"""
	DC = 0
	INV = 1
	NAV = 2
	NCAP = 3
	OFF = 4
	OFL = 5
	OK = 6
	UFL = 7
	ULEL = 8
	ULEU = 9


# noinspection SpellCheckingInspection
class RxConnector(Enum):
	"""154 Members, I11I ... RH8"""
	I11I = 0
	I13I = 1
	I15I = 2
	I17I = 3
	I21I = 4
	I23I = 5
	I25I = 6
	I27I = 7
	I31I = 8
	I33I = 9
	I35I = 10
	I37I = 11
	I41I = 12
	I43I = 13
	I45I = 14
	I47I = 15
	IF1 = 16
	IF2 = 17
	IF3 = 18
	IQ1I = 19
	IQ3I = 20
	IQ5I = 21
	IQ7I = 22
	R11 = 23
	R11C = 24
	R12 = 25
	R12C = 26
	R12I = 27
	R13 = 28
	R13C = 29
	R14 = 30
	R14C = 31
	R14I = 32
	R15 = 33
	R16 = 34
	R17 = 35
	R18 = 36
	R21 = 37
	R21C = 38
	R22 = 39
	R22C = 40
	R22I = 41
	R23 = 42
	R23C = 43
	R24 = 44
	R24C = 45
	R24I = 46
	R25 = 47
	R26 = 48
	R27 = 49
	R28 = 50
	R31 = 51
	R31C = 52
	R32 = 53
	R32C = 54
	R32I = 55
	R33 = 56
	R33C = 57
	R34 = 58
	R34C = 59
	R34I = 60
	R35 = 61
	R36 = 62
	R37 = 63
	R38 = 64
	R41 = 65
	R41C = 66
	R42 = 67
	R42C = 68
	R42I = 69
	R43 = 70
	R43C = 71
	R44 = 72
	R44C = 73
	R44I = 74
	R45 = 75
	R46 = 76
	R47 = 77
	R48 = 78
	RA1 = 79
	RA2 = 80
	RA3 = 81
	RA4 = 82
	RA5 = 83
	RA6 = 84
	RA7 = 85
	RA8 = 86
	RB1 = 87
	RB2 = 88
	RB3 = 89
	RB4 = 90
	RB5 = 91
	RB6 = 92
	RB7 = 93
	RB8 = 94
	RC1 = 95
	RC2 = 96
	RC3 = 97
	RC4 = 98
	RC5 = 99
	RC6 = 100
	RC7 = 101
	RC8 = 102
	RD1 = 103
	RD2 = 104
	RD3 = 105
	RD4 = 106
	RD5 = 107
	RD6 = 108
	RD7 = 109
	RD8 = 110
	RE1 = 111
	RE2 = 112
	RE3 = 113
	RE4 = 114
	RE5 = 115
	RE6 = 116
	RE7 = 117
	RE8 = 118
	RF1 = 119
	RF1C = 120
	RF2 = 121
	RF2C = 122
	RF2I = 123
	RF3 = 124
	RF3C = 125
	RF4 = 126
	RF4C = 127
	RF4I = 128
	RF5 = 129
	RF5C = 130
	RF6 = 131
	RF6C = 132
	RF7 = 133
	RF8 = 134
	RFAC = 135
	RFBC = 136
	RFBI = 137
	RG1 = 138
	RG2 = 139
	RG3 = 140
	RG4 = 141
	RG5 = 142
	RG6 = 143
	RG7 = 144
	RG8 = 145
	RH1 = 146
	RH2 = 147
	RH3 = 148
	RH4 = 149
	RH5 = 150
	RH6 = 151
	RH7 = 152
	RH8 = 153


# noinspection SpellCheckingInspection
class RxConverter(Enum):
	"""40 Members, IRX1 ... RX44"""
	IRX1 = 0
	IRX11 = 1
	IRX12 = 2
	IRX13 = 3
	IRX14 = 4
	IRX2 = 5
	IRX21 = 6
	IRX22 = 7
	IRX23 = 8
	IRX24 = 9
	IRX3 = 10
	IRX31 = 11
	IRX32 = 12
	IRX33 = 13
	IRX34 = 14
	IRX4 = 15
	IRX41 = 16
	IRX42 = 17
	IRX43 = 18
	IRX44 = 19
	RX1 = 20
	RX11 = 21
	RX12 = 22
	RX13 = 23
	RX14 = 24
	RX2 = 25
	RX21 = 26
	RX22 = 27
	RX23 = 28
	RX24 = 29
	RX3 = 30
	RX31 = 31
	RX32 = 32
	RX33 = 33
	RX34 = 34
	RX4 = 35
	RX41 = 36
	RX42 = 37
	RX43 = 38
	RX44 = 39


# noinspection SpellCheckingInspection
class RxQualityMeasMode(Enum):
	"""3 Members, PER ... SPOT"""
	PER = 0
	SENS = 1
	SPOT = 2


# noinspection SpellCheckingInspection
class SegmentPacketType(Enum):
	"""11 Members, ADVertiser ... RFPHytest"""
	ADVertiser = 0
	DH1 = 1
	DH3 = 2
	DH5 = 3
	E21P = 4
	E23P = 5
	E25P = 6
	E31P = 7
	E33P = 8
	E35P = 9
	RFPHytest = 10


# noinspection SpellCheckingInspection
class StopBits(Enum):
	"""2 Members, S1 ... S2"""
	S1 = 0
	S2 = 1


# noinspection SpellCheckingInspection
class StopCondition(Enum):
	"""2 Members, NONE ... SLFail"""
	NONE = 0
	SLFail = 1


# noinspection SpellCheckingInspection
class TestScenario(Enum):
	"""3 Members, CSPath ... UNDefined"""
	CSPath = 0
	SALone = 1
	UNDefined = 2


# noinspection SpellCheckingInspection
class TransmitPatternType(Enum):
	"""2 Members, ALL1 ... OTHer"""
	ALL1 = 0
	OTHer = 1


# noinspection SpellCheckingInspection
class TxConnector(Enum):
	"""77 Members, I12O ... RH18"""
	I12O = 0
	I14O = 1
	I16O = 2
	I18O = 3
	I22O = 4
	I24O = 5
	I26O = 6
	I28O = 7
	I32O = 8
	I34O = 9
	I36O = 10
	I38O = 11
	I42O = 12
	I44O = 13
	I46O = 14
	I48O = 15
	IF1 = 16
	IF2 = 17
	IF3 = 18
	IQ2O = 19
	IQ4O = 20
	IQ6O = 21
	IQ8O = 22
	R118 = 23
	R1183 = 24
	R1184 = 25
	R11C = 26
	R11O = 27
	R11O3 = 28
	R11O4 = 29
	R12C = 30
	R13C = 31
	R13O = 32
	R14C = 33
	R214 = 34
	R218 = 35
	R21C = 36
	R21O = 37
	R22C = 38
	R23C = 39
	R23O = 40
	R24C = 41
	R258 = 42
	R318 = 43
	R31C = 44
	R31O = 45
	R32C = 46
	R33C = 47
	R33O = 48
	R34C = 49
	R418 = 50
	R41C = 51
	R41O = 52
	R42C = 53
	R43C = 54
	R43O = 55
	R44C = 56
	RA18 = 57
	RB14 = 58
	RB18 = 59
	RC18 = 60
	RD18 = 61
	RE18 = 62
	RF18 = 63
	RF1C = 64
	RF1O = 65
	RF2C = 66
	RF3C = 67
	RF3O = 68
	RF4C = 69
	RF5C = 70
	RF6C = 71
	RFAC = 72
	RFAO = 73
	RFBC = 74
	RG18 = 75
	RH18 = 76


# noinspection SpellCheckingInspection
class TXConnectorBench(Enum):
	"""15 Members, R118 ... RH18"""
	R118 = 0
	R214 = 1
	R218 = 2
	R258 = 3
	R318 = 4
	R418 = 5
	RA18 = 6
	RB14 = 7
	RB18 = 8
	RC18 = 9
	RD18 = 10
	RE18 = 11
	RF18 = 12
	RG18 = 13
	RH18 = 14


# noinspection SpellCheckingInspection
class TxConverter(Enum):
	"""40 Members, ITX1 ... TX44"""
	ITX1 = 0
	ITX11 = 1
	ITX12 = 2
	ITX13 = 3
	ITX14 = 4
	ITX2 = 5
	ITX21 = 6
	ITX22 = 7
	ITX23 = 8
	ITX24 = 9
	ITX3 = 10
	ITX31 = 11
	ITX32 = 12
	ITX33 = 13
	ITX34 = 14
	ITX4 = 15
	ITX41 = 16
	ITX42 = 17
	ITX43 = 18
	ITX44 = 19
	TX1 = 20
	TX11 = 21
	TX12 = 22
	TX13 = 23
	TX14 = 24
	TX2 = 25
	TX21 = 26
	TX22 = 27
	TX23 = 28
	TX24 = 29
	TX3 = 30
	TX31 = 31
	TX32 = 32
	TX33 = 33
	TX34 = 34
	TX4 = 35
	TX41 = 36
	TX42 = 37
	TX43 = 38
	TX44 = 39
