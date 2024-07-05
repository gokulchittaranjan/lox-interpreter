import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
    exit_code = 0
    # Uncomment this block to pass the first stage
    toks = []
    errs = []
    if file_contents:
        line_no = 1
        ptr = 0
        inside_comment = False
        inside_string = False
        literal = []
        inside_number = False
        number = []

        while ptr < len(file_contents):

            ch = file_contents[ptr]
            ch_name = ""
            if ch == "\n":
                line_no += 1
                inside_comment = False
                ptr += 1
                continue
            if inside_string:
                if ch != '"':
                    literal.append(ch)
                else:
                    string = ''.join(literal)
                    toks.append(f'STRING "{string}" {string}')
                    inside_string = False
                    literal = []
                ptr += 1
                continue
            if inside_number:
                if ch not in "0123456789." or ("." in number and ch == "."):
                    # print(number, ch, inside_number, line_no, ptr)
                    inside_number = False
                    number = "".join(number)
                    if number[-1] == ".":
                        toks.append(f'NUMBER {number[:-1]} {number[:-1]}.0')
                        toks.append(f'DOT . null')
                    else:
                        if "." not in number:
                            toks.append(f'NUMBER {number} {number}.0')
                        else:
                            toks.append(f'NUMBER {number} {number}')
                    number = []
                else:
                    number.append(ch)
                    ptr += 1
                    continue
            if inside_comment:
                ch = ""
            if ch == "(":
                ch_name = "LEFT_PAREN"
            elif ch == ")":
                ch_name = "RIGHT_PAREN"
            elif ch == "{":
                ch_name = "LEFT_BRACE"
            elif ch == "}":
                ch_name = "RIGHT_BRACE"
            elif ch == ",":
                ch_name = "COMMA"
            elif ch == ".":
                ch_name = "DOT"
            elif ch == "+":
                ch_name = "PLUS"
            elif ch == "-":
                ch_name = "MINUS"
            elif ch == ";":
                ch_name = "SEMICOLON"
            elif ch == "*":
                ch_name = "STAR"
            elif ch == "=":
                if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "=":
                    ch_name = "EQUAL_EQUAL"
                    ch = "=="
                else:
                    ch_name = "EQUAL"
            elif ch == "!":
                if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "=":
                    ch_name = "BANG_EQUAL"
                    ch = "!="
                else:
                    ch_name = "BANG"
            elif ch == "<":
                if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "=":
                    ch_name = "LESS_EQUAL"
                    ch = "<="
                else:
                    ch_name = "LESS"
            elif ch == ">":
                if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "=":
                    ch_name = "GREATER_EQUAL"
                    ch = ">="
                else:
                    ch_name = "GREATER"
            elif ch == "/":
                if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "/":
                    inside_comment = True
                    ch = ""
                else:
                    ch_name = "SLASH"
            elif ch == '"':
                inside_string = True
                ptr += 1
                continue
            elif ch != "" and ch in "0123456789":
                inside_number = True
                number.append(ch)
                ptr += 1
                continue
            elif ch == " " or ch == "\t":
                ptr += 1
                continue
            elif ch != "":
                errs.append(f"[line {line_no}] Error: Unexpected character: {ch}")
                exit_code = 65
                ptr += 1
                continue
            if len(ch) > 0:
                ptr += len(ch)
                toks.append(f"{ch_name} {ch} null")
            else:
                ptr += 1
        if inside_string:
            errs.append(f"[line {line_no}] Error: Unterminated string.")
            exit_code = 65
        if inside_number and len(number) > 0:
            number = "".join(number)
            if number[-1] == ".":
                toks.append(f'NUMBER {number[:-1]} {number[:-1]}.0')
                toks.append(f'DOT . null')
            else:
                if "." not in number:
                    toks.append(f'NUMBER {number} {number}.0')
                else:
                    toks.append(f'NUMBER {number} {number}')
        toks.append("EOF  null") # Placeholder, remove this line when implementing the scanner
        print("\n".join(errs), file=sys.stderr)
        print("\n".join(toks))
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner
    exit(exit_code)


if __name__ == "__main__":
    main()
