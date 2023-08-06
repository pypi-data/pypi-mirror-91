from twopilabs.utils.scpi import *
from .x1000_base import SenseX1000Base


class ScpiControl(object):
    """Class containing SCPI commands concerning CONTROL subsystem"""

    def __init__(self, device: ScpiDevice) -> None:
        self.device = device

    def radar_enable(self, onoff: Optional[bool] = None) -> bool:
        """sets/gets whether power to radar subsystem is enabled"""
        if onoff is not None:
            self.device.execute('CONTROL:RADAR:ENABLE', param=ScpiBool(onoff))
        else:
            onoff = self.device.execute('CONTROL:RADAR:ENABLE?', result=ScpiBool).as_bool()

        self.device.raise_error()
        return onoff

    def radar_autopowerup(self, onoff: Optional[bool] = None) -> bool:
        """sets/gets whether radar should be powered-up automatically once power is supplied"""
        if onoff is not None:
            self.device.execute('CONTROL:RADAR:APUP', param=ScpiBool(onoff))
        else:
            onoff = self.device.execute('CONTROL:RADAR:APUP?', result=ScpiBool).as_bool()

        self.device.raise_error()
        return onoff

    def radar_powerup(self) -> None:
        """powers up the radar subsystem from standby state to ready state while power is supplied to frontend"""
        self.device.execute('CONTROL:RADAR:PUP')

    def radar_powerdown(self) -> None:
        """powers down the radar subsystem from ready to standby state while power is supplied to frontend"""
        self.device.execute('CONTROL:RADAR:PDN')

    def radar_status(self) -> SenseX1000Base.RadarStatus:
        """returns the current radar status"""
        status = SenseX1000Base.RadarStatus[self.device.execute('CONTROL:RADAR:STATUS?', result=ScpiChars).as_string()]

        self.device.raise_error()
        return status

    def radar_status_waitoff(self) -> None:
        """Overlapped command to wait for radar status to become OFF"""
        self.device.execute('CONTROL:RADAR:STATUS:WOFF')
        self.device.raise_error()

    def radar_status_waitstandby(self) -> None:
        """Overlapped command to wait for radar status to become STANDBY"""
        self.device.execute('CONTROL:RADAR:STATUS:WSTB')
        self.device.raise_error()

    def radar_status_waitready(self) -> None:
        """Overlapped command to wait for radar status to become READY"""
        self.device.execute('CONTROL:RADAR:STATUS:WRDY')
        self.device.raise_error()

    def radar_mainpll_nint(self, nint: Optional[int] = None) -> int:
        """sets/gets main PLL N divider (integer part)"""
        if nint is not None:
            self.device.execute('CONTROL:RADAR:MPLL:NINT', param=ScpiNumber(nint))
        else:
            nint = self.device.execute('CONTROL:RADAR:MPLL:NINT?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return nint

    def radar_mainpll_nfrac(self, nfrac: Optional[int] = None) -> int:
        """sets/gets main PLL N divider (fractional part)"""
        if nfrac is not None:
            self.device.execute('CONTROL:RADAR:MPLL:NFRAC', param=ScpiNumber(nfrac))
        else:
            nfrac = self.device.execute('CONTROL:RADAR:MPLL:NFRAC?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return nfrac

    def radar_mainpll_rampmode(self, mode: SenseX1000Base.RampMode = None) -> SenseX1000Base.RampMode:
        """sets/gets main PLL ramp mode"""
        if mode is not None:
            self.device.execute('CONTROL:RADAR:MPLL:RMODE', param=ScpiChars(mode.name))
        else:
            mode = SenseX1000Base.RampMode[self.device.execute(
                'CONTROL:RADAR:MPLL:RMODE?', result=ScpiChars).as_string()]

        self.device.raise_error()
        return mode

    def radar_mainpll_rampincr(self, incr: Optional[int] = None, ramp_idx: int = 0) -> int:
        """sets/gets main PLL ramp increment"""
        if incr is not None:
            self.device.execute(f'CONTROL:RADAR:MPLL:RINC{ramp_idx:d}', param=ScpiNumber(incr))
        else:
            incr = self.device.execute(f'CONTROL:RADAR:MPLL:RINC{ramp_idx:d}?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return incr

    def radar_mainpll_ramplen(self, length: Optional[int] = None, ramp_idx: int = 0) -> int:
        """sets/gets main PLL ramp length"""
        if length is not None:
            self.device.execute(f'CONTROL:RADAR:MPLL:RLEN{ramp_idx:d}', param=ScpiNumber(length))
        else:
            length = self.device.execute(f'CONTROL:RADAR:MPLL:RLEN{ramp_idx:d}?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return length

    def radar_mainpll_rampdwell(self, dwell: Optional[int] = None, ramp_idx: int = 0) -> int:
        """sets/gets main PLL ramp dwell"""
        if dwell is not None:
            self.device.execute(f'CONTROL:RADAR:MPLL:RDWELL{ramp_idx:d}', param=ScpiNumber(dwell))
        else:
            dwell = self.device.execute(f'CONTROL:RADAR:MPLL:RDWELL{ramp_idx:d}?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return dwell

    def radar_mainpll_locked(self) -> bool:
        """queries main PLL lock status"""
        locked = self.device.execute('CONTROL:RADAR:MPLL:LOCK?', result=ScpiBool).as_bool()

        self.device.raise_error()
        return locked

    def radar_auxpll_nint(self, nint: Optional[int] = None) -> int:
        """sets/gets aux PLL N divider (integer part)"""
        if nint is not None:
            self.device.execute('CONTROL:RADAR:APLL:NINT', param=ScpiNumber(nint))
        else:
            nint = self.device.execute('CONTROL:RADAR:APLL:NINT?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return nint

    def radar_auxpll_nfrac(self, nfrac: Optional[int] = None) -> int:
        """sets/gets aux PLL N divider (fractional part)"""
        if nfrac is not None:
            self.device.execute('CONTROL:RADAR:APLL:NFRAC', param=ScpiNumber(nfrac))
        else:
            nfrac = self.device.execute('CONTROL:RADAR:APLL:NFRAC?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return nfrac

    def radar_auxpll_locked(self) -> bool:
        """queries main PLL lock status"""
        locked = bool(self.device.execute('CONTROL:RADAR:APLL:LOCK?', result=ScpiBool))

        self.device.raise_error()
        return locked

    def radar_acq_samplecount(self, samplecount: Optional[int] = None) -> int:
        """sets/gets acquisition sample count"""
        if samplecount is not None:
            self.device.execute('CONTROL:RADAR:ACQ:SCOUNT', param=ScpiNumber(samplecount))
        else:
            samplecount = self.device.execute('CONTROL:RADAR:ACQ:SCOUNT?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return samplecount

    def radar_acq_repeatcount(self, repeatcount: Optional[int] = None) -> int:
        """sets/gets acquisition repeat count"""
        if repeatcount is not None:
            self.device.execute('CONTROL:RADAR:ACQ:RCOUNT', param=ScpiNumber(repeatcount))
        else:
            repeatcount = self.device.execute('CONTROL:RADAR:ACQ:RCOUNT?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return repeatcount

    def radar_acq_repeatperiod(self, repeatperiod: Optional[int] = None) -> int:
        """sets/gets acquisition repeat period"""
        if repeatperiod is not None:
            self.device.execute('CONTROL:RADAR:ACQ:RPERIOD', param=ScpiNumber(repeatperiod))
        else:
            repeatperiod = self.device.execute('CONTROL:RADAR:ACQ:RPERIOD?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return repeatperiod

    def radar_frontend_enable(self, enabled: Optional[bool] = None, chan_idx: int = 0) -> bool:
        """enables/disables radar frontend channel"""
        if enabled is not None:
            self.device.execute(f'CONTROL:RADAR:FRONTEND:CHANNEL{chan_idx:d}:ENABLE', param=ScpiBool(enabled))
        else:
            enabled = self.device.execute(
                f'CONTROL:RADAR:FRONTEND:CHANNEL{chan_idx:d}:ENABLE?', result=ScpiBool).as_bool()

        self.device.raise_error()
        return enabled

    def radar_frontend_force(self, force: Optional[SenseX1000Base.ChannelForce] = None,
                             chan_idx: int = 0) -> SenseX1000Base.ChannelForce:
        """sets/gets radar frontend channel force on/off"""
        if force is not None:
            self.device.execute(f'CONTROL:RADAR:FRONTEND:CHANNEL{chan_idx:d}:FORCE', param=ScpiChars(force.name))
        else:
            force = SenseX1000Base.ChannelForce[self.device.execute(
                f'CONTROL:RADAR:FRONTEND:CHANNEL{chan_idx:d}:FORCE?', result=ScpiChars).as_string()]

        self.device.raise_error()
        return force

    def radar_frontend_power(self, power: Optional[int] = None, chan_idx: int = 0) -> int:
        """sets/gets radar frontend channel TX power"""
        if power is not None:
            self.device.execute(f'CONTROL:RADAR:FRONTEND:CHANNEL{chan_idx:d}:POWER', param=ScpiNumber(power))
        else:
            power = self.device.execute(
                f'CONTROL:RADAR:FRONTEND:CHANNEL{chan_idx:d}:POWER?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return power

    def radar_frontend_coupling(self, coupling: Optional[SenseX1000Base.ChannelCoupling] = None,
                                chan_idx: int = 0) -> SenseX1000Base.ChannelCoupling:
        """sets/gets radar frontend channel coupling"""
        if coupling is not None:
            self.device.execute(f'CONTROL:RADAR:FRONTEND:CHANNEL{chan_idx:d}:COUPLING', param=ScpiChars(coupling.name))
        else:
            coupling = SenseX1000Base.ChannelCoupling[self.device.execute(
                f'CONTROL:RADAR:FRONTEND:CHANNEL{chan_idx:d}:COUPLING?', result=ScpiChars).as_string()]

        self.device.raise_error()
        return coupling

    def accessory_enable(self, onoff: Optional[bool] = None) -> bool:
        """Enable or disable power to the device accessory"""
        if onoff is not None:
            self.device.execute('CONTROL:ACCESSORY:ENABLE', param=ScpiBool(onoff))
        else:
            onoff = self.device.execute('CONTROL:ACCESSORY:ENABLE?', result=ScpiBool).as_bool()

        self.device.raise_error()
        return onoff

    def accessory_rgb_slot(self, slot_num: Optional[int] = None) -> int:
        """Select or get currently selected setting slot for RGB accessory"""
        if slot_num is not None:
            self.device.execute('CONTROL:ACCESSORY:RGB:SLOT:NUM', param=ScpiNumber(slot_num))
        else:
            slot_idx = self.device.execute('CONTROL:ACCESSORY:RGB:SLOT:NUM?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return slot_num

    def accessory_rgb_hue_value(self, value: Optional[float] = None, slot_num: Optional[int] = None) -> float:
        """Set or get HSB hue value for RGB accessory. If no slot is given, current slot is used."""
        if value is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:VALUE', param=ScpiNumber(value))
        else:
            value = self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:VALUE?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return value

    def accessory_rgb_hue_rate(self, rate: Optional[float] = None, slot_num: Optional[int] = None) -> float:
        """Set or get HSB hue animation rate for RGB accessory. If no slot is given, current slot is used."""
        if rate is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:RATE', param=ScpiNumber(rate))
        else:
            rate = self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:RATE?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return rate

    def accessory_rgb_hue_table_data(self, table_data: Optional[bytes] = None, slot_num: Optional[int] = None) -> bytes:
        """Sets or returns lookup table data"""
        if table_data is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:TABLE:DATA', param=ScpiArbBlock(table_data))
        else:
            table_data = self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:TABLE:DATA?', result=ScpiArbBlock).as_bytes()

        self.device.raise_error()
        return table_data

    def accessory_rgb_hue_table_length(self, slot_num: Optional[int] = None) -> int:
        """Returns the length of the lookup table"""
        table_len = self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:TABLE:LENGTH?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return table_len

    def accessory_rgb_hue_tap_data(self, tap_data: Optional[Iterable[float]] = None, slot_num: Optional[int] = None) -> Iterable[float]:
        """Sets or returns a list of tap indices to the lookup table"""
        if tap_data is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:TAP:DATA', param=ScpiNumberArray(tap_data))
        else:
            tap_data = self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:TAP:DATA?', result=ScpiNumberArray).as_float_list()

        self.device.raise_error()
        return tap_data

    def accessory_rgb_hue_tap_count(self, slot_num: Optional[int] = None) -> int:
        """Returns the number of taps supported in the system"""
        tap_count = self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:TAP:COUNT?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return tap_count

    def accessory_rgb_hue_tap_spread(self, tap_spread: Optional[float] = None, slot_num: Optional[int] = None) -> None:
        """Sets the tap index table by evenly spreading out taps across all available taps"""
        self.device.execute(f'CONTROL:ACCESSORY:RGB:HUE{slot_num or ""}:TAP:SPREAD', param=ScpiNumber(tap_spread))

        self.device.raise_error()
        return None

    def accessory_rgb_sat_value(self, value: Optional[float] = None, slot_num: Optional[int] = None) -> float:
        """Set or get HSB hue value for RGB accessory. If no slot is given, current slot is used."""
        if value is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:VALUE', param=ScpiNumber(value))
        else:
            value = self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:VALUE?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return value

    def accessory_rgb_sat_rate(self, rate: Optional[float] = None, slot_num: Optional[int] = None) -> float:
        """Set or get HSB hue animation rate for RGB accessory. If no slot is given, current slot is used."""
        if rate is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:RATE', param=ScpiNumber(rate))
        else:
            rate = self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:RATE?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return rate

    def accessory_rgb_sat_table_data(self, table_data: Optional[bytes] = None, slot_num: Optional[int] = None) -> bytes:
        """Sets or returns lookup table data"""
        if table_data is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:TABLE:DATA', param=ScpiArbBlock(table_data))
        else:
            table_data = self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:TABLE:DATA?', result=ScpiArbBlock).as_bytes()

        self.device.raise_error()
        return table_data

    def accessory_rgb_sat_table_length(self, slot_num: Optional[int] = None) -> int:
        """Returns the length of the lookup table"""
        table_len = self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:TABLE:LENGTH?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return table_len

    def accessory_rgb_sat_tap_data(self, tap_data: Optional[Iterable[float]] = None, slot_num: Optional[int] = None) -> Iterable[float]:
        """Sets or returns a list of tap indices to the lookup table"""
        if tap_data is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:TAP:DATA', param=ScpiNumberArray(tap_data))
        else:
            tap_data = self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:TAP:DATA?', result=ScpiNumberArray).as_float_list()

        self.device.raise_error()
        return tap_data

    def accessory_rgb_sat_tap_count(self, slot_num: Optional[int] = None) -> int:
        """Returns the number of taps supported in the system"""
        tap_count = self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:TAP:COUNT?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return tap_count

    def accessory_rgb_sat_tap_spread(self, tap_spread: Optional[float] = None, slot_num: Optional[int] = None) -> None:
        """Sets the tap index table by evenly spreading out taps across all available taps"""
        self.device.execute(f'CONTROL:ACCESSORY:RGB:SAT{slot_num or ""}:TAP:SPREAD', param=ScpiNumber(tap_spread))

        self.device.raise_error()
        return None

    def accessory_rgb_brightness_value(self, value: Optional[float] = None, slot_num: Optional[int] = None) -> float:
        """Set or get HSB hue value for RGB accessory. If no slot is given, current slot is used."""
        if value is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:VALUE', param=ScpiNumber(value))
        else:
            value = self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:VALUE?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return value

    def accessory_rgb_brightness_rate(self, rate: Optional[float] = None, slot_num: Optional[int] = None) -> float:
        """Set or get HSB hue animation rate for RGB accessory. If no slot is given, current slot is used."""
        if rate is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:RATE', param=ScpiNumber(rate))
        else:
            rate = self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:RATE?', result=ScpiNumber).as_float()

        self.device.raise_error()
        return rate

    def accessory_rgb_brightness_table_data(self, table_data: Optional[bytes] = None, slot_num: Optional[int] = None) -> bytes:
        """Sets or returns lookup table data"""
        if table_data is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:TABLE:DATA', param=ScpiArbBlock(table_data))
        else:
            table_data = self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:TABLE:DATA?', result=ScpiArbBlock).as_bytes()

        self.device.raise_error()
        return table_data

    def accessory_rgb_brightness_table_length(self, slot_num: Optional[int] = None) -> int:
        """Returns the length of the lookup table"""
        table_len = self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:TABLE:LENGTH?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return table_len

    def accessory_rgb_brightness_tap_data(self, tap_data: Optional[Iterable[float]] = None, slot_num: Optional[int] = None) -> Iterable[float]:
        """Sets or returns a list of tap indices to the lookup table"""
        if tap_data is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:TAP:DATA', param=ScpiNumberArray(tap_data))
        else:
            tap_data = self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:TAP:DATA?', result=ScpiNumberArray).as_float_list()

        self.device.raise_error()
        return tap_data

    def accessory_rgb_brightness_tap_count(self, slot_num: Optional[int] = None) -> int:
        """Returns the number of taps supported in the system"""
        tap_count = self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:TAP:COUNT?', result=ScpiNumber).as_int()

        self.device.raise_error()
        return tap_count

    def accessory_rgb_brightness_tap_spread(self, tap_spread: Optional[float] = None, slot_num: Optional[int] = None) -> None:
        """Sets the tap index table by evenly spreading out taps across all available taps"""
        self.device.execute(f'CONTROL:ACCESSORY:RGB:BRIGHTNESS{slot_num or ""}:TAP:SPREAD', param=ScpiNumber(tap_spread))

        self.device.raise_error()
        return None

    def accessory_rgb_hsb_value(self, hsb_value: Optional[Iterable[float]] = None, slot_num: Optional[int] = None) -> Iterable[float]:
        """Set or get Hue-Saturation-Brightness (HSB aka HSV) value triplet in one command."""
        if hsb_value is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:HSB{slot_num or ""}:VALUE', param=ScpiNumberArray(hsb_value))
        else:
            hsb_value = self.device.execute(f'CONTROL:ACCESSORY:RGB:HSB{slot_num or ""}:VALUE?', result=ScpiNumberArray).as_float_list()

        self.device.raise_error()
        return hsb_value

    def accessory_rgb_hsb_rate(self, hsb_rate: Optional[Iterable[float]] = None, slot_num: Optional[int] = None) -> Iterable[float]:
        """Set or get Hue-Saturation-Brightness (HSB aka HSV) rate triplet in one command."""
        if hsb_rate is not None:
            self.device.execute(f'CONTROL:ACCESSORY:RGB:HSB{slot_num or ""}:RATE', param=ScpiNumberArray(hsb_rate))
        else:
            hsb_rate = self.device.execute(f'CONTROL:ACCESSORY:RGB:HSB{slot_num or ""}:RATE?', result=ScpiNumberArray).as_float_list()

        self.device.raise_error()
        return hsb_rate
