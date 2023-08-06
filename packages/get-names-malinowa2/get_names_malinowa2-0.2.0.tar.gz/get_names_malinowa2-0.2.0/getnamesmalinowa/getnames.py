import names as nm


def get_random_male_full_name_len():
    name = nm.get_full_name(gender='male')
    print(f'{name} - {len(name)}')


def get_random_female_full_name_len():
    name = nm.get_full_name(gender='female')
    print(f'{name} - {len(name)}')


def get_random_male_first_name_len():
    name = nm.get_first_name(gender='male')
    print(f'{name} - {len(name)}')


def get_random_female_first_name_len():
    name = nm.get_first_name(gender='female')
    print(f'{name} - {len(name)}')

