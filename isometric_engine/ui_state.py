from dataclasses import dataclass

@dataclass
class UIState:
    console_out: bool = False
    debug_text_out: bool = False
