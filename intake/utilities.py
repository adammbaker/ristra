def category_from_choices(choices, value):
    for category, options in choices:
        for option in options:
            if value.lower() in option:
                return category
    return None