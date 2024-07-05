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

    # Uncomment this block to pass the first stage
    if file_contents:
        line_no = 1
        for ch in file_contents:
            ch_name = ""
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
            elif ch == "\n":
                line_no += 1
            else:
                print(f"[line {line_no}] Error: Unexpected character: {ch}")
                continue
            print(f"{ch_name} {ch} null")
        print("EOF  null") # Placeholder, remove this line when implementing the scanner
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
