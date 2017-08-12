from decimal import *

def convert_to_3places(float_):
    str_ = str(float_)
    return round(Decimal(str_), 3)

# print(convert_to_3places(2.0091750200663202e-08))
# print(convert_to_3places(2.675))
