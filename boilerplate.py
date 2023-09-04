##################### BOILERPLATE BEGINS ############################

import re
# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################

global err
err=0

class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"


# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    global err
    err=0
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char == '_')

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    print(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position+1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if lexeme[0].isdigit() and not is_valid_identifier(lexeme):
                        print(
                            f"Lexical Error: Invalid identifier: {lexeme}\nIdentifier can't start with digits") 
                        return None
                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme)) 
    return tokens

########################## BOILERPLATE ENDS ###########################



def checkGrammar(tokens):
    
    #global i
    i=0
    avail=0
    def is_terminal(token):
        nonlocal i
        nonlocal avail
        print(".....",token[1],".....")
        #print("hiii")
        #print(token in {'Identifier', 'Keyword', 'Integer', 'Float', 'Symbol'})
        if avail==1 and token[1]=='else':
            print(avail+"....")
            avail=0
            return token[0] in {'IDENTIFIER', 'KEYWORD', 'INTEGER', 'FLOAT', 'SYMBOL'}
        elif avail==0 and token[1]=='else':
            print("Syntactic error: 'else' comes before 'if'")
            return False
        else:
            return token[0] in {'IDENTIFIER', 'KEYWORD', 'INTEGER', 'FLOAT', 'SYMBOL'}
                

    def S(tokens):
        nonlocal i
        nonlocal avail
        # print(tokens[0][1])
        if tokens[i][1] == "else":
                print("Syntactic Error: 'else' comes before 'if'")
                #print("130")
                return False
        elif tokens[i][1] == "if":
                #tokens.pop(0)  # Consume 'Keyword'
                  # Consume '('
                i+=1
                avail=1  
                #print(tokens[i][1])
                print("....",avail)
                 
                if tokens and tokens[i][0] == TokenType.SYMBOL and tokens[i][1] == '(':
                     
                 i+=1   
                      
                 if A(tokens):
                    if tokens and tokens[i][0] == TokenType.SYMBOL and tokens[i][1] == ')':
                        #tokens.pop(0)  # Consume ')'
                        i+=1
                        return True
                    else:
                        print("Bracket present does not have matching bracket")
                        return False    
                    
                elif tokens and tokens[i][0] == TokenType.SYMBOL and tokens[i][1] == ')':
                     
                    print("Brackets not balanced")
                    return False
                
                elif tokens and tokens[i][0] == TokenType.KEYWORD and tokens[i][1] == 'else':
                    print("missed the condition for if statement")
                    return False
                else:
                    if A(tokens):
                        return True
                    else:
                        return False    
        if y(tokens):
            return True
        #print("141")
        return False

    def y(tokens):
        nonlocal i
        if tokens and is_terminal(tokens[i]):
            #tokens.pop(0)  # Consume a terminal token
            i+=1
            return True
        #print("148")
        return False

    def A(tokens):
        nonlocal i
        if tokens and tokens[i][0] == 'Symbol' and tokens[i][1] == '(':
            #tokens.pop(0)  # Consume 'Symbol'
            tokens.pop(0)  # Consume '('
            i+=1
            if cond(tokens):
                if tokens and tokens[0] == 'Symbol' and tokens[1] == ')':
                    tokens.pop(0)  # Consume ')'
                    i+=1
                    return True
                else:
                    print("brackets not balanced")
                    return False
            #print("159")    
            return False
        elif tokens and tokens[i][0] == 'Symbol' and tokens[i][1] == '(':
            print("Bracket present does not have matching bracket")
            return False
        else:
            if cond(tokens):
                return True
            else:
                return False
        #print("161")
        return False

    def cond(tokens):
        nonlocal i
        if tokens and tokens[i][0] == 'Symbol' and tokens[i][1] == '(':
            #tokens.pop(0)  # Consume 'Symbol'
            tokens.pop(0)  # Consume '('
            i+=1
            if x(tokens):
                if tokens and tokens[0] == 'Symbol' and tokens[1] in {'+', '-', '*', '/', '^', '<', '>', '='}:
                    #tokens.pop(0)  # Consume 'op1'
                    i+=1
                    if x(tokens):
                        if tokens and tokens[0] == 'Symbol' and tokens[1] == ')':
                            tokens.pop(0)  # Consume ')'
                            i+=1
                            return True
                        else:
                            print("brackets not balanced")
                            return False
                #print("175")        
                return False
        elif tokens and tokens[i][0] == 'Symbol' and tokens[i][1] == ')':
            print("Wrong usage of brackets")
            return False    
        else:
            if x(tokens):
                return True
            else:
                return False
        #print("179")
        return False

    def x(tokens):
        nonlocal i
        # print(tokens[i][0])
        # print(is_terminal(tokens[i][0]))
        if tokens and is_terminal(tokens[i][0]):
            #tokens.pop(0)  # Consume a terminal token
            # i+=1
            return True
        # elif cond(tokens):
        #         i+=1
        #         return True
        elif y(tokens):
                #i+=1
                return True
        else:
            print("Syntactic error")
            return False    
        #print("190")
        return False

    #Handle printing of token types and values
    if S(tokens):
        return True
    else:
        #print("197")
        return False
     

# Example usage:

# Test the tokenizer
if __name__ == "__main__":
    #source_code = "if 2 + xi >> 0 print 2.0 else print -1;"
    source_code = "if x>0 else else print 5;"
     
    tokens = tokenize(source_code)
     
    if err == 0:
        logs = checkGrammar(tokens)
    else:
        logs = None

    #print(tokens)
    #print(logs)
    if logs != 0:
        if tokens: 
            for token in tokens:
                print(f"Token Type: {token[0]}, Token Value: {token[1]}")