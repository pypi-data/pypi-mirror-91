from typing import NamedTuple, Optional

from .const import *
from .oven_cook_mode import OvenCookMode 

class OvenCookSetting(NamedTuple):
    """Cleaner representation of ErdOvenCookMode"""
    cook_mode: OvenCookMode
    temperature: int
    raw_bytes: Optional[bytes] = None

    def stringify(self, **kwargs) -> Optional[str]:
        """Format OvenCookSetting values nicely."""
        cook_state = self.cook_mode.oven_state
        temp_units = kwargs.get("temp_units", "°")

        modifiers = []
        if self.cook_mode.timed:
            modifiers.append(STATE_OVEN_TIMED)
        if self.cook_mode.delayed:
            modifiers.append(STATE_OVEN_DELAY)
        if self.cook_mode.probe:
            modifiers.append(STATE_OVEN_PROBE)
        if self.cook_mode.sabbath:
            modifiers.append(STATE_OVEN_SABBATH)

        temp_str = f" ({self.temperature}{temp_units})" if self.temperature > 0 else ""
        modifier_str = f" ({', '.join(modifiers)})" if modifiers else ""
        display_state = cook_state.stringify(**kwargs)

        if display_state in [STATE_OVEN_UNKNOWN, STATE_OVEN_OFF]:
            return display_state
            
        return f"{display_state}{temp_str}{modifier_str}"
    def __str__(self) -> str:
        return self.stringify() or ""
