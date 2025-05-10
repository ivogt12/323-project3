from lexer import lexer
from semantics import Semantics

class Parser:
    def __init__(self, input_file):
        self.fp = open(input_file, 'r')
        self.semantics = Semantics()
        self.current_token, self.current_lexeme = None, None
        self.next_token()  # Initialize first token
    
    def next_token(self):
        """Advance to the next token from lexer"""
        self.current_token, self.current_lexeme = lexer(self.fp)
        # print(f"Token: {self.current_token:14} Lexeme: {self.current_lexeme}")

    def match(self, expected_token, expected_lexeme=None):
        """Verify current token matches expected and advance"""
        if (self.current_token != expected_token or 
            (expected_lexeme and self.current_lexeme != expected_lexeme)):
            raise SyntaxError(
                f"Expected {expected_token}/{expected_lexeme}, "
                f"got {self.current_token}/{self.current_lexeme}"
            )
        self.next_token()

    # --- Grammar Rules Implementation ---

    def parse(self):
        """Entry point for parsing"""
        try:
            print("TEST1")
            self.Rat25S()
            print("TEST2")
            self.semantics.print_tables()
        except SyntaxError as e:
            print(f"\nERROR: {str(e)}")
            exit(1)

    # R1. <Rat25S> ::= $$ <Opt Declaration List> $$ <Statement List> $$
    def Rat25S(self):
        self.match("Separator", "$$")
        self.match("Separator", "$$")
        print("TEST1.1")
        self.OptDeclarationList()
        print("TEST1.2")
        self.match("Separator", "$$")
        print("TEST1.3")
        self.StatementList()
        print("TEST1.4")
        self.match("Separator", "$$")

    # R12. <Opt Declaration List> ::= <Declaration List> | ε
    def OptDeclarationList(self):
        if self.current_token == "Keyword" and self.current_lexeme in ["integer", "boolean"]:
            self.DeclarationList()

    # R13. <Declaration List> ::= <Declaration> ; <Declaration List Prime>
    def DeclarationList(self):
        self.Declaration()
        self.match("Separator", ";")
        self.DeclarationListPrime()

    # R14. <Declaration List Prime> ::= <Declaration List> | ε
    def DeclarationListPrime(self):
        if self.current_token == "Keyword" and self.current_lexeme in ["integer", "boolean"]:
            self.DeclarationList()

    # R15. <Declaration> ::= <Qualifier> <IDs>
    def Declaration(self):
        self.Qualifier()
        self.IDs()

    # R10. <Qualifier> ::= integer | boolean
    def Qualifier(self):
        if self.current_lexeme not in ["integer", "boolean"]:
            raise SyntaxError("Expected 'integer' or 'boolean' qualifier")
        self.semantics.current_qualifier = self.current_lexeme
        self.next_token()

    # R16. <IDs> ::= <Identifier> <IDs Prime>
    def IDs(self):
        if self.current_token != "Identifier":
            raise SyntaxError("Expected identifier in declaration")
        
        # Semantic Action: Add to symbol table
        self.semantics.add_to_symbol_table(self.current_lexeme)
        self.next_token()
        self.IDsPrime()

    # R17. <IDs Prime> ::= , <IDs> | ε
    def IDsPrime(self):
        if self.current_lexeme == ",":
            self.next_token()
            if self.current_token != "Identifier":
                raise SyntaxError("Expected identifier after comma")
            
            # Semantic Action: Add to symbol table
            self.semantics.add_to_symbol_table(self.current_lexeme)
            self.next_token()
            self.IDsPrime()

    # R18. <Statement List> ::= <Statement> <Statement List Prime>
    def StatementList(self):
        self.Statement()
        self.StatementListPrime()

    # R19. <Statement List Prime> ::= <Statement List> | ε
    def StatementListPrime(self):
        if (self.current_lexeme in ["{", "if", "while", "return", "scan", "print"] or 
            self.current_token == "Identifier"):
            self.StatementList()

    # R20. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
    def Statement(self):
        if self.current_lexeme == "{":
            self.Compound()
        elif self.current_token == "Identifier":
            self.Assign()
        elif self.current_lexeme == "if":
            self.If()
        elif self.current_lexeme == "return":
            self.Return()
        elif self.current_lexeme == "print":
            self.Print()
        elif self.current_lexeme == "scan":
            self.Scan()
        elif self.current_lexeme == "while":
            self.While()
        else:
            raise SyntaxError("Expected statement")

    # R21. <Compound> ::= { <Statement List> }
    def Compound(self):
        self.match("Separator", "{")
        self.StatementList()
        self.match("Separator", "}")

    # R22. <Assign> ::= <Identifier> = <Expression> ;
    def Assign(self):
        identifier = self.current_lexeme
        self.match("Identifier")
        self.match("Operator", "=")
        self.Expression()
        
        # Semantic Action: Generate POPM instruction
        self.semantics.generate_instruction("POPM", self.semantics.get_address(identifier))
        self.match("Separator", ";")

    # R23. <If> ::= if ( <Condition> ) <Statement> <If Prime>
    def If(self):
        self.match("Keyword", "if")
        self.match("Separator", "(")
        self.Condition()
        self.match("Separator", ")")
        self.Statement()
        self.IfPrime()

    # R24. <If Prime> ::= else <Statement> endif | endif
    def IfPrime(self):
        if self.current_lexeme == "else":
            # Backpatch for if-then-else
            self.semantics.back_patch(self.semantics.next_instruction_address)
            self.next_token()
            self.Statement()
            self.match("Keyword", "endif")
        elif self.current_lexeme == "endif":
            # Backpatch for if-then
            self.semantics.back_patch(self.semantics.next_instruction_address)
            self.next_token()
        else:
            raise SyntaxError("Expected 'else' or 'endif'")

    # R25. <Return> ::= return <Return Prime>
    def Return(self):
        self.match("Keyword", "return")
        self.ReturnPrime()

    # R26. <Return Prime> ::= <Expression> ; | ;
    def ReturnPrime(self):
        if self.current_lexeme != ";":
            self.Expression()
        self.match("Separator", ";")

    # R27. <Print> ::= print ( <Expression> ) ;
    def Print(self):
        self.match("Keyword", "print")
        self.match("Separator", "(")
        self.Expression()
        
        # Semantic Action: Generate output instruction
        self.semantics.generate_instruction("SOUT", None)
        self.match("Separator", ")")
        self.match("Separator", ";")

    # R28. <Scan> ::= scan ( <IDs> ) ;
    def Scan(self):
        self.match("Keyword", "scan")
        self.match("Separator", "(")
        
        if self.current_token != "Identifier":
            raise SyntaxError("Expected identifier in scan statement")
        
        # Semantic Action: Generate input instructions
        identifier = self.current_lexeme
        self.semantics.generate_instruction("SIN", None)
        self.semantics.generate_instruction("POPM", self.semantics.get_address(identifier))
        
        self.match("Identifier")
        self.match("Separator", ")")
        self.match("Separator", ";")

    # R29. <While> ::= while ( <Condition> ) <Statement> endwhile
    def While(self):
        # Semantic Action: Save loop start address
        loop_start = self.semantics.generate_instruction("LABEL", None)
        
        self.match("Keyword", "while")
        self.match("Separator", "(")
        self.Condition()
        self.match("Separator", ")")
        self.Statement()
        
        # Semantic Action: Generate jump back and backpatch
        self.semantics.generate_instruction("JMP", loop_start)
        self.semantics.back_patch(self.semantics.next_instruction_address)
        
        self.match("Keyword", "endwhile")

    # R30. <Condition> ::= <Expression> <Relop> <Expression>
    def Condition(self):
        self.Expression()
        op = self.current_lexeme
        self.Relop()
        self.Expression()
        
        # Semantic Action: Generate comparison instructions
        if op == "<":
            self.semantics.generate_instruction("LES", None)
        elif op == "<=":
            self.semantics.generate_instruction("LEQ", None)
        elif op == ">":
            self.semantics.generate_instruction("GRT", None)
        elif op == ">=":
            self.semantics.generate_instruction("GEQ", None)
        elif op == "==":
            self.semantics.generate_instruction("EQU", None)
        elif op == "!=":
            self.semantics.generate_instruction("NEQ", None)
        
        # Save address for JMP0 backpatching
        self.semantics.push_jump(self.semantics.generate_instruction("JMP0", None))

    # R31. <Relop> ::= == | != | > | < | <= | >=
    def Relop(self):
        valid_ops = ["==", "!=", ">", "<", "<=", ">="]
        if (self.current_token != "Operator" or 
            self.current_lexeme not in valid_ops):
            raise SyntaxError(f"Expected relational operator {valid_ops}")
        self.next_token()

    # R32-38. Expression Handling
    def Expression(self):
        """<Expression> ::= <Term> <ExpressionPrime>"""
        self.Term()
        self.ExpressionPrime()

    def ExpressionPrime(self):
        """Handles + and - operations"""
        if self.current_token == "Operator" and self.current_lexeme in ["+", "-"]:
            op = self.current_lexeme
            self.next_token()
            self.Term()
            
            # Semantic Action
            self.semantics.generate_instruction("A" if op == "+" else "S", None)
            self.ExpressionPrime()

    def Term(self):
        """<Term> ::= <Factor> <TermPrime>"""
        self.Factor()
        self.TermPrime()

    def TermPrime(self):
        """Handles * and / operations"""
        if self.current_token == "Operator" and self.current_lexeme in ["*", "/"]:
            op = self.current_lexeme
            self.next_token()
            self.Factor()
            
            # Semantic Action
            self.semantics.generate_instruction("M" if op == "*" else "D", None)
            self.TermPrime()

    def Factor(self):
        """<Factor> ::= <FactorPrime> <Primary>"""
        self.FactorPrime()
        self.Primary()

    def FactorPrime(self):
        """Handles unary minus"""
        if self.current_lexeme == "-":
            self.next_token()

    def Primary(self):
        """Handles identifiers, numbers, and parenthesized expressions"""
        if self.current_token == "Identifier":
            # Semantic Action: Push variable value
            self.semantics.generate_instruction(
                "PUSHM", 
                self.semantics.get_address(self.current_lexeme)
            )
            self.next_token()
        elif self.current_token == "Integer":
            # Semantic Action: Push literal value
            self.semantics.generate_instruction("PUSHI", int(self.current_lexeme))
            self.next_token()
        elif self.current_lexeme == "(":
            self.next_token()
            self.Expression()
            self.match("Separator", ")")
        elif self.current_lexeme in ["true", "false"]:
            # Semantic Action: Treat boolean as 1/0
            val = 1 if self.current_lexeme == "true" else 0
            self.semantics.generate_instruction("PUSHI", val)
            self.next_token()
        else:
            raise SyntaxError("Expected primary expression")