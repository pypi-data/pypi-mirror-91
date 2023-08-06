"""Fsup class"""
from datetime import datetime
import pathlib
import time
from rsfsup.common import RSBase, get_idn, validate
from rsfsup.status import Status
from rsfsup.spectrum_analyzer.instrument import SpecAn
from rsfsup.ssa.instrument import SSA
from rsfsup.mass_memory import MassMemory


class Fsup(RSBase):
    """Fsup class

    Attributes:
        visa (pyvisa.resources.Resource): pyvisa resource
    """

    _modes = {"SAN": "SPECTRUM", "PNO": "SSA"}
    _options = {
        "B4": "Low-aging OCXO",
        "B10": "External Generator Control",
        "B18": "Removable Hard Disk",
        "B19": "Second Hard Disk",
        "B21": "LO/IF Ports for External Mixers",
        "B23": "20 dB Preamplifier",
        "B25": "Electronic Attenuator",
        "B28": "Trigger Port",
        "B60": "Low Phase Noise",
        "B61": "Correlation Extension",
        "K5": "GSM/EDGE",
        "K8": "Bluetooth",
        "K9": "Power Sensor Measurements",
        "K30": "Noise Figure and Gain Measurements",
        "K70": "Vector Signal Analysis",
    }

    def __init__(self, visa):
        super().__init__(visa)
        self._visa.write("*CLS")
        self._visa.write("SYSTEM:ERROR:CLEAR:ALL")
        self._visa.write("*ESE 255")
        self._visa.write("FORMAT ASCII")
        self._idn = get_idn(visa)
        self._currentmode = self.mode
        if self._currentmode == "SPECTRUM":
            self.spectrum = SpecAn(self)
        else:
            self.ssa = SSA(self)
        self.status = Status(self)
        self.file_system = MassMemory(self)

    @property
    def model(self):
        """(str): the model number"""
        return self._idn.model

    @property
    def serial_number(self):
        """(str): the serial number"""
        return self._idn.serial_number

    @property
    def firmware_version(self):
        """(str): the firmware version"""
        return self._idn.firmware_version

    @property
    def mode(self):
        """value (str): {SPECTRUM, SSA}"""
        result = self._visa.query("INSTRUMENT?")
        return Fsup._modes.get(result, result)

    @mode.setter
    @validate
    def mode(self, value):
        modes = dict((v, k) for k, v in Fsup._modes.items())
        if value in modes and value != self._currentmode:
            original_timeout = self._visa.timeout
            self._visa.timeout = 5000  # ms
            if self._currentmode == "SPECTRUM":
                del self.spectrum
            else:
                del self.ssa
            self._currentmode = value
            new_mode = modes[value]
            self._visa.write(f"INSTRUMENT:SELECT {new_mode}")
            if self._currentmode == "SPECTRUM":
                self.spectrum = SpecAn(self)
            else:
                self.ssa = SSA(self)
            self._visa.timeout = original_timeout

    def reset(self):
        """Reset the instrument to the factory default settings"""
        self._visa.write("*RST")

    def set_clock(self):
        """Set the date and time to local machine's time"""
        self._visa.write(f"SYSTEM:DATE {datetime.now().strftime('%Y,%m,%d')}")
        self._visa.write(f"SYSTEM:TIME {datetime.now().strftime('%H,%M,%S')}")

    @property
    def time(self):
        """Return system time"""
        get = lambda x: [int(s) for s in self._visa.query(f"SYSTEM:{x}?").split(",")]
        return datetime(*(get("DATE") + get("TIME")))

    def lock_frontpanel(self):
        """Lock the front panel"""
        self._visa.write("SYSTEM:DISPLAY:FPANEL OFF")
        self._visa.write("SYSTEM:KLOCK ON")

    def unlock_frontpanel(self):
        """Unlock the front panel"""
        self._visa.write("SYSTEM:KLOCK OFF")
        self._visa.write("SYSTEM:DISPLAY:FPANEL ON")

    @property
    def update_display(self):
        """Whether to update the display during remote operation {ON, OFF}"""
        return self._visa.query("SYSTEM:DISPLAY:UPDATE?")

    @update_display.setter
    @validate
    def update_display(self, value):
        self._visa.write(f"SYSTEM:DISPLAY:UPDATE {value}")

    @property
    def options(self):
        """List the installed options"""
        codes = self._visa.query("*OPT?").split(",")
        installed_codes = [code for code in codes if not code.startswith("0")]
        return [Fsup._options.get(code, code) for code in installed_codes]

    @property
    def impedance(self):
        """value (int): RF input impedance {50, 75} Ω"""
        return int(self._visa.query("INPUT:IMPEDANCE?"))

    @impedance.setter
    @validate
    def impedance(self, value):
        self._visa.write(f"INPUT:IMPEDANCE {value}")

    def __repr__(self):
        return f"<R&S {self.model} at {self._visa.resource_name}>"

    def save_settings(self, file):
        """Save the instrument settings to file

        Instrument settings are stored in '.fsp' files located by default in
        'D:\\USER\\CONFIG' and are in a proprietary, non-readable format.

        Parameters:
            file (str): file name, e.g. 'test01.fsp', 'd:\\test01.fsp'
        """
        self._visa.write("MMEMORY:SELECT:DEFAULT")
        file = pathlib.PurePath(file)
        if file.is_absolute():
            self.file_system.drive = file.drive
            self.file_system.directory = str(file.parent)
        else:
            self.file_system.drive = "D:"
            self.file_system.directory = "D:\\USER\\CONFIG"
        self._visa.write(f"MMEMORY:STORE:STATE 1, '{file.stem}'")

    def load_settings(self, file):
        """Load the instrument settings from file

        Instrument settings are stored in '.fsp' files located by default in
        'D:\\USER\\CONFIG' and are in a proprietary, non-readable format.

        Parameters:
            file (str): file name, e.g. 'test01.fsp', 'd:\\test01.fsp'
        """
        file = pathlib.PurePath(file)
        try:
            file = "".join(str(file).split(file.suffix))
        except ValueError:
            file = str(file)
        self._visa.write("*CLS")
        self._visa.write(f"MMEMORY:LOAD:STATE 1, '{file}'; *OPC")
        while not self._visa.stb & 32:
            time.sleep(1)
        if self._visa.stb & 4:
            err = self._visa.query("SYSTEM:ERROR?")
            raise ValueError(err)

    def _write(self, cmd):
        self._visa.write(cmd)

    def _query(self, query):
        return self._visa.query(query)
