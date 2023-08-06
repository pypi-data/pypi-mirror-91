"""
the module to list constants used in given problems (e.g. 1000000007)

この module は問題中で使われている定数を列挙します。
この機能の実装は `kyuridenamida/atcoder-tools <https://github.com/kyuridenamida/atcoder-tools>`_ を参考にしています。

たとえば `Educational Codeforces Round 83: D. Count the Arrays <https://codeforces.com/contest/1312/problem/D>`_ に対しては
::

    {
        "MOD": 998244353,
    }

に相当する結果を返します。

MOD の値や YES / NO の文字列は間違えやすいため、この機能は便利です。
1000000007 でなく 10000000009 が使われていることに気付かず WA を出す、``Impossible`` と出力すべきところを ``impossible`` と出力してしまい WA になる、などの事態を防げます。
"""

import re
from logging import getLogger
from typing import *

from onlinejudge_template.types import *

logger = getLogger(__name__)


def list_constants_from_html(html: bytes) -> Dict[VarName, ConstantDecl]:
    replace = [
        ("\\", ""),
        ("{", ""),
        ("}", ""),
        (",", ""),
        ("'", ""),
        (" ^ ", "^"),
        (" + ", "+"),
        ("10^9+7", "1000000007"),
        ("10^9+9", "1000000009"),
    ]
    normalized = html.decode()
    for a, b in replace:
        normalized = normalized.replace(a, b)

    mod: Set[int] = set()
    for value in (10**9 + 7, 10**9 + 9, 998244353):
        if re.search(r'\b' + re.escape(str(value)) + r'\b', normalized):
            mod.add(value)

    constants: Dict[VarName, ConstantDecl] = {}
    if len(mod) == 1:
        constants[VarName('MOD')] = ConstantDecl(name=VarName('MOD'), type=VarType.ValueInt, value=Expr(str(mod.pop())))
    elif len(mod) >= 2:
        logger.error('too many MOD-like integers found: %s', mod)
    return constants


def list_constants_from_sample_cases(sample_cases: List[SampleCase]) -> Dict[VarName, ConstantDecl]:
    yes: Set[str] = set()
    no: Set[str] = set()
    first: Set[str] = set()
    second: Set[str] = set()
    for case in sample_cases:
        for token in case.output.decode().split():
            if token.lower() in ("yes", "possible"):
                yes.add(token)
            if token.lower() in ("no", "impossible"):
                no.add(token)
            if token.lower() in ("first", "alice"):
                first.add(token)
            if token.lower() in ("second", "bob"):
                second.add(token)
    logger.debug('YES-like strings: %s', yes)
    logger.debug('NO-like strings: %s', no)
    logger.debug('Alice-like strings: %s', first)
    logger.debug('Bob-like strings: %s', second)

    constants: Dict[VarName, ConstantDecl] = {}
    if len(yes) == 1:
        constants[VarName('YES')] = ConstantDecl(name=VarName('YES'), type=VarType.String, value=yes.pop())
    if len(no) == 1:
        constants[VarName('NO')] = ConstantDecl(name=VarName('NO'), type=VarType.String, value=no.pop())
    if len(first) == 1:
        constants[VarName('FIRST')] = ConstantDecl(name=VarName('FIRST'), type=VarType.String, value=first.pop())
    if len(second) == 1:
        constants[VarName('SECOND')] = ConstantDecl(name=VarName('SECOND'), type=VarType.String, value=second.pop())
    return constants


def list_constants(*, html: Optional[bytes], sample_cases: Optional[List[SampleCase]]) -> Dict[VarName, ConstantDecl]:
    constants = {}
    if html is not None:
        constants.update(list_constants_from_html(html))
    if sample_cases is not None:
        constants.update(list_constants_from_sample_cases(sample_cases))
    return constants
