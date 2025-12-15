from typing import List, Dict
from .commands import Action
from ..inference.context import ContextManager
from ..inference.mapper import LibraryMapper
from ..core.objects import MStructure, MInductive

class ActionDefineStructure(Action):
    def __init__(self, struct_obj: MStructure):
        self.struct = struct_obj

    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        lines = [f"structure {self.struct.name} where"]
        for field, ftype in self.struct.fields.items():
            # Mapper le type si possible
            clean_type = mapper.get_lean_name(ftype)
            lines.append(f"  {field} : {clean_type}")
        return "\n".join(lines)

class ActionDefineInductive(Action):
    def __init__(self, ind_obj: MInductive):
        self.ind = ind_obj

    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        lines = [f"inductive {self.ind.name}"]
        for c in self.ind.constructors:
            lines.append(f"| {c}")
        return "\n".join(lines)
