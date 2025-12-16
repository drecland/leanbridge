import re
from typing import NamedTuple, List, Optional

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

class LeanLexer:
    """
    Simplex regex-based lexer for a subset of Lean 4.
    """
    
    TOKEN_SPEC = [
        ('COMMENT', r'--.*'), # Single line comment
        ('STRING', r'"(?:[^"\\]|\\.)*"'), # String literal
        ('NUMBER', r'\d+(\.\d+)?'),
        ('ARROW', r'->'),
        ('GE', r'>='),
        ('LE', r'<='),
        ('NE', r'!='),
        ('KEYWORD', r'\b(namespace|section|end|structure|def|lemma|theorem|class|variable|where|extends|instance|noncomputable)\b'),
        ('ASSIGN', r':='),
        ('COLON', r':'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('PIPE', r'\|'),
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_\']*'),
        ('SKIP', r'[ \t]+'), # Skip spaces and tabs
        ('NEWLINE', r'\n'),
        ('MISMATCH', r'.'), # Any other character
    ]

    def __init__(self):
        self.regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.TOKEN_SPEC)
        self.re_token = re.compile(self.regex)

    def tokenize(self, code: str) -> List[Token]:
        tokens = []
        line_num = 1
        line_start = 0
        
        for mo in self.re_token.finditer(code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            
            if kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                # Simplified error handling: treat as part of random text if needed, 
                # but for now let's just create a generic token or raise error.
                # LeanBridgeReverse needs to be robust, so maybe just 'SYMBOL'?
                # For now let's keep it robust and add it as 'SYMBOL' or similar if needed.
                # Actually, definitions bodies can contain anything.
                # Let's emit a 'MISC' token for symbols like +, *, etc if not defined.
                tokens.append(Token('MISC', value, line_num, column))
            else:
                tokens.append(Token(kind, value, line_num, column))
                
        return tokens
