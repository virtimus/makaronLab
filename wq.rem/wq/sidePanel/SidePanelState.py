
'''
enum class SidePanelState {
    Opening = 0,
    Opened,
    Closing,
    Closed
};

const char* to_str(const SidePanelState state);
'''

from enum import Enum


class SidePanelState(Enum):
    Opening = 0
    Opened = 1
    Closing = 2
    Closed = 3