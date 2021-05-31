numbers_to_words1 = {
    0: 'Zero',
    1: 'One',
    2: 'Two',
    3: 'Three',
    4: 'Four',
    5: 'Five',
    6: 'Six',
    7: 'Seven',
    8: 'Eight',
    9: 'Nine',
    10: 'Ten',
    11: 'Eleven',
    12: 'Twelve',
    13: 'Thirteen',
    14: 'Fourteen',
    15: 'Fifteen',
    16: 'Sixteen',
    17: 'Seventeen',
    18: 'Eighteen',
    19: 'Nineteen'
}
numbers_to_words2 = [
    'Twenty',
    'Thirty',
    'Forty',
    'Fifty',
    'Sixty',
    'Seventy',
    'Eighty',
    'Ninety'
]


def number(number_int: int) -> str:
    if 0 <= number_int <= 19:
        return numbers_to_words1[number_int]
    elif 20 <= number_int <= 99:
        t, r = divmod(number_int, 10)
        return numbers_to_words2[t - 2] + ' ' + numbers_to_words1[r] if r else numbers_to_words2[t - 2]