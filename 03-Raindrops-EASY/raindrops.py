def convert(number: int) -> str:
    result = ''
    factors = [3, 5, 7]
    sounds = ['Pling', 'Plang', 'Plong']
    for factor, sound in zip(factors, sounds):
        if number % factor == 0:
            result += sound
    return result if result != '' else str(number)
