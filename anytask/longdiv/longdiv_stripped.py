def two_dim_array_to_string(lines):
    string = ""
    for line in lines:
        for char in line:
            string += char
        string += "\n"
    return string[:len(string) - 1]


def long_division(dividend, divider):
    lines = [list(str(dividend) + "|" + str(divider))]
    quotient = dividend // divider
    incomplete_divisible = ""
    left_indent = ""
    index_digit_of_quotient = 0
    for digit_of_divisible in str(dividend):
        incomplete_divisible += digit_of_divisible
        if int(incomplete_divisible) < divider:
            if index_digit_of_quotient != 0:
                index_digit_of_quotient += 1
            continue
        else:
            deductible = divider \
                         * int(str(quotient)[index_digit_of_quotient])
            if deductible == 0:
                index_digit_of_quotient += 1
                continue
            if index_digit_of_quotient != 0:
                if incomplete_divisible[0] == "0":
                    incomplete_divisible = incomplete_divisible[1:]
                    left_indent += " "
                lines.append(list(left_indent + incomplete_divisible))
            difference = int(incomplete_divisible) - deductible
            left_indent += (len(incomplete_divisible)
                            - len(str(deductible))) * " "
            lines.append(list(left_indent + str(deductible)))
            left_indent += (len(str(deductible))
                            - len(str(difference))) * " "
            index_digit_of_quotient += 1
            incomplete_divisible = str(difference)
    if int(incomplete_divisible) == 0:
        lines.append(list(left_indent + str(int(incomplete_divisible))))
    else:
        lines.append(list((len(incomplete_divisible)
                           - len(str(int(incomplete_divisible)))) * " "
                          + left_indent + str(int(incomplete_divisible))))
    lines[1] += list((len(str(dividend)) - len(lines[1]))
                     * " " + "|" + str(quotient))
    return two_dim_array_to_string(lines)


def main():
    print(long_division(123, 123))
    print()
    print(long_division(1, 1))
    print()
    print(long_division(15, 3))
    print()
    print(long_division(3, 15))
    print()
    print(long_division(12345, 25))
    print()
    print(long_division(1234, 1423))
    print()
    print(long_division(87654532, 1))
    print()
    print(long_division(24600, 123))
    print()
    print(long_division(4567, 1234567))
    print()
    print(long_division(246001, 123))
    print()
    print(long_division(100000, 50))
    print()
    print(long_division(123456789, 531))
    print()
    print(long_division(425934261694251, 12345678))


if __name__ == '__main__':
    main()
