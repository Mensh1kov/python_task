def two_dim_arr_to_str(lines):
    string = ""
    for line in lines:
        for char in line:
            string += char
        string += "\n"
    return string[:len(string) - 1]


def long_division(dividend, divider):
    lines = [list(str(dividend) + "|" + str(divider))]
    quotient = str(dividend // divider)
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
            digit_of_quotient = int(quotient[index_digit_of_quotient])
            deductible = str(divider * digit_of_quotient)
            if deductible == 0:
                index_digit_of_quotient += 1
                continue
            if index_digit_of_quotient != 0:
                if incomplete_divisible[0] == "0":
                    incomplete_divisible = incomplete_divisible[1:]
                    left_indent += " "
                lines.append(list(left_indent + incomplete_divisible))
            difference = str(int(incomplete_divisible) - int(deductible))
            len_deductible = len(deductible)
            left_indent += (len(incomplete_divisible) - len_deductible) * " "
            lines.append(list(left_indent + deductible))
            left_indent += (len_deductible - len(difference)) * " "
            index_digit_of_quotient += 1
            incomplete_divisible = difference
    remainder_division = str(int(incomplete_divisible))
    if remainder_division != "0":
        count_spase = len(incomplete_divisible) - len(remainder_division)
        left_indent += count_spase * " "
    lines.append(list(left_indent + remainder_division))
    count_spase = len(str(dividend)) - len(lines[1])
    lines[1] += list(count_spase * " " + "|" + quotient)
    return two_dim_arr_to_str(lines)


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
