from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 17 total commands, 0 Sub-groups, 17 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("result", core, parent)

	def get_spower(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SPOWer \n
		Snippet: value: bool = driver.configure.multiEval.result.get_spower() \n
		No command help available \n
			:return: enable: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SPOWer?')
		return Conversions.str_to_bool(response)

	def set_spower(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SPOWer \n
		Snippet: driver.configure.multiEval.result.set_spower(enable = False) \n
		No command help available \n
			:param enable: No help available
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SPOWer {param}')

	def get_pencoding(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PENCoding \n
		Snippet: value: bool = driver.configure.multiEval.result.get_pencoding() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PENCoding?')
		return Conversions.str_to_bool(response)

	def set_pencoding(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PENCoding \n
		Snippet: driver.configure.multiEval.result.set_pencoding(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PENCoding {param}')

	def get_frange(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:FRANge \n
		Snippet: value: bool = driver.configure.multiEval.result.get_frange() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:FRANge?')
		return Conversions.str_to_bool(response)

	def set_frange(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:FRANge \n
		Snippet: driver.configure.multiEval.result.set_frange(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:FRANge {param}')

	def get_sgacp(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SGACp \n
		Snippet: value: bool = driver.configure.multiEval.result.get_sgacp() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SGACp?')
		return Conversions.str_to_bool(response)

	def set_sgacp(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SGACp \n
		Snippet: driver.configure.multiEval.result.set_sgacp(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SGACp {param}')

	def get_so_bw(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SOBW \n
		Snippet: value: bool = driver.configure.multiEval.result.get_so_bw() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SOBW?')
		return Conversions.str_to_bool(response)

	def set_so_bw(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SOBW \n
		Snippet: driver.configure.multiEval.result.set_so_bw(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SOBW {param}')

	def get_sacp(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SACP \n
		Snippet: value: bool = driver.configure.multiEval.result.get_sacp() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SACP?')
		return Conversions.str_to_bool(response)

	def set_sacp(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SACP \n
		Snippet: driver.configure.multiEval.result.set_sacp(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:SACP {param}')

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Devm: bool: OFF | ON Differential error vector magnitude (only for EDR) ON: Evaluate results and show the view OFF: Do not evaluate results, hide the view (if applicable)
			- Phase_Diff: bool: OFF | ON Phase difference (only for EDR)
			- Mod_Scalars: bool: OFF | ON Statistical modulation results
			- Iq_Absolute: bool: OFF | ON IQ constellation absolute (only for EDR)
			- Iq_Differential: bool: OFF | ON IQ constellation differential (only for EDR)
			- Iq_Error: bool: OFF | ON IQ constellation error (only for EDR)
			- Freq_Dev: bool: OFF | ON Frequency deviation (only for BR and LE)
			- Pv_T: bool: OFF | ON Power vs. time
			- Power_Scalars: bool: OFF | ON Statistical power results
			- Spectrum_Obw: bool: OFF | ON Spectrum 20 dB bandwidth (only for BR)
			- Spectrum_Acp: bool: OFF | ON Spectrum ACP (only for BR and LE)
			- Spectrum_Gat_Acp: bool: OFF | ON Spectrum gated ACP (only for EDR)
			- Spec_Freq_Range: bool: OFF | ON Spectrum frequency range (only for BR)
			- Phase_Encoding: bool: OFF | ON Statistical differential phase encoding results (only for EDR in combined signal path)
			- Power_Vs_Slot: bool: OFF | ON Power versus slot (only for LE with CE)"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Devm'),
			ArgStruct.scalar_bool('Phase_Diff'),
			ArgStruct.scalar_bool('Mod_Scalars'),
			ArgStruct.scalar_bool('Iq_Absolute'),
			ArgStruct.scalar_bool('Iq_Differential'),
			ArgStruct.scalar_bool('Iq_Error'),
			ArgStruct.scalar_bool('Freq_Dev'),
			ArgStruct.scalar_bool('Pv_T'),
			ArgStruct.scalar_bool('Power_Scalars'),
			ArgStruct.scalar_bool('Spectrum_Obw'),
			ArgStruct.scalar_bool('Spectrum_Acp'),
			ArgStruct.scalar_bool('Spectrum_Gat_Acp'),
			ArgStruct.scalar_bool('Spec_Freq_Range'),
			ArgStruct.scalar_bool('Phase_Encoding'),
			ArgStruct.scalar_bool('Power_Vs_Slot')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Devm: bool = None
			self.Phase_Diff: bool = None
			self.Mod_Scalars: bool = None
			self.Iq_Absolute: bool = None
			self.Iq_Differential: bool = None
			self.Iq_Error: bool = None
			self.Freq_Dev: bool = None
			self.Pv_T: bool = None
			self.Power_Scalars: bool = None
			self.Spectrum_Obw: bool = None
			self.Spectrum_Acp: bool = None
			self.Spectrum_Gat_Acp: bool = None
			self.Spec_Freq_Range: bool = None
			self.Phase_Encoding: bool = None
			self.Power_Vs_Slot: bool = None

	def get_all(self) -> AllStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult[:ALL] \n
		Snippet: value: AllStruct = driver.configure.multiEval.result.get_all() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement.
		This command combines all other CONFigure:BLUetooth:MEAS<i>:MEValuation:RESult... commands. Tip: Use READ...? queries to
		retrieve results for disabled views. \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:ALL?', self.__class__.AllStruct())

	def set_all(self, value: AllStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult[:ALL] \n
		Snippet: driver.configure.multiEval.result.set_all(value = AllStruct()) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement.
		This command combines all other CONFigure:BLUetooth:MEAS<i>:MEValuation:RESult... commands. Tip: Use READ...? queries to
		retrieve results for disabled views. \n
			:param value: see the help for AllStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:ALL', value)

	def get_pscalar(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PSCalar \n
		Snippet: value: bool = driver.configure.multiEval.result.get_pscalar() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PSCalar?')
		return Conversions.str_to_bool(response)

	def set_pscalar(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PSCalar \n
		Snippet: driver.configure.multiEval.result.set_pscalar(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PSCalar {param}')

	def get_iq_absolute(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQABsolute \n
		Snippet: value: bool = driver.configure.multiEval.result.get_iq_absolute() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQABsolute?')
		return Conversions.str_to_bool(response)

	def set_iq_absolute(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQABsolute \n
		Snippet: driver.configure.multiEval.result.set_iq_absolute(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQABsolute {param}')

	def get_iq_error(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQERror \n
		Snippet: value: bool = driver.configure.multiEval.result.get_iq_error() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQERror?')
		return Conversions.str_to_bool(response)

	def set_iq_error(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQERror \n
		Snippet: driver.configure.multiEval.result.set_iq_error(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQERror {param}')

	def get_iq_difference(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQDiff \n
		Snippet: value: bool = driver.configure.multiEval.result.get_iq_difference() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQDiff?')
		return Conversions.str_to_bool(response)

	def set_iq_difference(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQDiff \n
		Snippet: driver.configure.multiEval.result.set_iq_difference(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:IQDiff {param}')

	def get_power_vs_time(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PVTime \n
		Snippet: value: bool = driver.configure.multiEval.result.get_power_vs_time() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PVTime?')
		return Conversions.str_to_bool(response)

	def set_power_vs_time(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PVTime \n
		Snippet: driver.configure.multiEval.result.set_power_vs_time(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PVTime {param}')

	def get_dev_magnitude(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:DEVMagnitude \n
		Snippet: value: bool = driver.configure.multiEval.result.get_dev_magnitude() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:DEVMagnitude?')
		return Conversions.str_to_bool(response)

	def set_dev_magnitude(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:DEVMagnitude \n
		Snippet: driver.configure.multiEval.result.set_dev_magnitude(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:DEVMagnitude {param}')

	def get_pdifference(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PDIFference \n
		Snippet: value: bool = driver.configure.multiEval.result.get_pdifference() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PDIFference?')
		return Conversions.str_to_bool(response)

	def set_pdifference(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PDIFference \n
		Snippet: driver.configure.multiEval.result.set_pdifference(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PDIFference {param}')

	def get_mscalar(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:MSCalar \n
		Snippet: value: bool = driver.configure.multiEval.result.get_mscalar() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:MSCalar?')
		return Conversions.str_to_bool(response)

	def set_mscalar(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:MSCalar \n
		Snippet: driver.configure.multiEval.result.set_mscalar(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:MSCalar {param}')

	def get_fdeviation(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:FDEViation \n
		Snippet: value: bool = driver.configure.multiEval.result.get_fdeviation() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:FDEViation?')
		return Conversions.str_to_bool(response)

	def set_fdeviation(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:FDEViation \n
		Snippet: driver.configure.multiEval.result.set_fdeviation(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:FDEViation {param}')

	def get_pv_slot(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PVSLot \n
		Snippet: value: bool = driver.configure.multiEval.result.get_pv_slot() \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:return: enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PVSLot?')
		return Conversions.str_to_bool(response)

	def set_pv_slot(self, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PVSLot \n
		Snippet: driver.configure.multiEval.result.set_pv_slot(enable = False) \n
		Enables or disables the evaluation of results and shows or hides the views in the multi-evaluation measurement. The last
		mnemonic denotes the view type: statistical modulation results , statistical power results, statistical differential
		phase encoding results (EDR in CSP) , power vs. time results, power vs. slot results (LE with CTE) , DEVM (EDR) , phase
		difference (EDR) , IQ constellation absolute (EDR) , IQ constellation differential (EDR) , IQ constellation error (EDR) ,
		frequency deviation (BR, LE) , frequency range results (BR) , spectrum 20 dB bandwidth (BR) , spectrum ACP (BR, LE) ,
		spectrum gated ACP (EDR) . Use CONFigure:BLUetooth:MEAS<i>:MEValuation to enable/disable all result types. Tip: Use READ..
		.? queries to retrieve results for disabled views. \n
			:param enable: OFF | ON ON: Evaluate results and show view OFF: Do not evaluate results, hide view
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:RESult:PVSLot {param}')
