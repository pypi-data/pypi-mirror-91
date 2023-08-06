from enum import Enum


# noinspection SpellCheckingInspection
class AccessCategory(Enum):
	"""4 Members, ACBE ... ACVO"""
	ACBE = 0
	ACBK = 1
	ACVI = 2
	ACVO = 3


# noinspection SpellCheckingInspection
class AccessNetType(Enum):
	"""8 Members, CPNetwork ... WILDcard"""
	CPNetwork = 0
	ESONetwork = 1
	FPNetwork = 2
	PDNetwork = 3
	PNETwork = 4
	PNWGaccess = 5
	TOEXperiment = 6
	WILDcard = 7


# noinspection SpellCheckingInspection
class AckType(Enum):
	"""1 Members, ACK ... ACK"""
	ACK = 0


# noinspection SpellCheckingInspection
class AllocSize(Enum):
	"""7 Members, T106 ... T996"""
	T106 = 0
	T242 = 1
	T26 = 2
	T2X9 = 3
	T484 = 4
	T52 = 5
	T996 = 6


# noinspection SpellCheckingInspection
class AuthAlgorithm(Enum):
	"""2 Members, MILenage ... XOR"""
	MILenage = 0
	XOR = 1


# noinspection SpellCheckingInspection
class AuthMethod(Enum):
	"""3 Members, DISPlay ... PBUTton"""
	DISPlay = 0
	KEYPad = 1
	PBUTton = 2


# noinspection SpellCheckingInspection
class AuthType(Enum):
	"""12 Members, AKA ... TTLS"""
	AKA = 0
	AKAPrime = 1
	CLEap = 2
	GTC = 3
	IDENtity = 4
	MD5 = 5
	NAK = 6
	NOTification = 7
	OTP = 8
	SIM = 9
	TLS = 10
	TTLS = 11


# noinspection SpellCheckingInspection
class AutoManualMode(Enum):
	"""2 Members, AUTO ... MANual"""
	AUTO = 0
	MANual = 1


# noinspection SpellCheckingInspection
class BarMethod(Enum):
	"""3 Members, EXPBar ... MUBar"""
	EXPBar = 0
	IMPBar = 1
	MUBar = 2


# noinspection SpellCheckingInspection
class BurstType(Enum):
	"""9 Members, ABURsts ... VHTBursts"""
	ABURsts = 0
	DCBursts = 1
	HESBursts = 2
	HTBursts = 3
	NHTBursts = 4
	OBURsts = 5
	OFF = 6
	ON = 7
	VHTBursts = 8


# noinspection SpellCheckingInspection
class Ch20Index(Enum):
	"""4 Members, CHA1 ... CHA4"""
	CHA1 = 0
	CHA2 = 1
	CHA3 = 2
	CHA4 = 3


# noinspection SpellCheckingInspection
class Channel80MhZ(Enum):
	"""2 Members, PRIMary ... SECondary"""
	PRIMary = 0
	SECondary = 1


# noinspection SpellCheckingInspection
class ChannelBandwidth(Enum):
	"""5 Members, BW16 ... BW88"""
	BW16 = 0
	BW20 = 1
	BW40 = 2
	BW80 = 3
	BW88 = 4


# noinspection SpellCheckingInspection
class ChannelBandwidthDut(Enum):
	"""4 Members, BW160 ... BW80"""
	BW160 = 0
	BW20 = 1
	BW40 = 2
	BW80 = 3


# noinspection SpellCheckingInspection
class CodeRate(Enum):
	"""28 Members, BR12 ... QR34"""
	BR12 = 0
	BR34 = 1
	C11Mbits = 2
	C55Mbits = 3
	D1MBit = 4
	D2MBits = 5
	MCS = 6
	MCS1 = 7
	MCS10 = 8
	MCS11 = 9
	MCS12 = 10
	MCS13 = 11
	MCS14 = 12
	MCS15 = 13
	MCS2 = 14
	MCS3 = 15
	MCS4 = 16
	MCS5 = 17
	MCS6 = 18
	MCS7 = 19
	MCS8 = 20
	MCS9 = 21
	Q1M12 = 22
	Q1M34 = 23
	Q6M23 = 24
	Q6M34 = 25
	QR12 = 26
	QR34 = 27


# noinspection SpellCheckingInspection
class CodingType(Enum):
	"""2 Members, BCC ... LDPC"""
	BCC = 0
	LDPC = 1


# noinspection SpellCheckingInspection
class ConnectionAllowed(Enum):
	"""2 Members, ANY ... SSID"""
	ANY = 0
	SSID = 1


# noinspection SpellCheckingInspection
class ConnectionMode(Enum):
	"""2 Members, ACONnect ... MANual"""
	ACONnect = 0
	MANual = 1


# noinspection SpellCheckingInspection
class DataFormatExt(Enum):
	"""7 Members, HEES ... VHT"""
	HEES = 0
	HEM = 1
	HES = 2
	HTG = 3
	HTM = 4
	NHT = 5
	VHT = 6


# noinspection SpellCheckingInspection
class DataRate(Enum):
	"""28 Members, MB1 ... MCS9"""
	MB1 = 0
	MB11 = 1
	MB12 = 2
	MB18 = 3
	MB2 = 4
	MB24 = 5
	MB36 = 6
	MB48 = 7
	MB5 = 8
	MB54 = 9
	MB6 = 10
	MB9 = 11
	MCS0 = 12
	MCS1 = 13
	MCS10 = 14
	MCS11 = 15
	MCS12 = 16
	MCS13 = 17
	MCS14 = 18
	MCS15 = 19
	MCS2 = 20
	MCS3 = 21
	MCS4 = 22
	MCS5 = 23
	MCS6 = 24
	MCS7 = 25
	MCS8 = 26
	MCS9 = 27


# noinspection SpellCheckingInspection
class DelayType(Enum):
	"""2 Members, BURSt ... CONStant"""
	BURSt = 0
	CONStant = 1


# noinspection SpellCheckingInspection
class DeviceClass(Enum):
	"""2 Members, A ... B"""
	A = 0
	B = 1


# noinspection SpellCheckingInspection
class DynFragment(Enum):
	"""4 Members, L1 ... NO"""
	L1 = 0
	L2 = 1
	L3 = 2
	NO = 3


# noinspection SpellCheckingInspection
class EapType(Enum):
	"""5 Members, AKA ... TTLS"""
	AKA = 0
	APRime = 1
	SIM = 2
	TLS = 3
	TTLS = 4


# noinspection SpellCheckingInspection
class EnableState(Enum):
	"""2 Members, DISable ... ENABle"""
	DISable = 0
	ENABle = 1


# noinspection SpellCheckingInspection
class EncryptionType(Enum):
	"""3 Members, AES ... TKIP"""
	AES = 0
	DISabled = 1
	TKIP = 2


# noinspection SpellCheckingInspection
class EntityOperationMode(Enum):
	"""6 Members, AP ... WDIRect"""
	AP = 0
	HSPot2 = 1
	IBSS = 2
	STATion = 3
	TESTmode = 4
	WDIRect = 5


# noinspection SpellCheckingInspection
class FlowType(Enum):
	"""2 Members, ANNounced ... UNANnounced"""
	ANNounced = 0
	UNANnounced = 1


# noinspection SpellCheckingInspection
class FrameFormat(Enum):
	"""6 Members, HEMU ... VHT"""
	HEMU = 0
	HESU = 1
	HETB = 2
	HT = 3
	NHT = 4
	VHT = 5


# noinspection SpellCheckingInspection
class FrequencyBand(Enum):
	"""2 Members, B6GHz ... BS6Ghz"""
	B6GHz = 0
	BS6Ghz = 1


# noinspection SpellCheckingInspection
class Giltf(Enum):
	"""3 Members, L116 ... L432"""
	L116 = 0
	L216 = 1
	L432 = 2


# noinspection SpellCheckingInspection
class GuardInterval(Enum):
	"""5 Members, GI08 ... SHORt"""
	GI08 = 0
	GI16 = 1
	GI32 = 2
	LONG = 3
	SHORt = 4


# noinspection SpellCheckingInspection
class HeTbMainMeasState(Enum):
	"""3 Members, OFF ... RUN"""
	OFF = 0
	RDY = 1
	RUN = 2


# noinspection SpellCheckingInspection
class IpAddrIndex(Enum):
	"""3 Members, IP1 ... IP3"""
	IP1 = 0
	IP2 = 1
	IP3 = 2


# noinspection SpellCheckingInspection
class Ipv6AddField(Enum):
	"""3 Members, AATNknown ... ATNavailable"""
	AATNknown = 0
	ATAVailable = 1
	ATNavailable = 2


# noinspection SpellCheckingInspection
class Ipv6AddFieldExt(Enum):
	"""8 Members, AATNknown ... SNPiaavailab"""
	AATNknown = 0
	ATNavailable = 1
	DNPiaavailab = 2
	PDNiaavailab = 3
	PIAavailable = 4
	PRIaavailabl = 5
	PSNiaavailab = 6
	SNPiaavailab = 7


# noinspection SpellCheckingInspection
class IpVersion(Enum):
	"""2 Members, IV4 ... IV6"""
	IV4 = 0
	IV6 = 1


# noinspection SpellCheckingInspection
class IpVersionExt(Enum):
	"""3 Members, IV4 ... IV6"""
	IV4 = 0
	IV4V6 = 1
	IV6 = 2


# noinspection SpellCheckingInspection
class LenMode(Enum):
	"""4 Members, DEFault ... UDEFined"""
	DEFault = 0
	OFF = 1
	ON = 2
	UDEFined = 3


# noinspection SpellCheckingInspection
class Level(Enum):
	"""4 Members, LEV0 ... LEV3"""
	LEV0 = 0
	LEV1 = 1
	LEV2 = 2
	LEV3 = 3


# noinspection SpellCheckingInspection
class LogCategoryB(Enum):
	"""4 Members, EMPTy ... WARNing"""
	EMPTy = 0
	ERRor = 1
	INFO = 2
	WARNing = 3


# noinspection SpellCheckingInspection
class LtfGi(Enum):
	"""3 Members, L208 ... L432"""
	L208 = 0
	L216 = 1
	L432 = 2


# noinspection SpellCheckingInspection
class LtfType(Enum):
	"""3 Members, X1 ... X4"""
	X1 = 0
	X2 = 1
	X4 = 2


# noinspection SpellCheckingInspection
class McsIndex(Enum):
	"""12 Members, MCS ... MCS9"""
	MCS = 0
	MCS1 = 1
	MCS10 = 2
	MCS11 = 3
	MCS2 = 4
	MCS3 = 5
	MCS4 = 6
	MCS5 = 7
	MCS6 = 8
	MCS7 = 9
	MCS8 = 10
	MCS9 = 11


# noinspection SpellCheckingInspection
class McsSupport(Enum):
	"""2 Members, NOTSupported ... SUPPorted"""
	NOTSupported = 0
	SUPPorted = 1


# noinspection SpellCheckingInspection
class MimoMode(Enum):
	"""3 Members, SMULtiplexin ... TXDiversity"""
	SMULtiplexin = 0
	STBC = 1
	TXDiversity = 2


# noinspection SpellCheckingInspection
class MuMimoLongTrainField(Enum):
	"""2 Members, MASK ... SING"""
	MASK = 0
	SING = 1


# noinspection SpellCheckingInspection
class NdpSoundingMethod(Enum):
	"""2 Members, NONTrigger ... TBASed"""
	NONTrigger = 0
	TBASed = 1


# noinspection SpellCheckingInspection
class NdpSoundingType(Enum):
	"""3 Members, CQI ... SU"""
	CQI = 0
	MU = 1
	SU = 2


# noinspection SpellCheckingInspection
class NetAuthTypeInd(Enum):
	"""4 Members, ATConditions ... OESupported"""
	ATConditions = 0
	DREDirection = 1
	HREDirection = 2
	OESupported = 3


# noinspection SpellCheckingInspection
class Ngrouping(Enum):
	"""2 Members, GRP16 ... GRP4"""
	GRP16 = 0
	GRP4 = 1


# noinspection SpellCheckingInspection
class NumColumns(Enum):
	"""2 Members, COL1 ... COL2"""
	COL1 = 0
	COL2 = 1


# noinspection SpellCheckingInspection
class NumOfDigits(Enum):
	"""2 Members, THDigits ... TWDigits"""
	THDigits = 0
	TWDigits = 1


# noinspection SpellCheckingInspection
class Pattern(Enum):
	"""37 Members, AONE ... PT10"""
	AONE = 0
	AZERo = 1
	PN1 = 2
	PN10 = 3
	PN11 = 4
	PN12 = 5
	PN13 = 6
	PN14 = 7
	PN15 = 8
	PN16 = 9
	PN17 = 10
	PN18 = 11
	PN19 = 12
	PN2 = 13
	PN20 = 14
	PN21 = 15
	PN22 = 16
	PN23 = 17
	PN24 = 18
	PN25 = 19
	PN26 = 20
	PN27 = 21
	PN28 = 22
	PN29 = 23
	PN3 = 24
	PN30 = 25
	PN31 = 26
	PN32 = 27
	PN4 = 28
	PN5 = 29
	PN6 = 30
	PN7 = 31
	PN8 = 32
	PN9 = 33
	PRANdom = 34
	PT01 = 35
	PT10 = 36


# noinspection SpellCheckingInspection
class PayloadType(Enum):
	"""6 Members, AONes ... PRANdom"""
	AONes = 0
	AZERoes = 1
	BP01 = 2
	BP10 = 3
	DEFault = 4
	PRANdom = 5


# noinspection SpellCheckingInspection
class PccBasebandBoard(Enum):
	"""140 Members, BBR1 ... SUW44"""
	BBR1 = 0
	BBR11 = 1
	BBR12 = 2
	BBR13 = 3
	BBR14 = 4
	BBR2 = 5
	BBR21 = 6
	BBR22 = 7
	BBR23 = 8
	BBR24 = 9
	BBR3 = 10
	BBR31 = 11
	BBR32 = 12
	BBR33 = 13
	BBR34 = 14
	BBR4 = 15
	BBR41 = 16
	BBR42 = 17
	BBR43 = 18
	BBR44 = 19
	BBT1 = 20
	BBT11 = 21
	BBT12 = 22
	BBT13 = 23
	BBT14 = 24
	BBT2 = 25
	BBT21 = 26
	BBT22 = 27
	BBT23 = 28
	BBT24 = 29
	BBT3 = 30
	BBT31 = 31
	BBT32 = 32
	BBT33 = 33
	BBT34 = 34
	BBT4 = 35
	BBT41 = 36
	BBT42 = 37
	BBT43 = 38
	BBT44 = 39
	SUA012 = 40
	SUA034 = 41
	SUA056 = 42
	SUA078 = 43
	SUA1 = 44
	SUA11 = 45
	SUA112 = 46
	SUA12 = 47
	SUA13 = 48
	SUA134 = 49
	SUA14 = 50
	SUA15 = 51
	SUA156 = 52
	SUA16 = 53
	SUA17 = 54
	SUA178 = 55
	SUA18 = 56
	SUA2 = 57
	SUA21 = 58
	SUA212 = 59
	SUA22 = 60
	SUA23 = 61
	SUA234 = 62
	SUA24 = 63
	SUA25 = 64
	SUA256 = 65
	SUA26 = 66
	SUA27 = 67
	SUA278 = 68
	SUA28 = 69
	SUA3 = 70
	SUA31 = 71
	SUA312 = 72
	SUA32 = 73
	SUA33 = 74
	SUA334 = 75
	SUA34 = 76
	SUA35 = 77
	SUA356 = 78
	SUA36 = 79
	SUA37 = 80
	SUA378 = 81
	SUA38 = 82
	SUA4 = 83
	SUA41 = 84
	SUA412 = 85
	SUA42 = 86
	SUA43 = 87
	SUA434 = 88
	SUA44 = 89
	SUA45 = 90
	SUA456 = 91
	SUA46 = 92
	SUA47 = 93
	SUA478 = 94
	SUA48 = 95
	SUA5 = 96
	SUA6 = 97
	SUA7 = 98
	SUA8 = 99
	SUU1 = 100
	SUU11 = 101
	SUU12 = 102
	SUU13 = 103
	SUU14 = 104
	SUU2 = 105
	SUU21 = 106
	SUU22 = 107
	SUU23 = 108
	SUU24 = 109
	SUU3 = 110
	SUU31 = 111
	SUU32 = 112
	SUU33 = 113
	SUU34 = 114
	SUU4 = 115
	SUU41 = 116
	SUU42 = 117
	SUU43 = 118
	SUU44 = 119
	SUW1 = 120
	SUW11 = 121
	SUW12 = 122
	SUW13 = 123
	SUW14 = 124
	SUW2 = 125
	SUW21 = 126
	SUW22 = 127
	SUW23 = 128
	SUW24 = 129
	SUW3 = 130
	SUW31 = 131
	SUW32 = 132
	SUW33 = 133
	SUW34 = 134
	SUW4 = 135
	SUW41 = 136
	SUW42 = 137
	SUW43 = 138
	SUW44 = 139


# noinspection SpellCheckingInspection
class PccFadingBoard(Enum):
	"""60 Members, FAD012 ... FAD8"""
	FAD012 = 0
	FAD034 = 1
	FAD056 = 2
	FAD078 = 3
	FAD1 = 4
	FAD11 = 5
	FAD112 = 6
	FAD12 = 7
	FAD13 = 8
	FAD134 = 9
	FAD14 = 10
	FAD15 = 11
	FAD156 = 12
	FAD16 = 13
	FAD17 = 14
	FAD178 = 15
	FAD18 = 16
	FAD2 = 17
	FAD21 = 18
	FAD212 = 19
	FAD22 = 20
	FAD23 = 21
	FAD234 = 22
	FAD24 = 23
	FAD25 = 24
	FAD256 = 25
	FAD26 = 26
	FAD27 = 27
	FAD278 = 28
	FAD28 = 29
	FAD3 = 30
	FAD31 = 31
	FAD312 = 32
	FAD32 = 33
	FAD33 = 34
	FAD334 = 35
	FAD34 = 36
	FAD35 = 37
	FAD356 = 38
	FAD36 = 39
	FAD37 = 40
	FAD378 = 41
	FAD38 = 42
	FAD4 = 43
	FAD41 = 44
	FAD412 = 45
	FAD42 = 46
	FAD43 = 47
	FAD434 = 48
	FAD44 = 49
	FAD45 = 50
	FAD456 = 51
	FAD46 = 52
	FAD47 = 53
	FAD478 = 54
	FAD48 = 55
	FAD5 = 56
	FAD6 = 57
	FAD7 = 58
	FAD8 = 59


# noinspection SpellCheckingInspection
class PeDuration(Enum):
	"""6 Members, AUTO ... PE8"""
	AUTO = 0
	PE0 = 1
	PE12 = 2
	PE16 = 3
	PE4 = 4
	PE8 = 5


# noinspection SpellCheckingInspection
class PowerIndicator(Enum):
	"""3 Members, OVERdriven ... UNDerdriven"""
	OVERdriven = 0
	RANGe = 1
	UNDerdriven = 2


# noinspection SpellCheckingInspection
class PrioMode(Enum):
	"""3 Members, AUTO ... TIDPriority"""
	AUTO = 0
	ROURobin = 1
	TIDPriority = 2


# noinspection SpellCheckingInspection
class PrioModeB(Enum):
	"""2 Members, AUTO ... ROURobin"""
	AUTO = 0
	ROURobin = 1


# noinspection SpellCheckingInspection
class Profile(Enum):
	"""6 Members, MODA ... MODF"""
	MODA = 0
	MODB = 1
	MODC = 2
	MODD = 3
	MODE = 4
	MODF = 5


# noinspection SpellCheckingInspection
class ProtocolType(Enum):
	"""2 Members, ICMP ... UDP"""
	ICMP = 0
	UDP = 1


# noinspection SpellCheckingInspection
class PsState(Enum):
	"""7 Members, ASSociated ... PROBed"""
	ASSociated = 0
	AUTHenticated = 1
	CTIMeout = 2
	DEAuthenticated = 3
	DISassociated = 4
	IDLE = 5
	PROBed = 6


# noinspection SpellCheckingInspection
class PulseLengthMode(Enum):
	"""5 Members, BLENgth ... UDEFined"""
	BLENgth = 0
	DEFault = 1
	OFF = 2
	ON = 3
	UDEFined = 4


# noinspection SpellCheckingInspection
class RateSupport(Enum):
	"""3 Members, DISabled ... OPTional"""
	DISabled = 0
	MANDatory = 1
	OPTional = 2


# noinspection SpellCheckingInspection
class Repeat(Enum):
	"""2 Members, CONTinuous ... SINGleshot"""
	CONTinuous = 0
	SINGleshot = 1


# noinspection SpellCheckingInspection
class Reservation(Enum):
	"""3 Members, ANY ... SET"""
	ANY = 0
	OFF = 1
	SET = 2


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
class ResultState(Enum):
	"""3 Members, FAILure ... SUCCess"""
	FAILure = 0
	IDLE = 1
	SUCCess = 2


# noinspection SpellCheckingInspection
class RuAlloc(Enum):
	"""5 Members, DMY1 ... USR1"""
	DMY1 = 0
	DMY2 = 1
	DMY3 = 2
	OFF = 3
	USR1 = 4


# noinspection SpellCheckingInspection
class RuAllocation(Enum):
	"""70 Members, OFF ... RU9"""
	OFF = 0
	RU0 = 1
	RU1 = 2
	RU10 = 3
	RU11 = 4
	RU12 = 5
	RU13 = 6
	RU14 = 7
	RU15 = 8
	RU16 = 9
	RU17 = 10
	RU18 = 11
	RU19 = 12
	RU2 = 13
	RU20 = 14
	RU21 = 15
	RU22 = 16
	RU23 = 17
	RU24 = 18
	RU25 = 19
	RU26 = 20
	RU27 = 21
	RU28 = 22
	RU29 = 23
	RU3 = 24
	RU30 = 25
	RU31 = 26
	RU32 = 27
	RU33 = 28
	RU34 = 29
	RU35 = 30
	RU36 = 31
	RU37 = 32
	RU38 = 33
	RU39 = 34
	RU4 = 35
	RU40 = 36
	RU41 = 37
	RU42 = 38
	RU43 = 39
	RU44 = 40
	RU45 = 41
	RU46 = 42
	RU47 = 43
	RU48 = 44
	RU49 = 45
	RU5 = 46
	RU50 = 47
	RU51 = 48
	RU52 = 49
	RU53 = 50
	RU54 = 51
	RU55 = 52
	RU56 = 53
	RU57 = 54
	RU58 = 55
	RU59 = 56
	RU6 = 57
	RU60 = 58
	RU61 = 59
	RU62 = 60
	RU63 = 61
	RU64 = 62
	RU65 = 63
	RU66 = 64
	RU67 = 65
	RU68 = 66
	RU7 = 67
	RU8 = 68
	RU9 = 69


# noinspection SpellCheckingInspection
class RuIndex(Enum):
	"""9 Members, RU1 ... RU9"""
	RU1 = 0
	RU2 = 1
	RU3 = 2
	RU4 = 3
	RU5 = 4
	RU6 = 5
	RU7 = 6
	RU8 = 7
	RU9 = 8


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
class Scenario(Enum):
	"""6 Members, MIMFading ... UNDefined"""
	MIMFading = 0
	MIMO = 1
	MIMO2 = 2
	SCFading = 3
	STANdard = 4
	UNDefined = 5


# noinspection SpellCheckingInspection
class SecurityType(Enum):
	"""5 Members, DISabled ... WPERsonal"""
	DISabled = 0
	W2ENterprise = 1
	W2Personal = 2
	WENTerprise = 3
	WPERsonal = 4


# noinspection SpellCheckingInspection
class SegmentNumber(Enum):
	"""3 Members, A ... C"""
	A = 0
	B = 1
	C = 2


# noinspection SpellCheckingInspection
class Size(Enum):
	"""2 Members, SIZE0 ... SIZE1"""
	SIZE0 = 0
	SIZE1 = 1


# noinspection SpellCheckingInspection
class SmoothingBit(Enum):
	"""2 Members, NRECommended ... RECommended"""
	NRECommended = 0
	RECommended = 1


# noinspection SpellCheckingInspection
class SourceInt(Enum):
	"""2 Members, EXTernal ... INTernal"""
	EXTernal = 0
	INTernal = 1


# noinspection SpellCheckingInspection
class SpacialStreamsNr(Enum):
	"""8 Members, NSS1 ... NSS8"""
	NSS1 = 0
	NSS2 = 1
	NSS3 = 2
	NSS4 = 3
	NSS5 = 4
	NSS6 = 5
	NSS7 = 6
	NSS8 = 7


# noinspection SpellCheckingInspection
class SpatialStreams(Enum):
	"""5 Members, ALL ... STR2"""
	ALL = 0
	OFF = 1
	ON = 2
	STR1 = 3
	STR2 = 4


# noinspection SpellCheckingInspection
class StandardType(Enum):
	"""10 Members, ACSTd ... NGFStd"""
	ACSTd = 0
	ANSTd = 1
	ASTD = 2
	AXSTd = 3
	BSTD = 4
	GNSTd = 5
	GONStd = 6
	GOSTd = 7
	GSTD = 8
	NGFStd = 9


# noinspection SpellCheckingInspection
class Station(Enum):
	"""3 Members, STA1 ... STA3"""
	STA1 = 0
	STA2 = 1
	STA3 = 2


# noinspection SpellCheckingInspection
class Streams(Enum):
	"""2 Members, STR1 ... STR2"""
	STR1 = 0
	STR2 = 1


# noinspection SpellCheckingInspection
class Subfield(Enum):
	"""39 Members, A000 ... A224"""
	A000 = 0
	A001 = 1
	A002 = 2
	A003 = 3
	A004 = 4
	A005 = 5
	A006 = 6
	A007 = 7
	A008 = 8
	A009 = 9
	A010 = 10
	A011 = 11
	A012 = 12
	A013 = 13
	A014 = 14
	A015 = 15
	A016 = 16
	A024 = 17
	A032 = 18
	A040 = 19
	A048 = 20
	A056 = 21
	A064 = 22
	A072 = 23
	A080 = 24
	A088 = 25
	A096 = 26
	A112 = 27
	A113 = 28
	A114 = 29
	A115 = 30
	A116 = 31
	A120 = 32
	A128 = 33
	A192 = 34
	A200 = 35
	A208 = 36
	A216 = 37
	A224 = 38


# noinspection SpellCheckingInspection
class SyncState(Enum):
	"""7 Members, ADINtermed ... RFHandover"""
	ADINtermed = 0
	ADJusted = 1
	INValid = 2
	OFF = 3
	ON = 4
	PENDing = 5
	RFHandover = 6


# noinspection SpellCheckingInspection
class Tid(Enum):
	"""8 Members, TID0 ... TID7"""
	TID0 = 0
	TID1 = 1
	TID2 = 2
	TID3 = 3
	TID4 = 4
	TID5 = 5
	TID6 = 6
	TID7 = 7


# noinspection SpellCheckingInspection
class TriggerBandwidth(Enum):
	"""7 Members, ALL ... ON"""
	ALL = 0
	BW160 = 1
	BW20 = 2
	BW40 = 3
	BW80 = 4
	OFF = 5
	ON = 6


# noinspection SpellCheckingInspection
class TriggerFrmPowerMode(Enum):
	"""3 Members, AUTO ... MAXPower"""
	AUTO = 0
	MANual = 1
	MAXPower = 2


# noinspection SpellCheckingInspection
class TriggerRate(Enum):
	"""31 Members, ALL ... QR34"""
	ALL = 0
	BR12 = 1
	BR34 = 2
	C11Mbits = 3
	C55Mbits = 4
	D1MBit = 5
	D2MBits = 6
	MCS0 = 7
	MCS1 = 8
	MCS10 = 9
	MCS11 = 10
	MCS12 = 11
	MCS13 = 12
	MCS14 = 13
	MCS15 = 14
	MCS2 = 15
	MCS3 = 16
	MCS4 = 17
	MCS5 = 18
	MCS6 = 19
	MCS7 = 20
	MCS8 = 21
	MCS9 = 22
	OFF = 23
	ON = 24
	Q1M12 = 25
	Q1M34 = 26
	Q6M23 = 27
	Q6M34 = 28
	QR12 = 29
	QR34 = 30


# noinspection SpellCheckingInspection
class TriggerSlope(Enum):
	"""4 Members, FEDGe ... REDGe"""
	FEDGe = 0
	OFF = 1
	ON = 2
	REDGe = 3


# noinspection SpellCheckingInspection
class TriggerType(Enum):
	"""5 Members, BQRP ... MRTS"""
	BQRP = 0
	BRP = 1
	BSRP = 2
	BTR = 3
	MRTS = 4


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


# noinspection SpellCheckingInspection
class VhtRates(Enum):
	"""3 Members, MC07 ... MC09"""
	MC07 = 0
	MC08 = 1
	MC09 = 2


# noinspection SpellCheckingInspection
class YesNoStatus(Enum):
	"""2 Members, NO ... YES"""
	NO = 0
	YES = 1
