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
	Inst3 = 3
	Inst4 = 4


# noinspection SpellCheckingInspection
class CommSettings(Enum):
	"""Repeated capability CommSettings \n
	Whether to set LE or BR EDR settings"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Hw1 = 1
	Hw2 = 2
	Hw3 = 3
	Hw4 = 4


# noinspection SpellCheckingInspection
class HardwareIntf(Enum):
	"""Repeated capability HardwareIntf \n
	Whether to set LE or BR EDR settings"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Intf1 = 1
	Intf2 = 2
	Intf3 = 3
	Intf4 = 4


# noinspection SpellCheckingInspection
class UsbSettings(Enum):
	"""Repeated capability UsbSettings \n
	Whether to set LE or BR EDR settings"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Sett1 = 1
	Sett2 = 2
	Sett3 = 3
	Sett4 = 4
