import random

def generateName():
    adjectives = [ "blue", "fuzzy", "green", "happy", "jolly", "kind", "little", "merry", "nice", "orange", "pretty", "quick", "red", "silly", "tiny", "yellow", "zany" ]
    nouns = ["apple", "banana", "carrot", "dog", "elephant", "frog", "giraffe", "horse", "iguana", "jellyfish", "kangaroo", "lion", "monkey", "newt", "owl", "penguin", "quail", "rabbit", "snake", "tiger", "unicorn", "vulture", "walrus", "xerus", "yak", "zebra"]
    return f"{adjectives[random.randint(0, len(adjectives) - 1)]}-{nouns[random.randint(0, len(nouns) - 1)]}"

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip