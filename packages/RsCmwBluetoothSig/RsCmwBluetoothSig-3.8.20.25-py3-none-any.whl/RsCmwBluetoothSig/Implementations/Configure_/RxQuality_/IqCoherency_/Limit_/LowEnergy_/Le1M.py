from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le1M:
	"""Le1M commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("le1M", core, parent)

	# noinspection PyTypeChecker
	class A0ReferenceStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Limit: float or bool: numeric Range: 0 (Rad) to 3.14 (Rad)
			- Enable: bool: OFF | ON Disables/enables the limit check"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Limit'),
			ArgStruct.scalar_bool('Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit: float or bool = None
			self.Enable: bool = None

	def get_a_0_reference(self) -> A0ReferenceStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A0Reference \n
		Snippet: value: A0ReferenceStruct = driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le1M.get_a_0_reference() \n
		Defines the IQ samples coherency limit for mean reference phase deviation (RPD) results for the reference antenna.
		Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for A0ReferenceStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A0Reference?', self.__class__.A0ReferenceStruct())

	def set_a_0_reference(self, value: A0ReferenceStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A0Reference \n
		Snippet: driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le1M.set_a_0_reference(value = A0ReferenceStruct()) \n
		Defines the IQ samples coherency limit for mean reference phase deviation (RPD) results for the reference antenna.
		Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param value: see the help for A0ReferenceStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A0Reference', value)

	# noinspection PyTypeChecker
	class A1NreferenceStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Limit: float or bool: numeric Range: 0 (Rad) to 3.14 (Rad)
			- Enable: bool: OFF | ON Disables/enables the limit check"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Limit'),
			ArgStruct.scalar_bool('Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit: float or bool = None
			self.Enable: bool = None

	def get_a_1_nreference(self) -> A1NreferenceStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A1NReference \n
		Snippet: value: A1NreferenceStruct = driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le1M.get_a_1_nreference() \n
		Defines the IQ samples coherency limit for 95% relative phase values RP(m) for non-reference antennas A1NReference to
		A3NReference. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for A1NreferenceStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A1NReference?', self.__class__.A1NreferenceStruct())

	def set_a_1_nreference(self, value: A1NreferenceStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A1NReference \n
		Snippet: driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le1M.set_a_1_nreference(value = A1NreferenceStruct()) \n
		Defines the IQ samples coherency limit for 95% relative phase values RP(m) for non-reference antennas A1NReference to
		A3NReference. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param value: see the help for A1NreferenceStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A1NReference', value)

	# noinspection PyTypeChecker
	class A2NreferenceStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Limit: float or bool: numeric Range: 0 (Rad) to 3.14 (Rad)
			- Enable: bool: OFF | ON Disables/enables the limit check"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Limit'),
			ArgStruct.scalar_bool('Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit: float or bool = None
			self.Enable: bool = None

	def get_a_2_nreference(self) -> A2NreferenceStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A2NReference \n
		Snippet: value: A2NreferenceStruct = driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le1M.get_a_2_nreference() \n
		Defines the IQ samples coherency limit for 95% relative phase values RP(m) for non-reference antennas A1NReference to
		A3NReference. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for A2NreferenceStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A2NReference?', self.__class__.A2NreferenceStruct())

	def set_a_2_nreference(self, value: A2NreferenceStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A2NReference \n
		Snippet: driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le1M.set_a_2_nreference(value = A2NreferenceStruct()) \n
		Defines the IQ samples coherency limit for 95% relative phase values RP(m) for non-reference antennas A1NReference to
		A3NReference. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param value: see the help for A2NreferenceStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A2NReference', value)

	# noinspection PyTypeChecker
	class A3NreferenceStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Limit: float or bool: numeric Range: 0 (Rad) to 3.14 (Rad)
			- Enable: bool: OFF | ON Disables/enables the limit check"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Limit'),
			ArgStruct.scalar_bool('Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit: float or bool = None
			self.Enable: bool = None

	def get_a_3_nreference(self) -> A3NreferenceStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A3NReference \n
		Snippet: value: A3NreferenceStruct = driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le1M.get_a_3_nreference() \n
		Defines the IQ samples coherency limit for 95% relative phase values RP(m) for non-reference antennas A1NReference to
		A3NReference. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for A3NreferenceStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A3NReference?', self.__class__.A3NreferenceStruct())

	def set_a_3_nreference(self, value: A3NreferenceStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A3NReference \n
		Snippet: driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le1M.set_a_3_nreference(value = A3NreferenceStruct()) \n
		Defines the IQ samples coherency limit for 95% relative phase values RP(m) for non-reference antennas A1NReference to
		A3NReference. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param value: see the help for A3NreferenceStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE1M:A3NReference', value)
