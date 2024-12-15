import toml
import re
import sys

# Парсер для учебного конфигурационного языка
def parse_config(input_text):
    constants = {}

    def parse_value(value):
        if value.isdigit():
            return int(value)
        elif re.match(r'^\(\s*(\d+\s*,\s*)*\d*\s*\)$', value):
            items = re.findall(r'\d+', value)
            return [int(item) for item in items]
        else:
            raise ValueError(f"Недопустимое значение: {value}")


    def evaluate_expression(expression):
        tokens = expression.split()
        stack = []

        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token in constants:
                stack.append(constants[token])
            elif token in ('+', '-', '*'):
                if len(stack) < 2:
                    raise ValueError(f"Недостаточно операндов для операции '{token}' в выражении: {expression}")
                b, a = stack.pop(), stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
            elif token == 'min()':
                if len(stack) < 2:
                    raise ValueError(f"Недостаточно операндов для функции 'min()' в выражении: {expression}")
                stack.append(min(stack.pop(), stack.pop()))
            elif token == 'len()':
                if not stack:
                    raise ValueError(f"Недостаточно операндов для функции 'len()' в выражении: {expression}")
                stack.append(len(stack.pop()))
            else:
                raise ValueError(f"Недопустимый токен в выражении: {token}")

        if len(stack) != 1:
            raise ValueError(f"Ошибка вычисления выражения: {expression}, итоговый стек: {stack}")

        return stack[0]


    def parse_line(line):
        match = re.match(r'var\s+([a-zA-Z][a-zA-Z0-9]*)\s*:=\s*(.+)', line)
        if match:
            name, value = match.groups()
            value = value.strip()
            if value.startswith('${') and value.endswith('}'):
                expression = value[2:-1].strip()
                constants[name] = evaluate_expression(expression)
            else:
                constants[name] = parse_value(value)
        else:
            raise ValueError(f"Синтаксическая ошибка в строке: {line}")

    cleaned_text = input_text.strip()

    for line in cleaned_text.splitlines():
        line = line.strip()
        if not line:
            continue
        parse_line(line)

    return constants

# Основная функция командной строки
def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_text = f.read()

        constants = parse_config(input_text)
        toml_output = toml.dumps({"constants": constants})
        print(toml_output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
