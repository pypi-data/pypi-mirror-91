from enum import Enum
from .Internal.RepeatedCapability import VALUE_DEFAULT
from .Internal.RepeatedCapability import VALUE_EMPTY


# noinspection SpellCheckingInspection
class Instance(Enum):
	"""Global Repeated capability Instance \n
	Selects the instrument"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Inst1 = 1
	Inst2 = 2


# noinspection SpellCheckingInspection
class Antenna(Enum):
	"""Repeated capability Antenna \n
	Selects the antenna"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class DomainName(Enum):
	"""Repeated capability DomainName \n
	Index of the PLMN"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5


# noinspection SpellCheckingInspection
class Dummy(Enum):
	"""Repeated capability Dummy \n
	Selects the Dummy"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class IpRouteAddress(Enum):
	"""Repeated capability IpRouteAddress \n
	route number"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5


# noinspection SpellCheckingInspection
class IpVersion(Enum):
	"""Repeated capability IpVersion \n
	IP Version"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	V4 = 4
	V6 = 6


# noinspection SpellCheckingInspection
class PacketGenerator(Enum):
	"""Repeated capability PacketGenerator \n
	Selects the Packet Generator"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class Plnm(Enum):
	"""Repeated capability Plnm \n
	Index of the PLMN"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5


# noinspection SpellCheckingInspection
class Realm(Enum):
	"""Repeated capability Realm \n
	Index of the PLMN"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5


# noinspection SpellCheckingInspection
class Station(Enum):
	"""Repeated capability Station \n
	Selects the instrument"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class User(Enum):
	"""Repeated capability User \n
	Selects the User"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
