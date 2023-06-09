import random

time = ['day', 'night', 'evening', 'sunrise', 'sunset']
objects = ['forest','desert','grassland']
atmosphere = ['foggy', 'raining', 'clear sky']
elements = ['grass', 'flowers', 'waterfall', 'mountains', 'hills', 'trench']
mood = ['vibrant', 'dark', 'gloomy', 'bright']

def generate_prompt():
    random_time = random.choice(time)
    random_atmosphere = random.choice(atmosphere)
    random_elements = random.sample(elements, k=3)
    random_mood = random.choice(mood)
    random_object = random.choice(objects)
    return f"A {random_object} with {random_atmosphere} at {random_time} with {', '.join(random_elements)}, {random_mood}"
    