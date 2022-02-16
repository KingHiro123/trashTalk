import random
import string


def create_sku():
    str1 = ''.join((random.choice(string.ascii_letters)
                    for x in range(4)))
    str1 += ''.join((random.choice(string.digits)
                    for x in range(4)))

    sam_list = list(str1)  # it converts the string to list.
    # It uses a random.shuffle() function to shuffle the string.
    random.shuffle(sam_list)
    final_string = ''.join(sam_list)
    final_string = "SKU" + final_string

    return final_string