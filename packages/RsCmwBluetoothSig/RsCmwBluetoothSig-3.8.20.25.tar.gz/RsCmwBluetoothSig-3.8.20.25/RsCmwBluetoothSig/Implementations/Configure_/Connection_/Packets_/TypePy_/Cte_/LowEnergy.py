from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergy:
	"""LowEnergy commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_le_1_m(self) -> enums.CteType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:TYPE:CTE:LENergy:LE1M \n
		Snippet: value: enums.CteType = driver.configure.connection.packets.typePy.cte.lowEnergy.get_le_1_m() \n
		Selects the CTE type. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: cte_type: AOA2us | AOD1us | AOD2us | AOA1us AOA1us: angle of arrival 1 µs AOA2us: angle of arrival 2 µs AOD1us: angle of departure 1 µs AOD2us: angle of departure 2 µs
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:TYPE:CTE:LENergy:LE1M?')
		return Conversions.str_to_scalar_enum(response, enums.CteType)

	def set_le_1_m(self, cte_type: enums.CteType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:TYPE:CTE:LENergy:LE1M \n
		Snippet: driver.configure.connection.packets.typePy.cte.lowEnergy.set_le_1_m(cte_type = enums.CteType.AOA1us) \n
		Selects the CTE type. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param cte_type: AOA2us | AOD1us | AOD2us | AOA1us AOA1us: angle of arrival 1 µs AOA2us: angle of arrival 2 µs AOD1us: angle of departure 1 µs AOD2us: angle of departure 2 µs
		"""
		param = Conversions.enum_scalar_to_str(cte_type, enums.CteType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:TYPE:CTE:LENergy:LE1M {param}')

	# noinspection PyTypeChecker
	def get_le_2_m(self) -> enums.CteType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:TYPE:CTE:LENergy:LE2M \n
		Snippet: value: enums.CteType = driver.configure.connection.packets.typePy.cte.lowEnergy.get_le_2_m() \n
		Selects the CTE type. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: cte_type: AOA2us | AOD1us | AOD2us | AOA1us AOA1us: angle of arrival 1 µs AOA2us: angle of arrival 2 µs AOD1us: angle of departure 1 µs AOD2us: angle of departure 2 µs
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:TYPE:CTE:LENergy:LE2M?')
		return Conversions.str_to_scalar_enum(response, enums.CteType)

	def set_le_2_m(self, cte_type: enums.CteType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:TYPE:CTE:LENergy:LE2M \n
		Snippet: driver.configure.connection.packets.typePy.cte.lowEnergy.set_le_2_m(cte_type = enums.CteType.AOA1us) \n
		Selects the CTE type. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param cte_type: AOA2us | AOD1us | AOD2us | AOA1us AOA1us: angle of arrival 1 µs AOA2us: angle of arrival 2 µs AOD1us: angle of departure 1 µs AOD2us: angle of departure 2 µs
		"""
		param = Conversions.enum_scalar_to_str(cte_type, enums.CteType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:TYPE:CTE:LENergy:LE2M {param}')
