
import json
from pathlib import Path


CHECKPOINTS_PATH=Path("data/checkpoints.json")


def load_checkpoints() -> list[dict]:
    with open(CHECKPOINTS_PATH,"r",encoding="utf-8") as f:
        return json.load(f)
    
def get_all_checkpoints() -> list[dict]:
    return sorted(load_checkpoints,key=lambda item:item["order_index"])


def get_checkpoint_by_key(checkpoint_key:str) -> dict | None:
    for checkpoint in load_checkpoints():
        if checkpoint["checkpoint_key"] == checkpoint_key:
            return checkpoint
    return None

def  get_checkpoint_by_order(order_index:int) -> dict|None:
    for checkpoint in load_checkpoints():
        if checkpoint["order_index"] == order_index:
            return checkpoint
    return None

def get_next_checkpoint(current_order_index:int) -> dict|None:
    return get_checkpoint_by_order(current_order_index+1)       