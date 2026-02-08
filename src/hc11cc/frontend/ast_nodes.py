from dataclasses import dataclass
from typing import List, Union
from enum import Enum, auto


@dataclass
class Type:
    name: str

    def __repr__(self):
        return f"Type({self.name})"


U8 = Type("u8")


@dataclass
class Expr:
    pass


@dataclass
class IntLit(Expr):
    val: int


@dataclass
class Var(Expr):
    name: str


class BinOpKind(Enum):
    ADD = auto()
    SUB = auto()


@dataclass
class BinOp(Expr):
    op: BinOpKind
    lhs: Expr
    rhs: Expr


@dataclass
class Stmt:
    pass


@dataclass
class Let(Stmt):
    name: str
    ty: Type
    init: Expr


@dataclass
class Return(Stmt):
    expr: Expr


@dataclass
class Function:
    name: str
    ret_ty: Type
    body: List[Stmt]


@dataclass
class Program:
    functions: List[Function]
