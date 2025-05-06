from lexer import lexer

# control whether to print the parsing rules
print_rules = True

# global variables for tracking current token and file pointers
current_token = None
current_lexeme = None
output_file = None
fp = None  # file pointer for lexer

# ************ Symbol table for identifiers ************
symbol_table = {}

symbol_table_memory_address = 10000

def add_to_symbol_table(token : str):
    """Add identifier to symbol table"""
    if token not in symbol_table:
        
        global symbol_table_memory_address
        symbol_table[token] = symbol_table_memory_address
        symbol_table_memory_address += 1
    else:
        print(f"Error: Identifier '{token}' already declared")
        exit(1)

def is_token_in_symbol_table(token : str):
    """Check if token is in symbol table"""
    if token in symbol_table:
        return True
    else:
        return False

def get_Address(token : str):
    """Get address of token in symbol table"""
    if token in symbol_table:
        return symbol_table[token]
    else:
        print(f"Error: Identifier '{token}' not found in symbol table")
        exit(1)

# ************ Instruction table for code generation ************
# global variable for instruction operand
inst_Operand = 10000

instructionDict = {}

# global variable for instruction address
inst_Address = 1

# Each entry in the instruction array has an instruction object that contains:
# 1. address
# 2. opcode
# 3. operand
class InstructionTable:
    def __init__(self, address, op, operand):
        self.address = address
        self.op = op
        self.operand = operand
        # global inst_Operand
        # self.operand = inst_Operand
        # inst_Operand += 1

def generate_instruction(op, operand):
    """Generate instruction and add to instruction array"""
    global inst_Address
    instruction = InstructionTable(inst_Address, op, operand)
    instructionDict[inst_Address] = instruction
    inst_Address += 1

stack = []

def back_patch(JMP_address):
    addr = stack.pop()
    instructionDict[addr].operand = JMP_address
    
# ************ Parsing functions ************
def next_token():
    """Get next token from lexer and write to output file"""
    global current_token, current_lexeme
    current_token, current_lexeme = lexer(fp)
    
    # write token info to output file
    if output_file:
        output_file.write(f"Token: {current_token:14} Lexeme: {current_lexeme}\n")
    if print_rules:
        print(f"Token: {current_token:14} Lexeme: {current_lexeme}")

def syntax_error(expected):
    """Handle syntax errors with meaningful messages"""
    err_msg = f"[Syntax Error] Expected {expected}, but got '{current_lexeme}' ({current_token})"
    if output_file:
        output_file.write(err_msg + "\n")
    print(err_msg)
    exit(1)

# R1. <Rat25S> ::= $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$
def Rat25S():
    if print_rules: 
        if output_file: output_file.write("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$\n")
        print("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$")
    
    if current_token != "Separator" or current_lexeme != "$$":
        syntax_error("$$")
    next_token()
    
    # OptFunctionDefinitions()

    if current_token != "Separator" or current_lexeme != "$$":
        syntax_error("$$")
    next_token()
    
    OptDeclarationList()
    
    if current_token != "Separator" or current_lexeme != "$$":
        syntax_error("$$")
    next_token()
    
    StatementList()
    
    if current_token != "Separator" or current_lexeme != "$$":
        syntax_error("$$")
    next_token()

    

# R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
# def OptFunctionDefinitions():
#     if print_rules: 
#         if output_file: output_file.write("<Opt Function Definitions> -> <Function Definitions> | <Empty>\n")
#         print("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
    
#     if current_token == "Keyword" and current_lexeme == "function":
#         FunctionDefinitions()
#     else:
#         if print_rules: 
#             if output_file: output_file.write("<Empty>\n")
#             print("<Empty>")

# # R3. <Function Definitions> ::= <Function> <Function Definitions>
# def FunctionDefinitions():
#     if print_rules: 
#         if output_file: output_file.write("<Function Definitions> -> <Function> <Function Definitions Prime>\n")
#         print("<Function Definitions> -> <Function> <Function Definitions Prime>")
#     Function()

#     FunctionDefintionsPrime()

# # R4. <Function Definitions Prime> ::= <Function Definitions> | ε
# def FunctionDefintionsPrime():
#     if print_rules:
#         if output_file: output_file.write("<Function Definitions Prime> -> <Function> | ε\n")
#         print("<Function Definitions Prime> -> <Function> | ε ")
#     if current_token == "Keyword" and current_lexeme == "function":
#         Function()
#     else:
#         if print_rules: 
#             if output_file: output_file.write("<Empty>\n")
#             print("<Empty>")
            

# # R5. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
# def Function():
#     if print_rules: 
#         if output_file: output_file.write("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>\n")
#         print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    
#     if current_lexeme != "function":
#         syntax_error("function")
#     next_token()
    
#     if current_token != "Identifier":
#         syntax_error("Identifier")
#     next_token()
    
#     if current_lexeme != "(":
#         syntax_error("(")
#     next_token()
    
#     OptParameterList()
    
#     if current_lexeme != ")":
#         syntax_error(")")
#     next_token()
    
#     OptDeclarationList()
#     Body()

# # R6. <Opt Parameter List> ::= <Parameter List> | <Empty>
# def OptParameterList():
#     if print_rules: 
#         if output_file: output_file.write("<Opt Parameter List> -> <Parameter List> | <Empty>\n")
#         print("<Opt Parameter List> -> <Parameter List> | <Empty>")
    
#     if current_token == "Identifier":
#         ParameterList()
#     else:
#         if print_rules: 
#             if output_file: output_file.write("<Empty>\n")
#             print("<Empty>")

# # R7. <Parameter List> ::= <Parameter> <Parameter List Prime>
# def ParameterList():
#     if print_rules: 
#         if output_file: output_file.write("<Parameter List> -> <Parameter> <Parameter List Prime\n")
#         print("<Parameter List> -> <Parameter> <Parameter List Prime>")
    
#     Parameter()

#     ParameterListPrime()

# # R8. <Parameter List Prime> ::= , <Parameter List> | ε
# def ParameterListPrime():
#     if print_rules: 
#         if output_file: output_file.write("<Parameter List Prime> -> , <Parameter List> | ε\n")
#         print("<Parameter List Prime> -> , <Parameter List> | ε")
    
#     if current_lexeme == ",":
#         next_token()
#         ParameterList()
#     else:
#         if print_rules: 
#             if output_file: output_file.write("<Empty>\n")
#             print("<Empty>")

# # R9. <Parameter> ::= <IDs> <Qualifier>
# def Parameter():
#     if print_rules: 
#         if output_file: output_file.write("<Parameter> -> <IDs> <Qualifier>\n")
#         print("<Parameter> -> <IDs> <Qualifier>")
    
#     IDs()

#     Qualifier()

# R10. <Qualifier> ::= integer | boolean | real
def Qualifier():
    if print_rules: 
        if output_file: output_file.write("<Qualifier> -> integer | boolean\n") # ("<Qualifier> -> integer | boolean | real\n")
        print("<Qualifier> -> integer | boolean") # ("<Qualifier> -> integer | boolean | real")
    
    if current_token == "Keyword" and current_lexeme in {"integer", "boolean"}: # {"integer", "boolean", "real"}
        next_token()
    else:
        syntax_error("Qualifier (integer|boolean)") # (integer|boolean|real)

# R11. <Body> ::= { <Statement List> }
def Body():
    if print_rules: 
        if output_file: output_file.write("<Body> -> { <Statement List> }\n")
        print("<Body> -> { <Statement List> }")
    
    if current_lexeme != "{":
        syntax_error("{")
    next_token()
    
    StatementList()
    
    if current_lexeme != "}":
        syntax_error("}")
    next_token()

# R12. <Opt Declaration List> ::= <Declaration List> | <Empty>
def OptDeclarationList():
    if print_rules: 
        if output_file: output_file.write("<Opt Declaration List> -> <Declaration List> | <Empty>\n")
        print("<Opt Declaration List> -> <Declaration List> | <Empty>")
    
    if current_token == "Keyword" and current_lexeme in {"integer", "boolean"}: # {"integer", "boolean", "real"}
        DeclarationList()
    else:
        if print_rules: 
            if output_file: output_file.write("<Empty>\n")
            print("<Empty>")

# R13. <Declaration List> ::= <Declaration> ; <Declaration List Prime>
def DeclarationList():
    if print_rules: 
        if output_file: output_file.write("<Declaration List> -> <Declaration> ; <Declaration List Prime>\n")
        print("<Declaration List> -> <Declaration> ; <Declaration List Prime>")
    
    Declaration()
    if current_lexeme != ";":
        syntax_error(";")
    next_token()
    
    DeclarationListPrime()

# R14. <Declaration List Prime> ::= <Declaration List> | ε
def DeclarationListPrime():
    if print_rules: 
        if output_file: output_file.write("<Declaration List Prime> -> <Declaration List> | ε\n")
        print("<Declaration List Prime> -> <Declaration List> | ε")
    
    if current_token == "Keyword" and current_lexeme in {"integer", "boolean"}: # {"integer", "boolean", "real"}
        DeclarationList()
    else:
        if print_rules: 
            if output_file: output_file.write("<Empty>\n")
            print("<Empty>")

# global variable to track if we are in a declaration
# (used to check if an identifier is already declared)
# and to prevent re-declaration of the same identifier
# in the same scope
is_declaration = False
# R15. <Declaration> ::= <Qualifier> <IDs>
def Declaration():
    if print_rules: 
        if output_file: output_file.write("<Declaration> -> <Qualifier> <IDs>\n")
        print("<Declaration> -> <Qualifier> <IDs>")
    
    Qualifier()

    # if the current token was already declared, then we need to raise an error
    if is_token_in_symbol_table(current_lexeme):
        print(f"Error: Identifier '{current_lexeme}' already declared")
        exit(1)
    else:
        # add identifier to symbol table
        add_to_symbol_table(current_lexeme)
        global is_declaration
        is_declaration = True
        IDs()
        is_declaration = False

# R16. <IDs> ::= <Identifier> <IDs Prime>
def IDs():
    if print_rules: 
        if output_file: output_file.write("<IDs> -> <Identifier> <IDs Prime>\n")
        print("<IDs> -> <Identifier> <IDs Prime>")
    
    if current_token != "Identifier":
        syntax_error("Identifier")
    next_token()
    
    IDsPrime()

# R17. <IDs Prime> ::= , <IDs> | ε
def IDsPrime():
    if print_rules: 
        if output_file: output_file.write("<IDs Prime> -> , <IDs> | ε\n")
        print("<IDs Prime> -> , <IDs> | ε")
    
    if current_lexeme == ",":
        next_token()
        global is_declaration
        if is_declaration and is_token_in_symbol_table(current_lexeme):
            print(f"Error: Identifier '{current_lexeme}' already declared")
            exit(1)
        else:
            global is_scan

            if is_declaration:
                add_to_symbol_table(current_lexeme)

            if is_scan:
                # generate the instruction for the scan
                generate_instruction("SIN", None)
                # generate the instruction for the assignment
                generate_instruction("POPM", get_Address(current_lexeme))
            IDs()
    else:
        if print_rules: 
            if output_file: output_file.write("<Empty>\n")
            print("<Empty>")

# R18. <Statement List> ::= <Statement> <Statement List Prime>
def StatementList():
    if print_rules: 
        if output_file: output_file.write("<Statement List> -> <Statement> <Statement List Prime>\n")
        print("<Statement List> -> <Statement> <Statement List Prime>")
    
    Statement()

    StatementListPrime()

# R19. <Statement List Prime> ::= <Statement List> | ε
def StatementListPrime():
    if print_rules: 
        if output_file: output_file.write("<Statement List Prime> -> <Statement List> | ε\n")
        print("<Statement List Prime> -> <Statement List> | ε")
    
    if current_lexeme in {"{", "if", "while", "return", "scan", "print"} or current_token == "Identifier":
        StatementList()
    else:
        if print_rules: 
            if output_file: output_file.write("<Empty>\n")
            print("<Empty>")

# R20. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
def Statement():
    if print_rules: 
        if output_file: output_file.write("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>\n")
        print("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
    
    if current_lexeme == "{":
        Compound()
    elif current_token == "Identifier":
        Assign()
    elif current_lexeme == "if":
        If()
    elif current_lexeme == "return":
        Return()
    elif current_lexeme == "print":
        Print()
    elif current_lexeme == "scan":
        Scan()
    elif current_lexeme == "while":
        While()
    else:
        syntax_error("Statement start")

# R21. <Compound> ::= { <Statement List> }
def Compound():
    if print_rules: 
        if output_file: output_file.write("<Compound> -> { <Statement List> }\n")
        print("<Compound> -> { <Statement List> }")
    
    if current_lexeme != "{":
        syntax_error("{")
    next_token()
    
    StatementList()
    
    if current_lexeme != "}":
        syntax_error("}")
    next_token()

# R22. <Assign> ::= <Identifier> = <Expression> ;
def Assign():
    if print_rules: 
        if output_file: output_file.write("<Assign> -> <Identifier> = <Expression> ;\n")
        print("<Assign> -> <Identifier> = <Expression> ;")
    
    if current_token != "Identifier":
        syntax_error("Identifier")

    # save the token of the identifier
    save = current_lexeme
    
    # if the current identifier was not declared, then we need to raise an error
    if not is_token_in_symbol_table(current_lexeme):
        print(f"Error: Identifier '{current_lexeme}' was not declared")
        exit(1)
    else:
        next_token()
    
    if current_lexeme != "=":
        syntax_error("=")
    next_token()
    
    Expression()

    # generate the instruction for the assignment
    generate_instruction("POPM", get_Address(save))
    
    if current_lexeme != ";":
        syntax_error(";")
    next_token()

# R23. <If> ::= if ( <Condition> ) <Statement> <If Prime>
def If():
    if print_rules: 
        if output_file: output_file.write("<If> -> if ( <Condition> ) <Statement> <If Prime>\n")
        print("<If> -> if ( <Condition> ) <Statement> <If Prime>")
    
    if current_lexeme != "if":
        syntax_error("if")
    next_token()
    
    if current_lexeme != "(":
        syntax_error("(")
    next_token()
    
    Condition()
    
    if current_lexeme != ")":
        syntax_error(")")
    next_token()
    
    Statement()
    
    IfPrime()

# R24. <If Prime> ::= else <Statement> endif | endif
def IfPrime():
    global inst_Address
    
    if print_rules: 
        if output_file: output_file.write("<If Prime> -> else <Statement> endif | endif\n")
        print("<If Prime> -> else <Statement> endif | endif")
    
    if current_lexeme == "else":
        back_patch(inst_Address)
        # generate the instruction for the else
        generate_instruction("LABEL", None)
        next_token()
        Statement()
        if current_lexeme != "endif":
            syntax_error("endif")
        next_token()
    
    elif current_lexeme == "endif":
        back_patch(inst_Address)
        # generate the instruction for the endif
        generate_instruction("LABEL", None)
        next_token()
    else:
        syntax_error("else or endif")

# R25. <Return> ::= return <Return Prime>
def Return():
    if print_rules: 
        if output_file: output_file.write("<Return> -> return <Return Prime>\n")
        print("<Return> -> return <Return Prime>")
    
    if current_lexeme != "return":
        syntax_error("return")
    next_token()
    
    ReturnPrime()

# R26. <Return Prime> ::= <Expression> ; | ;
def ReturnPrime():
    if print_rules: 
        if output_file: output_file.write("<Return Prime> -> <Expression> ; | ;\n")
        print("<Return Prime> -> <Expression> ; | ;")
    
    if current_lexeme == ";":
        next_token()
    elif current_token in {"Identifier", "Integer"} or current_lexeme in {"true", "false", "-"}: # {"Identifier", "Integer", "Real"}
        Expression()
        
        if current_lexeme != ";":
            syntax_error(";")
        next_token()
    else:
        syntax_error("Expression or ;")

# R27. <Print> ::= print ( <Expression> );
def Print():
    if print_rules: 
        if output_file: output_file.write("<Print> -> print ( <Expression> );\n")
        print("<Print> -> print ( <Expression> );")
    
    if current_lexeme != "print":
        syntax_error("print")
    next_token()
    
    if current_lexeme != "(":
        syntax_error("(")
    next_token()
    
    Expression()
    
    if current_lexeme != ")":
        syntax_error(")")

    generate_instruction("SOUT", None)
    next_token()
    
    if current_lexeme != ";":
        syntax_error(";")
    next_token()

# global variable to track if we are in a scan statement
# (used to check if an identifier is already declared)
# and to prevent re-declaration of the same identifier
# in the same scope
is_scan = False
# R28. <Scan> ::= scan ( <IDs> );
def Scan():
    if print_rules: 
        if output_file: output_file.write("<Scan> -> scan ( <IDs> );\n")
        print("<Scan> -> scan ( <IDs> );")
    
    if current_lexeme != "scan":
        syntax_error("scan")
    next_token()
    
    if current_lexeme != "(":
        syntax_error("(")
    next_token()

    # if the current token was not declared, then we need to raise an error
    if not is_token_in_symbol_table(current_lexeme):
        print(f"Error: Identifier '{current_lexeme}' was not declared")
        exit(1)
    global is_scan
    is_scan = True

    generate_instruction("SIN", None)
    # generate the instruction for the scan
    generate_instruction("POPM", get_Address(current_lexeme))
    IDs()
    is_scan = False
    if current_lexeme != ")":
        syntax_error(")")
    next_token()
    
    if current_lexeme != ";":
        syntax_error(";")
    next_token()

# R29. <While> ::= while ( <Condition> ) <Statement> endwhile
def While():
    if print_rules: 
        if output_file: output_file.write("<While> -> while ( <Condition> ) <Statement> endwhile\n")
        print("<While> -> while ( <Condition> ) <Statement> endwhile")
    
    if current_lexeme != "while":
        syntax_error("while")
    global inst_Address
    Ar = inst_Address
    generate_instruction("LABEL", None)
    next_token()
    
    if current_lexeme != "(":
        syntax_error("(")
    next_token()
    
    Condition()
    
    if current_lexeme != ")":
        syntax_error(")")
    next_token()
    
    Statement()

    # generate the instruction for the while loop
    generate_instruction("JMP", Ar)

    back_patch(inst_Address)

    if current_lexeme != "endwhile":
        syntax_error("endwhile")
    next_token()

# R30. <Condition> ::= <Expression> <Relop> <Expression>
def Condition():
    if print_rules: 
        if output_file: output_file.write("<Condition> -> <Expression> <Relop> <Expression>\n")
        print("<Condition> -> <Expression> <Relop> <Expression>")
    
    Expression()
    op = current_lexeme
    Relop()
    Expression()
    # generate the instruction for the condition
    global stack
    match op:
        case "<":
            generate_instruction("LES", None)
            stack.append(inst_Address)
            generate_instruction("JMP0", None)
        case "<=":
            generate_instruction("LEQ", None)
            stack.append(inst_Address)
            generate_instruction("JMP0", None)
        case ">":
            generate_instruction("GRT", None)
            stack.append(inst_Address)
            generate_instruction("JMP0", None)
        case ">=":  
            generate_instruction("GEQ", None)
            stack.append(inst_Address)
            generate_instruction("JMP0", None)
        case "==":
            generate_instruction("EQU", None)
            stack.append(inst_Address)
            generate_instruction("JMP0", None)
        case "!=":
            generate_instruction("NEQ", None)
            stack.append(inst_Address)
            generate_instruction("JMP0", None)

# R31. <Relop> ::= == | != | > | < | <= | >=
def Relop():
    if print_rules: 
        if output_file: output_file.write("<Relop> -> == | != | > | < | <= | >=\n")
        print("<Relop> -> == | != | > | < | <= | >=")
    
    if current_token == "Operator" and current_lexeme in {"==", "!=", ">", "<", "<=", ">="}:
        next_token()
    else:
        syntax_error("relational operator (==|!=|>|<|<=|>=)")

# R32. <Expression> ::= <Term> <ExpressionPrime>
def Expression():
    if print_rules: 
        if output_file: output_file.write("<Expression> -> <Term> <ExpressionPrime>\n")
        print("<Expression> -> <Term> <ExpressionPrime>")
    Term()
    ExpressionPrime()

# R33. <ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | ε
def ExpressionPrime():
    if current_token == "Operator" and current_lexeme in {"+", "-"}:
        # save the token of the operator
        save = current_lexeme
        if print_rules: 
            if output_file: output_file.write(f"<ExpressionPrime> -> {current_lexeme} <Term> <ExpressionPrime>\n")
            print(f"<ExpressionPrime> -> {current_lexeme} <Term> <ExpressionPrime>")
        next_token()
        Term()
        if save == "+":
            generate_instruction("A", None)
        elif save == "-":
            generate_instruction("S", None)
        ExpressionPrime()
    else:
        if print_rules: 
            if output_file: output_file.write("<ExpressionPrime> -> ε\n")
            print("<ExpressionPrime> -> ε")

# R34. <Term> ::= <Factor> <TermPrime>
def Term():
    if print_rules: 
        if output_file: output_file.write("<Term> -> <Factor> <TermPrime>\n")
        print("<Term> -> <Factor> <TermPrime>")
    Factor()
    TermPrime()

# R35. <TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | ε
def TermPrime():
    if current_token == "Operator" and current_lexeme in {"*", "/"}:
        # save the token of the operator
        save = current_lexeme
        if print_rules: 
            if output_file: output_file.write(f"<TermPrime> -> {current_lexeme} <Factor> <TermPrime>\n")
            print(f"<TermPrime> -> {current_lexeme} <Factor> <TermPrime>")
        next_token()
        Factor()
        if save == "*":
            generate_instruction("M", None)
        elif save == "/":
            generate_instruction("D", None)
        TermPrime()
    else:
        if print_rules: 
            if output_file: output_file.write("<TermPrime> -> ε\n")
            print("<TermPrime> -> ε")

# R36. <Factor> ::= <Factor Prime> <Primary>
def Factor():
    if print_rules: 
        if output_file: output_file.write("<Factor> -> <Factor Prime> <Primary>\n")
        print("<Factor> -> <Factor Prime> <Primary>")
    
    FactorPrime()
    Primary()

# R37. <Factor Prime> ::= - | ε
def FactorPrime():
    if current_lexeme == "-":
        if print_rules: 
            if output_file: output_file.write("<Factor Prime> -> -\n")
            print("<Factor Prime> -> -")
        next_token()
    else:
        if print_rules: 
            if output_file: output_file.write("<Factor Prime> -> ε\n")
            print("<Factor Prime> -> ε")

# R38. <Primary> ::= Identifier | Integer | Identifier ( <IDs> ) | Real | ( <Expression> ) | true | false
def Primary():
    if print_rules: 
        if output_file: output_file.write("<Primary> -> Identifier | Integer | Identifier ( <IDs> ) | ( <Expression> ) | true | false\n")
        print("<Primary> -> Identifier | Integer | Identifier ( <IDs> ) | ( <Expression> ) | true | false")

        # ("<Primary> -> Identifier | Integer | Identifier ( <IDs> ) | Real | ( <Expression> ) | true | false\n")
        # print("<Primary> -> Identifier | Integer | Identifier ( <IDs> ) | Real | ( <Expression> ) | true | false")
    
    if current_token == "Identifier":
        # if the current token was already declared, then we need to raise an error
        if not is_token_in_symbol_table(current_lexeme):
            print(f"Error: Identifier '{current_lexeme}' was not declared")
            exit(1)
        # generate the instruction for the identifier
        generate_instruction("PUSHM", get_Address(current_lexeme))
        next_token()
        if current_lexeme == "(":
            next_token()
            IDs()
            if current_lexeme != ")":
                syntax_error(")")
            next_token()
    elif current_token in {"Integer"}: # {"Integer", "Real"}
        # generate the instruction for the integer
        generate_instruction("PUSHI", current_lexeme)
        next_token()
    elif current_lexeme == "(":
        next_token()
        Expression()
        if current_lexeme != ")":
            syntax_error(")")
        next_token()
    elif current_lexeme in {"true", "false"}:
        next_token()
    else:
        syntax_error("Identifier | Integer | Identifier ( <IDs> ) | ( <Expression> ) | true | false")
        # ("Identifier | Integer | Identifier ( <IDs> ) | Real | ( <Expression> ) | true | false")

def syntax_analyzer(input_filename, output_filename):
    """Main analyzer function that processes input file"""
    global output_file, fp
    
    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            output_file = outfile
            fp = infile  # make file pointer available globally
            
            # initialize first token
            next_token()
            
            # begin parsing
            Rat25S()
            
            # verify we reached EOF
            if current_token != "EOF":
                syntax_error("EOF")
                
            if output_file:
                output_file.write("Parsing completed successfully!\n")
            print("Parsing completed successfully!")
            print("\n\nSymbol Table:")
            for identifier, address in symbol_table.items():
                print(f"{identifier}: {address}")
                if output_file:
                    output_file.write(f"{identifier}: {address}\n")

            print("\n\nInstruction Table:")
            for address, instruction in instructionDict.items():
                print(f"Address: {address}, Opcode: {instruction.op}, Operand: {instruction.operand}")
                if output_file:
                    output_file.write(f"Address: {address}, Opcode: {instruction.op}, Operand: {instruction.operand}\n")
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found")
    except Exception as e:
        print(f"Error during parsing: {str(e)}")

if __name__ == "__main__":
    input_file = input("Enter input file name: ")
    output_file_name = input("Enter output file name: ")
    syntax_analyzer(input_file, output_file_name)