from random import choice

emojies = {
        '#': '#️⃣',
        '*': '*️⃣',
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
        }

emoji_numbers = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
        }

emoji_to_numbers = {
        '0️⃣': '0',
        '1️⃣': '1',
        '2️⃣': '2',
        '3️⃣': '3',
        '4️⃣': '4',
        '5️⃣': '5',
        '6️⃣': '6',
        '7️⃣': '7',
        '8️⃣': '8',
        '9️⃣': '9',
        }

def welcome(mention):
    messages = [
            f'Welcome to Costco {mention}... I love you.',
            f'Hey {mention}, did you bring the toe dip?',
            f'Here\'s {mention}!',
            f'Hello there {mention}',
            (
                f'Good morning {mention}, and in case I don\'t see ya,'
                ' good afternoon, good evening, and good night!'
            ),
            (
                f'Hello. My name is {mention}.'
                ' You killed my father. Prepare to die',
            ),
            f'You talkin\' to me {mention}?'
            ]
    return choice(messages)
