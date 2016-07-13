def print_card(fields, large_field=False, free_field=False,
               comment='', is_commented=False,
               use_continuation_marks=True):
    card = fields[0]

    if large_field:
        card += '*'
        field_length = 16
        n_fields = 4
        continuation_mark = '*'
    else:
        field_length= 8
        n_fields = 8

        if use_continuation_marks:
            continuation_mark = '+'
        else:
            continuation_mark = ''

    if free_field:
        separator = ','
    else:
        separator = ''
        card = card.ljust(8)

    if is_commented:
        comment_mark = '$ '
    else:
        comment_mark = ''

    col = 0

    for field in fields[1:]:
        col += 1

        if col > n_fields:
            col = 1

            card += continuation_mark + '\n'

            if free_field:
                card += comment_mark + continuation_mark + separator
            else:
                card += comment_mark + continuation_mark.ljust(8)

        if field != '':
            card_length = len(card)

        card += separator + print_field(field, field_length, free_field)

    return comment + comment_mark + card[:card_length] + '\n'


def print_field(value, field_length=8, free_field=False):

    if isinstance(value, float):
        field = print_double(value, field_length=field_length)
    elif isinstance(value, int):
        field = str(value).rjust(field_length)
    else:
        field = value.upper().rjust(field_length)

    if free_field:
        return field.strip()
    else:
        return field


def print_double(value, field_length=8):
    f_format = '{{0: {}.{}{}}}'.format(field_length, field_length - 1, 'f')
    E_format = '{{0: {}.{}{}}}'.format(field_length, field_length - 1, 'E')
    exponent = ''
    available_chars = field_length

    if value == 0:
        significant = '0.0'
    elif (-100000 < value and value <= -0.001 or
        0.001 <= value and value < 100000):
        value_str = f_format.format(value)
        significant = value_str[0] + value_str[1:field_length].strip('0')
    else:
        value_str = E_format.format(value)
        E_index = value_str.index('E')
        significant = value_str[:E_index][:field_length].strip('0')
        exponent = value_str[E_index + 1:]

        if exponent[1] == '0':
            exponent = exponent[0] + exponent[2:]

        available_chars = field_length - len(exponent)

        if len(significant) < available_chars:
            exponent = 'E' + exponent
            available_chars -= 1

    if significant[-1] == '.':
        significant += '0'

    return (significant[:available_chars] + exponent).rjust(field_length)