import random
import re

test_rolls = [
        'd',
        '1d',
        'd2',
        '1d2',
        '3+d',
        '3-d',
        '33+1d',
        '33-1d',
        '55+1d2+4',
        '-3+32+1d2-4',
        '11+22d33-44',
        '20+11+22d33+32+4+5',
        'd2-1',
        'd2-1',
        'd2-1',
        'd2-1',
        ]

test_rolls2 = [
        '10+d',
        ]

test_grand_total_mods = [
        '10',
        '-20',
        '+20',
        '-10+10+10',
        ]


def roll(args):
    print("\nTEST\n")


    grand_total = 0
    roll_totals = []
    rolls = []

    # checks for correct argument syntax
    total_modifier_ptn = re.compile(r'^([+-]?[0-9]*)*$')
    roll_ptn = re.compile(
            # preceeding modifiers
            r'^([+-]?[0-9]+(?!d)[+-])*'
            # roll, ensure no double operator with r'(?<![+-])'
            r'((?<![+-])[+-])?[0-9]*d[0-9]*'
            # trailing modifiers
            r'([+-][0-9]+)*$'
            )

    # for retrieving lists of values from roll expression
    leading_mods_ptn = re.compile(r'^([+-]?[0-9]+(?![0-9]*d))+')
    trailing_mods_ptn = re.compile(r'([+-][0-9]+)+$')

    # for directly retrieving values, findall
    lead_mod_ptn = re.compile(r'[+-]?[0-9]+')
    trail_mod_ptn = re.compile(r'[+-][0-9]+')
    count_ptn = re.compile(r'[+-]*[0-9]+(?=d)')
    sides_ptn = re.compile(r'(?<=d)[0-9]+')

    for arg in args:
        if total_modifier_ptn.search(arg):
            modifiers = re.findall(r'[+-]?[0-9]*', arg)
            for mod in modifiers:
                if not mod:
                    continue
                grand_total += int(mod)

            print("TOTAL", arg)
            print("totals", modifiers)
            print("grand total", grand_total)
            print('')

        if roll_ptn.search(arg):
            modifier = 0
            count = 1
            sides = 20
            roll_values = []
            roll_total = 0

            lead_mods_match = leading_mods_ptn.search(arg)
            trail_mods_match = trailing_mods_ptn.search(arg)
            count_match = count_ptn.search(arg)
            sides_match = sides_ptn.search(arg)

            if lead_mods_match:
                modifiers = lead_mod_ptn.findall(lead_mods_match.group())
                for mod in modifiers:
                    modifier += int(mod)

            if trail_mods_match:
                modifiers = trail_mod_ptn.findall(trail_mods_match.group())
                for mod in modifiers:
                    modifier += int(mod)

            if count_match:
                count = int(count_match.group())

            if sides_match:
                sides = int(sides_match.group())

            for _ in range(abs(count)):
                value = random.randint(1, sides)
                value = value * -1 if count < 0 else value
                roll_values.append(value)
                roll_total += value

            roll_total += int(modifier)
            grand_total += roll_total

            print("ROLL", arg)
            print('modifier', modifier)
            print('count', count)
            print('sides', sides)
            print('roll values', roll_values)
            print('roll total', roll_total)
            print('grand total', grand_total)
            print('')


def roll_test(args):
    print("\nTEST\n")

    roll_ptn = re.compile(
            # preceeding modifiers
            r'^([+-]?[0-9]+(?!d)[+-])*'
            # roll, ensure no double operator with r'(?<![+-])'
            r'((?<![+-])[+-])?[0-9]*d[0-9]*'
            # trailing modifiers
            r'([+-][0-9]+)*$'
            )
    total_modifier_ptn = re.compile(r'^([+-]?[0-9]*)*$')

    grand_total = 0
    for arg in args:
        if total_modifier_ptn.search(arg):
            modifiers = re.findall(r'[+-]?[0-9]*', arg)
            for mod in modifiers:
                if not mod:
                    continue
                grand_total += int(mod)

            print("TOTAL", arg)
            print("totals", modifiers)
            print("grand total", grand_total)
            print('')

        if roll_ptn.search(arg):
            start_mods = re.search(r'^([+-]?[0-9]+(?![0-9]*d))+', arg)
            end_mods = re.search(r'([+-][0-9]+)+$', arg)
            countEx = re.search(r'[+-]*[0-9]+(?=d)', arg)
            sidesEx = re.search(r'(?<=d)[0-9]+', arg)
            modifier = 0
            count = 1
            sides = 20
            roll_values = []
            roll_total = 0

            if start_mods:
                modifiers = re.findall(r'[+-]?[0-9]+', start_mods.group())
                print('start mods', modifiers)
                for mod in modifiers:
                    modifier += int(mod)

            if end_mods:
                modifiers = re.findall(r'[+-][0-9]+', end_mods.group())
                print('end mods', modifiers)
                for mod in modifiers:
                    modifier += int(mod)

            if countEx:
                count = int(countEx.group())
            if sidesEx:
                sides = int(sidesEx.group())
            for _ in range(abs(count)):
                value = random.randint(1, sides)
                value = value * -1 if count < 0 else value
                roll_values.append(value)
                roll_total += value

            grand_total += roll_total
            grand_total += int(modifier)

            print("ROLL", arg)
            print('modifier', modifier)
            print('count', count)
            print('sides', sides)
            print('roll values', roll_values)
            print('grand total', grand_total)
            print('')


roll(test_rolls2)
# roll(test_grand_total_mods)
