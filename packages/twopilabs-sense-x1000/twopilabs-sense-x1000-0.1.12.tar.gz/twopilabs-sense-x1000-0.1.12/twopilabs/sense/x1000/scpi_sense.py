from twopilabs.utils.scpi import *
from .x1000_base import SenseX1000Base
import yaml


class ScpiSense(object):
    """Class containing SCPI commands concerning SENSE subsystem"""

    def __init__(self, device: ScpiDevice) -> None:
        self.device = device

    def dump(self) -> dict:
        """returns a configuration dictionary"""
        config = self.device.execute('SENSE:DUMP?', result=ScpiString).as_bytes()

        self.device.raise_error()
        return yaml.load(config, Loader=yaml.FullLoader)

    def frequency_cw(self, freq: Optional[float] = None) -> float:
        """Sets or gets CW frequency"""
        if freq is not None:
            self.device.execute('SENSE:FREQ:CW', param=ScpiNumber(freq, unit='HZ'))
        else:
            freq = self.device.execute('SENSE:FREQ:CW?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return freq

    def frequency_start(self, freq: Optional[float] = None) -> float:
        """Sets or gets sweep start frequency"""
        if freq is not None:
            self.device.execute('SENSE:FREQ:START', param=ScpiNumber(freq, unit='HZ'))
        else:
            freq = self.device.execute('SENSE:FREQ:START?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return freq

    def frequency_stop(self, freq: Optional[float] = None) -> float:
        """Sets or gets sweep stop frequency"""
        if freq is not None:
            self.device.execute('SENSE:FREQ:STOP', param=ScpiNumber(freq, unit='HZ'))
        else:
            freq = self.device.execute('SENSE:FREQ:STOP?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return freq

    def frequency_center(self, freq: Optional[float] = None) -> float:
        """Sets or gets sweep center frequency. Modifies sweep frequency span to stay within allowed limits"""
        if freq is not None:
            self.device.execute('SENSE:FREQ:CENTER', param=ScpiNumber(freq, unit='HZ'))
        else:
            freq = self.device.execute('SENSE:FREQ:CENTER?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return freq

    def frequency_span(self, freq: Optional[float] = None) -> float:
        """Sets or gets sweep frequency span. Modifies sweep center frequency to stay within allowed limits.

        Frequency span may be either positive or negative. A negative value automatically causes the SENSE:SWEEP
        subsystem to report a downslope.
        Frequency span will be negative when stop frequency is smaller than start frequency.
        """
        if freq is not None:
            self.device.execute('SENSE:FREQ:SPAN', param=ScpiNumber(freq, unit='HZ'))
        else:
            freq = self.device.execute('SENSE:FREQ:SPAN?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return freq

    def frequency_mode(self, mode: Optional[SenseX1000Base.FrequencyMode] = None) -> SenseX1000Base.FrequencyMode:
        """Sets or gets sweep frequency mode (CW or SWEEP)"""
        if mode is not None:
            self.device.execute('SENSE:FREQ:MODE', param=ScpiChars(mode.name))
        else:
            mode = SenseX1000Base.FrequencyMode[(self.device.execute('SENSE:FREQ:MODE?', result=ScpiChars)).as_string()]

        self.device.raise_error()
        return mode

    def sweep_points(self, points: Optional[int] = None) -> int:
        """Sets or gets number of points per sweep. Modifies sweep time to achieve the system sample-rate"""
        if points is not None:
            self.device.execute('SENSE:SWEEP:POINTS', param=ScpiNumber(points))
        else:
            points = self.device.execute('SENSE:SWEEP:POINTS?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return points

    def sweep_time(self, time: Optional[float] = None) -> float:
        """Sets or gets the sweep duration. Modifies points per sweep to achieve the system sample-rate"""
        if time is not None:
            self.device.execute('SENSE:SWEEP:TIME', param=ScpiNumber(time, unit='S'))
        else:
            time = self.device.execute('SENSE:SWEEP:TIME?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return time

    def sweep_direction(self,
                        direction: Optional[SenseX1000Base.SweepDirection] = None) -> SenseX1000Base.SweepDirection:
        """Sets or gets the sweep slope of first sweep in acquisition"""
        if direction is not None:
            self.device.execute('SENSE:SWEEP:DIRECTION', param=ScpiChars(direction.name))
        else:
            direction = SenseX1000Base.SweepDirection[self.device.execute(
                'SENSE:SWEEP:DIRECTION?', result=ScpiChars).as_string()]

        self.device.raise_error()
        return direction

    def sweep_mode(self, mode: Optional[SenseX1000Base.SweepMode] = None) -> SenseX1000Base.SweepMode:
        """Sets or gets the sweep mode (SINGLE or ALTERNATING)"""
        if mode is not None:
            self.device.execute('SENSE:SWEEP:MODE', param=ScpiChars(mode.name))
        else:
            mode = SenseX1000Base.SweepMode[self.device.execute('SENSE:SWEEP:MODE?', result=ScpiChars).as_string()]

        self.device.raise_error()
        return mode

    def sweep_count(self, count: Optional[int] = None) -> int:
        """Sets or gets the number of sweeps in an acquisition (single trigger event)"""
        if count is not None:
            self.device.execute('SENSE:SWEEP:COUNT', param=ScpiNumber(count))
        else:
            count = self.device.execute('SENSE:SWEEP:COUNT?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return count

    def sweep_period(self, period: Optional[float] = None) -> float:
        """Sets or getss the sweep period for multi-sweep acquisitions"""
        if period is not None:
            self.device.execute('SENSE:SWEEP:PERIOD', param=ScpiNumber(period, unit='S'))
        else:
            period = self.device.execute('SENSE:SWEEP:PERIOD?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return period
