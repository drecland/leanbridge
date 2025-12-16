from typing import List, Optional
from .lexer import LeanLexer, Token

class LeanToPythonConverter:
    """
    Parses Lean code tokens and generates `LeanBridge` Python code.
    Follows a recursive descent-like pattern but simplified for "flat" files
    declarations.
    """
    def __init__(self):
        self.lexer = LeanLexer()
        self.tokens: List[Token] = []
        self.pos = 0
        self.indent_level = 0
        self.python_lines = []

    def convert(self, lean_code: str) -> str:
        self.tokens = self.lexer.tokenize(lean_code)
        self.pos = 0
        self.indent_level = 0
        self.python_lines = []
        
        self._emit_header()
        
        while self.pos < len(self.tokens):
            token = self._peek()
            if not token: 
                break
                
            if token.type == 'KEYWORD':
                if token.value in ('namespace', 'section'):
                    self._parse_scope()
                elif token.value == 'end':
                    self._parse_end()
                elif token.value == 'structure':
                    self._parse_structure()
                elif token.value == 'def':
                    self._parse_def(is_computable=True)
                elif token.value == 'noncomputable':
                    self._consume('KEYWORD') # noncomputable
                    if self._check('KEYWORD', 'def'):
                        self._parse_def(is_computable=False)
                    else:
                        # Fallback or other noncomputable things
                        self._emit_comment(f"Skipped noncomputable {self._peek().value}")
                        self._advance()
                elif token.value in ('lemma', 'theorem'):
                    self._parse_claim()
                elif token.value == 'variable':
                    self._parse_variable()
                else:
                    self._advance()
            else:
                 self._advance()
                 
        return "\n".join(self.python_lines)

    def _emit_header(self):
        self.python_lines.append("from leanbridge import LeanBridgeInterpreter, MScalar, MStructure")
        self.python_lines.append("from leanbridge.actions.commands import ActionDeclare, ActionClaim, ActionSolve, ActionDefine")
        self.python_lines.append("")
        self.python_lines.append("bridge = LeanBridgeInterpreter()")
        self.python_lines.append("")

    def _emit(self, line: str):
        indent = "    " * self.indent_level
        self.python_lines.append(f"{indent}{line}")
        
    def _emit_comment(self, text: str):
        self._emit(f"# {text}")

    def _peek(self, offset=0) -> Optional[Token]:
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def _advance(self):
        self.pos += 1

    def _consume(self, type_name: str, value: str = None) -> Optional[Token]:
        token = self._peek()
        if token and token.type == type_name:
            if value is None or token.value == value:
                self.pos += 1
                return token
        return None
    
    def _check(self, type_name: str, value: str = None) -> bool:
        token = self._peek()
        if token and token.type == type_name:
            if value is None or token.value == value:
                return True
        return False

    def _parse_scope(self):
        # namespace Foo
        kind_tok = self._consume('KEYWORD') # namespace or section
        name_tok = self._consume('ID')
        name = name_tok.value if name_tok else ""
        
        scope_method = "Namespace" if kind_tok.value == 'namespace' else "Section"
        self._emit(f"with bridge.{scope_method}(\"{name}\"):")
        self.indent_level += 1

    def _parse_end(self):
        # end Foo
        self._consume('KEYWORD') # end
        self._consume('ID') # optional name
        
        if self.indent_level > 0:
            self.indent_level -= 1
        
    def _parse_structure(self):
        # structure Point where
        #   x : Float
        #   y : Float
        self._consume('KEYWORD', 'structure')
        id_tok = self._consume('ID')
        name = id_tok.value if id_tok else "UnknownStruct"
        
        # Optional 'where'
        if self._check('KEYWORD', 'where'):
            self._consume('KEYWORD', 'where')
            
        # Parse fields until we hit a keyword that starts a new block or end tokens
        # Heuristic: fields look like ID : Type
        fields = {}
        
        while True:
            # Check stopping conditions
            if self._check('KEYWORD'):
                # 'end' or start of another definition
                break
            if not self._peek():
                break
                
            # Expecting ID or (ID : Type) or just ID
            # Simple parser: look for ID : Type
            f_name = self._consume('ID')
            if not f_name:
                # Could be parenthesis or other things we ignore for now
                self._advance()
                continue
                
            if self._check('COLON'):
                self._consume('COLON')
                # Read type until newline or next field
                # Very naive type grabbing: just grab the next ID or simple expression
                f_type_tok = self._consume('ID')
                f_type = f_type_tok.value if f_type_tok else "Any"
                fields[f_name.value] = f_type
            else:
                # Maybe just a field name ?
                pass
                
        # Emit code
        # bridge.define_structure("Point", {"x": "Float", ...})
        fields_str = str(fields)
        self._emit(f"bridge.define_structure(\"{name}\", {fields_str})")

    def _parse_variable(self):
        # variable (x : Real)
        self._consume('KEYWORD', 'variable')
        
        # (x : Real)
        # We need to extract x and Real
        # Simple loop to consume until closing paren
        if self._check('LPAREN'):
            self._consume('LPAREN')
            var_name = self._consume('ID')
            self._consume('COLON')
            var_type = self._consume('ID')
            self._consume('RPAREN')
            
            if var_name and var_type:
                # bridge.add_action(ActionDeclare("x", MScalar("Real")))
                # We assume simple scalar for now
                self._emit(f"bridge.add_action(ActionDeclare(\"{var_name.value}\", MScalar(\"{var_type.value}\")))")

    def _parse_def(self, is_computable: bool):
        # def square (n : Nat) : Nat := n * n
        self._consume('KEYWORD', 'def') 
        name_tok = self._consume('ID')
        name = name_tok.value if name_tok else "unknown"
        
        # Args
        args = []
        while self._check('LPAREN'):
            # (n : Nat)
            # A bit sloppy: capture everything as string until RPAREN
            self._consume('LPAREN')
            arg_content = []
            while not self._check('RPAREN') and self._peek():
                arg_content.append(self._peek().value)
                self._advance()
            self._consume('RPAREN')
            
            # Reconstruct (n : Nat)
            full_arg = "(" + " ".join(arg_content) + ")"
            # clean up spaces
            full_arg = full_arg.replace(" : ", " : ") 
            args.append(full_arg)

        # Return type
        ret_type = None
        if self._check('COLON'):
            self._consume('COLON')
            rt_tok = self._consume('ID')
            if rt_tok: ret_type = rt_tok.value

        # Body := ...
        body = "sorry"
        if self._check('ASSIGN'):
            self._consume('ASSIGN')
            # Consume until next keyword or EOF?
            # Creating a robust body parser is hard.
            # We will read until newline that looks like it ends the def specific logic
            # OR just grab a few tokens. 
            # For this simplified version, let's grab everything until end of line ??
            # Actually Lean definitions can span multiple lines.
            # We will act as a 'dumb' parser that reads until it sees a new top-level keyword at start of line
            # But we don't have line info easily here in token stream (we do have line logic in lexer, but flattened here).
            # Let's take a simple heuristic: read until implicit end?
            
            # Simple approach: Read tokens until we hit a KEYWORD that is usually top-level
            # (namespace, section, end, structure, def, lemma, theorem, class, variable)
            # CAREFUL: 'if' 'let' 'match' are keywords too but inside def.
            # Our lexer only tags specific keywords as KEYWORD. 
            # So if we hit one of OUR keywords, we stop.
            
            body_parts = []
            while self._peek():
                if self._check('KEYWORD'):
                    # is it a top level keyword?
                    # The lexer KEYWORD list is mostly top-level. 
                    # 'where' is used in structure, 'extends' in structure/class.
                    # We might stop prematurely if 'def' uses 'where' (e.g. mutual).
                    # Reasonable assumption for LeanBridge subset: simple defs.
                    break
                
                tok = self._peek()
                body_parts.append(tok.value)
                self._advance()
                
            body = " ".join(body_parts)
            
        # Emit
        # bridge.add_action(ActionDefine("square", "n * n", args=["(n : Nat)"], type_hint="Nat", is_computable=True))
        args_str = str(args)
        rt_str = f"\"{ret_type}\"" if ret_type else "None"
        body_esc = f"\"{body}\""
        
        self._emit(f"bridge.add_action(ActionDefine(\"{name}\", {body_esc}, args={args_str}, type_hint={rt_str}, is_computable={is_computable}))")

    def _parse_claim(self):
        # lemma foo : x > 0 := by sorry
        self._consume('KEYWORD') # lemma/theorem
        name_tok = self._consume('ID')
        name = name_tok.value if name_tok else "anon"
        
        self._consume('COLON')
        
        # Statement: read until :=
        stmt_parts = []
        while self._peek() and not self._check('ASSIGN'):
            stmt_parts.append(self._peek().value)
            self._advance()
        statement = " ".join(stmt_parts)
        
        # Emit claim
        self._emit(f"bridge.add_action(ActionClaim(\"{name}\", \"{statement}\"))")
        
        # Body (Proof)
        if self._check('ASSIGN'):
            self._consume('ASSIGN')
            
            # Check for 'by'
            # Lexer doesn't have 'by' as keyword yet, it's ID
            if self._check('ID', 'by'):
                self._consume('ID', 'by')
                
                # Check method
                method_tok = self._consume('ID') # sorry, simp, etc.
                method = method_tok.value if method_tok else "sorry"
                
                self._emit(f"bridge.add_action(ActionSolve(\"{method}\"))")
            else:
                 # consume rest as body?
                 pass
