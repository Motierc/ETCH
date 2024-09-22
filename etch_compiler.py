# ETCH (Esoteric Turing Complete HTML)

from lark import Lark, Tree, Token
import os
import pathlib

FILE_NAME = r"\numbers.etch" # Change the name for different files

ETCH_LOCATION = str(pathlib.Path(__file__).parent.resolve()) + r"\ETCH Files" + FILE_NAME
COMPILE_LOCATION = "\\".join(os.path.splitext(ETCH_LOCATION)[0].split("\\")[:-2]) + "\\Compiled Files\\" + ".".join(FILE_NAME.split(".")[:-1]) +".py"

grammar = r"""

start: doctype

doctype: "<!DOCTYPE ETCH>" head body "</ETCH>"

head: "<head>" reference* resource* "</head>"
reference: "<reference" attribute* ">"
resource: "<resource" attribute* ">" value "</resource>"


body: "<body>" statement* "</body>"
statement: indenter
        | print 
        | input
        | logic 
        | pass
        | break

indenter: while_loop 
    | for_loop
    | if_block
    | else_block

while_loop: "<while" attribute* ">" statement* "</while>"
for_loop: "<for" attribute* ">" statement* "</for>"
if_block: "<if" attribute* ">" statement* "</if>"
else_block: "<else>" statement* "</else>"
pass: "</pass>"
break: "</break>"

print: "<print" attribute* ">" (value | logic) "</print>"
logic: "<logic" attribute* ">" (TEXT) "</logic>"
input: "<input" attribute* ">" (value | logic) "</input>"

attribute: ATTRIBUTE_NAME "=" ESCAPED_STRING

value:
    | true
    | false
    | ESCAPED_STRING 
    | SIGNED_NUMBER 
    | list

true: "True"
false: "False"
list: / \[[^]]+[]]+ /   // I just kept adding stuff and this worked :)

var_name: CNAME
  // Matches text outside tags

// Terminals
ATTRIBUTE_NAME: /[a-zA-Z_][a-zA-Z0-9_-]*/
TEXT: /(?<=\>)[^<]+/
%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.CNAME
%import common.WS
%ignore WS
%ignore COMMENT
COMMENT: /<!--.*?-->/s
"""

indents = 0
last_keyword = None 

if os.path.splitext(ETCH_LOCATION)[1] != ".etch":
    raise Exception(f"Wrong File Type: Receieved file type \"{os.path.splitext(ETCH_LOCATION)[1]}\" expected \".etch\"")

with open(COMPILE_LOCATION, "w") as file:
    file.write("")

def tree_to_array(tree):
    if isinstance(tree, Tree):
        return [tree.data] + [tree_to_array(child) for child in tree.children]
    elif isinstance(tree, Token):
        return str(tree)
    else:
        return str(tree)

def parse(code: str) -> Tree:
        parser = Lark(grammar, start='start', parser="lalr")
        tree = parser.parse(code)
        return tree_to_array(tree)

def write(stuff):
    print(stuff, end = "")
    with open(COMPILE_LOCATION, "a") as file:
        file.write(f"{stuff}")

def to_python (etch, tags: str): # NOT MY FINEST WORK | FUTURE MOTIERC, PLEASE FIX THIS, MAKE IT FASTER
    global indents
    global last_keyword

    if etch == "FINISH":
        write(tags)
        return ""         
    elif etch == "statement": return tags
    elif etch == "indenter":                                    # Manage Indents
        indents += 1
        return tags
    elif etch == "end":
        indents -= 1
        return tags
    to_write = "    " * indents  
    if etch == "logic":
        if last_keyword == "print": 
            last_keyword = "p_logic"
        else: 
            last_keyword = "logic"
            write(tags)
            tags = ""
        return tags
    elif isinstance(etch, list): # Manage Non - Keywords
        to_write = ""
        if last_keyword in ["if_block", "while_loop"]:
            to_write = etch[2][1:-1]
            to_write += ":\n"
        elif last_keyword == "for_loop":
            if etch[0] == "attribute":
                if etch[1] == "increment":
                    to_write = etch[2][1:-1].split("+")[0].split("-")[0] + " in range("
                    tags = tags[:-4]
                    tags += etch[2][len(etch[2][1:-1].split("+")[0].split("-")[0])+1:-1] + "):\n"
                elif etch[1] == "start_value":
                    tags = tags[3:]
                    tags = etch[2][1:-1] + tags
                elif etch[1] == "end_value":
                    tags = tags.split(", ")
                    tags = ", ".join([tags[0], etch[2][1:-1], tags[1]])
            else: raise Exception(f"Argument Error: {etch[0]} not recognised.")
        elif last_keyword == "print":
            if etch[0] == "attribute" and etch[1] == "end": tags = f", end = {etch[2]})\n"
            elif etch[0] == "value": 
                print("", end="")
                last_keyword = None
                to_write = etch[1]
                if tags[-2:] != ")\n":
                    tags = ")\n"
            else:
                raise Exception(f"Argument Error: {etch[0]} not recognised.")       
        elif last_keyword == "input":
            if etch[1] == "set_to":
                to_write += f"{etch[2][1:-1]} = "
            elif etch[0] == "value":
                tags += f"{etch[1]})\n"
            else:
                raise Exception(f"Argument Error: {etch} not recognised.")
        elif last_keyword == "logic":
            if etch[0] == "attribute" and etch[1] == "set_to":
                to_write = "    " * indents
                to_write += f"{etch[2][1:-1]} = "
            elif etch[0] == "value":
                tags = etch[1]+"\n"   
            else: 
                raise Exception(f"Argument Error: {etch} not recognised.")
        elif last_keyword == "resource":
            if etch[1] == "name":
                to_write = etch[2][1:-1] + " = "
            elif etch[0] == "value":
                tags = etch[1]
                if isinstance(tags, list):
                    tags = tags[1]
                tags += "\n"
        else:
            print(f"{etch}",end="")         
            to_write = etch
    else:        
        if last_keyword != "p_logic":
            write(tags)
            tags = ""

        if etch == "FINISH":
            return tags
        elif etch == "while_loop":                                # Manage Indenters
            to_write = "    " * (indents-1) + "while "
            last_keyword = "while_loop"
        elif etch == "for_loop":
            to_write = "    " * (indents-1) + "for "
            tags = "0, , 1):\n"
            last_keyword = "for_loop"
        elif etch == "if_block":
            to_write = "    " * (indents-1) + "if "
            last_keyword = "if_block"
        elif etch == "else_block":
            to_write = "    " * (indents-1) + "else:\n"
            last_keyword = "else_block"
        elif etch == "print":
            to_write += "print("
            last_keyword = "print"
            tags = ")\n"
        elif etch == "input":
            tags = "input("
            last_keyword = "input"
        elif etch == "resource":
            last_keyword = "resource"
        elif etch == "pass":
            to_write += "pass\n"
            last_keyword = "pass"
        elif etch == "break":
            to_write += "break\n"
            last_keyword = "break"
        else:                                                     # Manage Uknowns
            if last_keyword == "p_logic":
                to_write = f"{etch}"
                if tags[-2:] != ")\n" and etch != "" and to_write != "":
                    to_write += ")\n"  
                else:
                    to_write+=tags
                tags = ""  
            else:
                to_write = "    " * indents
                to_write += f"{etch}\n"      
    write(to_write)
    return tags

def compile(file_location: str) -> None: # TODO: Tell when a loop/if ends
        with open(file_location) as code_read_file:
            start_code = code_read_file.read()
        tree_array = parse(start_code)
        global last_keyword
        p_arr = tree_array[1][1][1:] + tree_array[1][2][1:]
        p_arr: list
        nested_array = p_arr
        #input(nested_array)
        p_arr = []
        stack = [(nested_array, 0)]
        tags = ""
        while stack:
            #input(f"\n{stack}")
            current_array, index = stack.pop()
            #print(f"\n--> {current_array}")
            try: 
                if current_array[0] in ["indenter"] and index == len(current_array):
                    to_python("end", tags)
            except Exception: pass

            while index < len(current_array):
                element = current_array[index]
                if isinstance(element, list):  # If the element is a list, push it onto the stack
                    if element[0] in ["attribute", "var_name", "value", "text"]: 
                        tags = to_python(element, tags)
                        index+=1
                        continue
                    stack.append((current_array, index + 1))  # Push the rest of the current list
                    stack.append((element, 0))  # Push the new list
                    break
                tags = to_python(element, tags)

                index += 1
        to_python("FINISH", tags)

        #return tree_array


compile(ETCH_LOCATION)