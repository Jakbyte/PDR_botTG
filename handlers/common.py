from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup


class SearchStates(StatesGroup):
    searching_fabula = State()
    searching_kupap_number = State()
    searching_npu_number = State()


async def send_long_message(message: Message, text: str, chunk_size: int = 4096, parse_mode: str = None):
    if len(text) <= chunk_size:
        await message.answer(text, parse_mode=parse_mode)
        return
    lines = text.split('\n')
    current_chunk = ""
    for line in lines:
        if len(current_chunk) + len(line) + 1 > chunk_size:
            await message.answer(current_chunk, parse_mode=parse_mode)
            current_chunk = line
        else:
            current_chunk = current_chunk + "\n" + line if current_chunk else line
    if current_chunk:
        await message.answer(current_chunk, parse_mode=parse_mode)
