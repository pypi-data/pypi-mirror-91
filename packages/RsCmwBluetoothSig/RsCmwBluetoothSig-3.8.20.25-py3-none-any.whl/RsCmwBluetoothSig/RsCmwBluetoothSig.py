from typing import List

from .Internal.Core import Core
from .Internal.InstrumentErrors import RsInstrException
from .Internal.CommandsGroup import CommandsGroup
from .Internal.VisaSession import VisaSession
from . import repcap
from .Internal.RepeatedCapability import RepeatedCapability


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RsCmwBluetoothSig:
	"""621 total commands, 10 Sub-groups, 0 group commands"""
	driver_options = "SupportedInstrModels = CMW500/CMW100/CMW270/CMW280/CMP, SupportedIdnPatterns = CMW, SimulationIdnString = 'Rohde&Schwarz,CMW500,100001,3.8.20.0025'"

	def __init__(self, resource_name: str, id_query: bool = True, reset: bool = False, options: str = None, direct_session: object = None):
		"""Initializes new RsCmwBluetoothSig session. \n
		Parameter options tokens examples:
			- 'Simulate=True' - starts the session in simulation mode. Default: False
			- 'SelectVisa=socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
			- 'SelectVisa=rs' - forces usage of RohdeSchwarz Visa
			- 'SelectVisa=ni' - forces usage of National Instruments Visa
			- 'QueryInstrumentStatus = False' - same as driver.utilities.instrument_status_checking = False
			- 'DriverSetup=(WriteDelay = 20, ReadDelay = 5)' - Introduces delay of 20ms before each write and 5ms before each read
			- 'DriverSetup=(OpcWaitMode = OpcQuery)' - mode for all the opc-synchronised write/reads. Other modes: StbPolling, StbPollingSlow, StbPollingSuperSlow
			- 'DriverSetup=(AddTermCharToWriteBinBLock = True)' - Adds one additional LF to the end of the binary data (some instruments require that)
			- 'DriverSetup=(AssureWriteWithTermChar = True)' - Makes sure each command/query is terminated with termination character. Default: Interface dependent
			- 'DriverSetup=(TerminationCharacter = 'x')' - Sets the termination character for reading. Default: '<LF>' (LineFeed)
			- 'DriverSetup=(IoSegmentSize = 10E3)' - Maximum size of one write/read segment. If transferred data is bigger, it is split to more segments
			- 'DriverSetup=(OpcTimeout = 10000)' - same as driver.utilities.opc_timeout = 10000
			- 'DriverSetup=(VisaTimeout = 5000)' - same as driver.utilities.visa_timeout = 5000
			- 'DriverSetup=(ViClearExeMode = 255)' - Binary combination where 1 means performing viClear() on a certain interface as the very first command in init
			- 'DriverSetup=(OpcQueryAfterWrite = True)' - same as driver.utilities.opc_query_after_write = True
		:param resource_name: VISA resource name, e.g. 'TCPIP::192.168.2.1::INSTR'
		:param id_query: if True: the instrument's model name is verified against the models supported by the driver and eventually throws an exception.
		:param reset: Resets the instrument (sends *RST command) and clears its status sybsystem
		:param options: string tokens alternating the driver settings.
		:param direct_session: Another driver object or pyVisa object to reuse the session instead of opening a new session."""
		self._core = Core(resource_name, id_query, reset, RsCmwBluetoothSig.driver_options, options, direct_session)
		self._core.driver_version = '3.8.20.0025'
		self._options = options
		self._add_all_global_repcaps()
		self._custom_properties_init()
		# noinspection PyTypeChecker
		self._base = CommandsGroup("ROOT", self._core, None)

	@classmethod
	def from_existing_session(cls, session: object, options: str = None) -> 'RsCmwBluetoothSig':
		"""Creates a new RsCmwBluetoothSig object with the entered 'session' reused. \n
		:param session: can be an another driver or a direct pyvisa session.
		:param options: string tokens alternating the driver settings."""
		# noinspection PyTypeChecker
		return cls(None, False, False, options, session)

	def __str__(self) -> str:
		if self._core.io:
			return f"RsCmwBluetoothSig session '{self._core.io.resource_name}'"
		else:
			return f"RsCmwBluetoothSig with session closed"

	@staticmethod
	def assert_minimum_version(min_version: str) -> None:
		"""Asserts that the driver version fulfills the minimum required version you have entered.
		This way you make sure your installed driver is of the entered version or newer."""
		min_version_list = min_version.split('.')
		curr_version_list = '3.8.20.0025'.split('.')
		count_min = len(min_version_list)
		count_curr = len(curr_version_list)
		count = count_min if count_min < count_curr else count_curr
		for i in range(count):
			minimum = int(min_version_list[i])
			curr = int(curr_version_list[i])
			if curr > minimum:
				break
			if curr < minimum:
				raise RsInstrException(f"Assertion for minimum RsCmwBluetoothSig version failed. Current version: '3.8.20.0025', minimum required version: '{min_version}'")
				
	@staticmethod
	def list_resources(expression: str = '?*::INSTR', visa_select: str = None) -> List[str]:
		"""Finds all the resources defined by the expression
			- '?*' - matches all the available instruments
			- 'USB::?*' - matches all the USB instruments
			- "TCPIP::192?*' - matches all the LAN instruments with the IP address starting with 192
		:param expression: see the examples in the function
		:param visa_select: optional parameter selecting a specific VISA. Examples: '@ni', '@rs'
		"""
		rm = VisaSession.get_resource_manager(visa_select)
		resources = rm.list_resources(expression)
		rm.close()
		# noinspection PyTypeChecker
		return resources

	def close(self) -> None:
		"""Closes the active RsCmwBluetoothSig session."""
		self._core.io.close()

	def get_session_handle(self) -> object:
		"""Returns the underlying session handle."""
		return self._core.get_session_handle()

	def _add_all_global_repcaps(self) -> None:
		"""Adds all the repcaps defined as global to the instrument's global repcaps dictionary."""
		self._core.io.add_global_repcap('<Instance>', RepeatedCapability("ROOT", 'repcap_instance_get', 'repcap_instance_set', repcap.Instance.Inst1))

	def repcap_instance_get(self) -> repcap.Instance:
		"""Returns Global Repeated capability Instance \n
		Selects the instrument"""
		return self._core.io.get_global_repcap_value('<Instance>')

	def repcap_instance_set(self, value: repcap.Instance) -> None:
		"""Sets Global Repeated capability Instance \n
		Selects the instrument
		Default value after init: Instance.Inst1"""
		self._core.io.set_global_repcap_value('<Instance>', value)

	def _custom_properties_init(self):
		"""Adds all the interfaces that are custom for the driver."""
		from .CustomFiles.utilities import Utilities
		self.utilities = Utilities(self._core)
		from .CustomFiles.events import Events
		self.events = Events(self._core)
		from .CustomFiles.reliability import Reliability
		self.reliability = Reliability(self._core)

	@property
	def configure(self):
		"""configure commands group. 12 Sub-classes, 3 commands."""
		if not hasattr(self, '_configure'):
			from .Implementations.Configure import Configure
			self._configure = Configure(self._core, self._base)
		return self._configure

	@property
	def diagnostic(self):
		"""diagnostic commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_diagnostic'):
			from .Implementations.Diagnostic import Diagnostic
			self._diagnostic = Diagnostic(self._core, self._base)
		return self._diagnostic

	@property
	def sense(self):
		"""sense commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_sense'):
			from .Implementations.Sense import Sense
			self._sense = Sense(self._core, self._base)
		return self._sense

	@property
	def connection(self):
		"""connection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_connection'):
			from .Implementations.Connection import Connection
			self._connection = Connection(self._core, self._base)
		return self._connection

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Implementations.Source import Source
			self._source = Source(self._core, self._base)
		return self._source

	@property
	def route(self):
		"""route commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_route'):
			from .Implementations.Route import Route
			self._route = Route(self._core, self._base)
		return self._route

	@property
	def call(self):
		"""call commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_call'):
			from .Implementations.Call import Call
			self._call = Call(self._core, self._base)
		return self._call

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .Implementations.LowEnergy import LowEnergy
			self._lowEnergy = LowEnergy(self._core, self._base)
		return self._lowEnergy

	@property
	def rxQuality(self):
		"""rxQuality commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rxQuality'):
			from .Implementations.RxQuality import RxQuality
			self._rxQuality = RxQuality(self._core, self._base)
		return self._rxQuality

	@property
	def clean(self):
		"""clean commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_clean'):
			from .Implementations.Clean import Clean
			self._clean = Clean(self._core, self._base)
		return self._clean

	def clone(self) -> 'RsCmwBluetoothSig':
		"""Creates a deep copy of the RsCmwBluetoothSig object. Also copies:
			- All the existing Global repeated capability values
			- All the default group repeated capabilities setting \n
		After cloning, you can set all the repeated capabilities settings independentely from the original group.
		Calling close() on the new object does not close the original VISA session"""
		cloned = RsCmwBluetoothSig.from_existing_session(self.get_session_handle(), self._options)
		self._base.synchronize_repcaps(cloned)
		cloned.repcap_instance_set(self.repcap_instance_get())
		return cloned

	def restore_all_repcaps_to_default(self) -> None:
		"""Sets all the Group and Global repcaps to their initial values"""
		self._base.restore_repcaps()
		self.repcap_instance_set(repcap.Instance.Inst1)
