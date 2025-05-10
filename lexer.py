def lexer(fp):
    # Token construction
    curr_tok = ""
    curr_tok_type = ""
    curr_char = ""
    
    # Comment handling states
    in_comment = False
    comment_start_line = 0
    line_num = 1

    # Token definitions
    SEPARATORS = {'{', '}', ';', '(', ')', '$$', ',', ':'}
    OPERATORS = {'==', '=', '!=', '>', '<', '<=', '>=', '+', '-', '*', '/'}
    KEYWORDS = {
        'function', 'integer', 'boolean', 'if', 'else', 'endif',
        'while', 'return', 'scan', 'print', 'endwhile', 'true', 'false'
    }

    while True:
        curr_char = fp.read(1)
        
        # Track line numbers
        if curr_char == '\n':
            line_num += 1
            
        # --- Handle EOF ---
        if curr_char == "":
            if in_comment:
                raise SyntaxError(f"Unterminated comment starting at line {comment_start_line}")
            return ("EOF", "EOF")
        
        # --- Comment Processing ---
        if in_comment:
            if curr_char == '*':
                next_char = fp.read(1)
                if next_char == ']':
                    in_comment = False
                else:
                    fp.seek(fp.tell() - 1)
            continue
        
        # Detect comment start
        if not curr_tok and curr_char == '[':
            next_char = fp.read(1)
            if next_char == '*':
                in_comment = True
                comment_start_line = line_num
                continue
            fp.seek(fp.tell() - 1)  # Put back if not a comment
        
        # --- Skip Whitespace ---
        if curr_char in {' ', '\t', '\n'}:
            if curr_tok:  # Return accumulated token
                break
            continue
        
        # --- Start New Token ---
        if not curr_tok:
            curr_tok = curr_char
            # Determine token type
            if curr_char in {'$', '{', '}', ';', '(', ')', ',', ':'}:
                curr_tok_type = "Separator"
            elif curr_char in {'=', '!', '>', '<', '+', '-', '*', '/'}:
                curr_tok_type = "Operator"
            elif curr_char.isalpha():
                curr_tok_type = "Identifier"
            elif curr_char.isdigit():
                curr_tok_type = "Integer"
            else:
                curr_tok_type = "Unknown"
            continue
        
        # Handle $$ separator
        if curr_tok == '$' and curr_char == '$':
            return ("Separator", "$$")
        
        # Handle multi-character operators (==, !=, etc)
        if curr_tok_type == "Operator":
            potential_op = curr_tok + curr_char
            if potential_op in OPERATORS:
                return ("Operator", potential_op)
            fp.seek(fp.tell() - 1)
            return ("Operator", curr_tok)
        
        # Handle identifiers/keywords
        if curr_tok_type == "Identifier":
            if curr_char.isalnum():
                curr_tok += curr_char
                continue
            fp.seek(fp.tell() - 1)
            return ("Keyword", curr_tok) if curr_tok in KEYWORDS else ("Identifier", curr_tok)
        
        # Handle integers
        if curr_tok_type == "Integer":
            if curr_char.isdigit():
                curr_tok += curr_char
                continue
            fp.seek(fp.tell() - 1)
            return ("Integer", curr_tok)
        
        # Handle other separators
        if curr_tok_type == "Separator":
            fp.seek(fp.tell() - 1)
            return ("Separator", curr_tok)
    
    # --- Return Completed Token ---
    if curr_tok_type == "Identifier" and curr_tok in KEYWORDS:
        return ("Keyword", curr_tok)
    
    return (curr_tok_type, curr_tok)