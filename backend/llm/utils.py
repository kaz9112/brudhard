import re
from langchain_core.messages import AIMessage

def filter_reasoning_content(message: AIMessage) -> AIMessage:
    if isinstance(message.content, str):
        message.content = re.sub(r"<thought>.*?</thought>", "", message.content, flags=re.DOTALL).strip()
    elif isinstance(message.content, list):
        new_blocks = []
        for block in message.content:
            if isinstance(block, str):
                cleaned_str = re.sub(r"<thought>.*?</thought>", "", block, flags=re.DOTALL).strip()
                if cleaned_str: new_blocks.append(cleaned_str)
            elif isinstance(block, dict):
                if block.get("type") != "reasoning":
                    if "text" in block:
                        block["text"] = re.sub(r"<thought>.*?</thought>", "", block["text"], flags=re.DOTALL).strip()
                    new_blocks.append(block)
        message.content = new_blocks
    if hasattr(message, "additional_kwargs"):
        message.additional_kwargs.pop("reasoning_content", None)
    return message