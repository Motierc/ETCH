from lark import Lark, Tree, Token

CODE_LOCATION = r"excample.etch"

grammar = """

start: doctype

doctype: "<!DOCTYPE ETCH>" head body "</ETCH>"

head: "<head>" reference* resource* "</head>"
reference: "<reference" attribute* ">"
resource: "<resource" attribute* ">" value "</resource>"

body: "<body>" statement* "</body>"
statement: while_loop 
        | for_loop 
        | if_else 
        | print 
        | logic 
        | text

while_loop: "<while" attribute* ">" statement* "</while>"
for_loop: "<for" attribute* ">" statement* "</for>"
if_else: if_block else_block
if_block: "<if" attribute* ">" statement* "</if>"
else_block: "<else>" statement* "</else>"

print: "<print" attribute* ">" (value | logic | var_name) "</print>"
logic: "<logic" attribute* ">" text "</logic>"
attribute: ATTRIBUTE_NAME "=" ESCAPED_STRING

value:
    | true
    | false
    | ESCAPED_STRING 
    | SIGNED_NUMBER 
    | array
true: "True"
false: "False"
array: "[" (value | var_name)? ("," (value | var_name))* "]"

var_name: CNAME
text: /[^<]+/  // Matches text outside tags

// Terminals
ATTRIBUTE_NAME: /[a-zA-Z_][a-zA-Z0-9_-]*/
%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.CNAME
%import common.WS
%ignore WS
%ignore COMMENT
COMMENT: /<!--.*?-->/s

"""

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

def un_str(start: str) -> str:
    return start[1:-1]

def to_python (etch, last_keyword: str, tags: str): # NOT MY FINEST WORK | FUTURE MOTIERC, PLEASE FIX THIS, MAKE IT FASTER
    #print(etch)
    print(etch)
    return tags

def compile(file_location: str) -> None: # TODO: Tell when a loop/if ends
        with open(file_location) as code_read_file:
            start_code = code_read_file.read()
        tree_array = parse(start_code)
        """
        p_arr = tree_array[1][1][1:] + tree_array[1][2][1:]
        p_arr: list
        nested_array = p_arr
        #input(nested_array)
        p_arr = []
        stack = [(nested_array, 0)]
        last_keyword = None 
        tags = ""
        while stack:
            #input(f"\n{stack}")
            current_array, index = stack.pop()
            #print(f"\n--> {current_array}")
            try: 
                if current_array[0] in ["while_loop", "for_loop"]:
                    print("LOOOOOOP!")
            except Exception: pass

            while index < len(current_array):
                element = current_array[index]
                if isinstance(element, list):  # If the element is a list, push it onto the stack
                    if element[0] in ["attribute", "var_name", "value", "text"]: 
                        tags = to_python(element, last_keyword, tags)
                        index+=1
                        continue
                    stack.append((current_array, index + 1))  # Push the rest of the current list
                    stack.append((element, 0))  # Push the new list
                    break
                
                tags = to_python(element, last_keyword, tags)
                last_keyword = element
                index += 1
        """
        return tree_array


print(compile(CODE_LOCATION))