import decimal    


def num2words(num):
    minus = ''
    if int(num)<0:
        num = -num
        minus = 'Minus '
    num = decimal.Decimal(num)
    decimal_part = num - int(num)
    num = int(num)

    if decimal_part:
        return num2words(num) + " point " + (" ".join(num2words(i) for i in str(decimal_part)[2:]))

    under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crore'}

    if num < 20:
        print(num)
        return under_20[num]

    if num < 100:
        return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

    # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
    pivot = max([key for key in above_100.keys() if key <= num])

    return minus + num2words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot == 0 else ' ' + num2words(num % pivot))


def d2w(digits):
    number = str(digits)
    return num2words(decimal.Decimal(number))


def num2words_b(num):
    minus = ''
    if int(num)<0:
        num = -num
        minus = 'Minus '
    num = decimal.Decimal(num)
    decimal_part = num - int(num)
    num = int(num)

    if decimal_part:
        return num2words_b(num) + " দশমিক " + (" ".join(num2words_b(i) for i in str(decimal_part)[2:]))

    under_20 = ['শূন্য', 'এক', 'দুই', 'তিন', 'চার', 'পাঁচ', 'ছয়', 'সাত', 'আট', 'নয়', 'দশ', 'এগার', 'বার', 'তের', 'চৌদ্দ',
                'পনের', 'ষোল', 'সতের', 'আঠার', 'ঊনিশ', 'বিশ', 'একুশ', 'বাইশ', 'তেইশ', 'চব্বিশ', 'পচিশ', 'ছাব্বিশ', 'সাতাশ', 'আঠাশ',
                'উনত্রিশ', 'ত্রিশ','একত্রিশ', 'বত্রিশ', 'তেত্রিশ', 'চৌত্রিশ', 'পয়ত্রিশ', 'ছত্রিশ', 'সাতত্রিশ', 'আটত্রিশ', 'ঊনচল্লিশ', 'চল্লিশ', 'একচল্লিশ',
                'বিয়াল্লিশ', 'তেতাল্লিশ', 'চুয়াল্লিশ', 'পয়তাল্লিশ', 'ছয়চল্লিশ', 'সাতচল্লিশ', 'আটচল্লিশ', 'উনপঞ্চাশ', 'পঞ্চাশ', 'একান্ন', 'বায়ান্ন', 'তিপ্পান্ন',
                'চুয়ান্ন', 'পঞ্চান্ন', 'ছাপ্পান্ন', 'সাতান্ন', 'আটান্ন', 'ঊনষাট', 'ষাট', 'একষট্টি', 'বাষট্টি', 'তেষট্টি', 'চৌষট্টি', 'পয়ষট্টি', 'ছেষট্টি', 'সাষট্টি',
                'আটষট্টি', 'ঊনসত্তর', 'সত্তর', 'একাত্তর', 'বাহাত্তর', 'তেহাত্তর', 'চুয়াত্তর', 'পচাত্তর', 'ছিয়াত্তর', 'সাতাত্তর', 'আটাত্তর', 'ঊনআশি', 'আশি',
                'একাশি', 'বিরাশি', 'তিরাশি', 'চৌরাশি', 'পচাশি', 'ছিয়াশি', 'সাতাশি', 'আটাশি', 'ঊননব্বই', 'নব্বই', 'একানব্বই', 'বিরানব্বই', 'তিরানব্বই',
                'চুরানব্বই', 'পচানব্বঈ', 'ছিয়ানব্বই', 'সাতানব্বই', 'আটানব্বই', 'নিরানব্বই', 'একশত', ]
    tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    above_100 = {100: 'শত', 1000: 'হাজার', 100000: 'লক্ষ', 10000000: 'কোটি'}

    if num <= 100:
        return under_20[num]

    # if num < 100:
    #     return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

    # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
    pivot = max([key for key in above_100.keys() if key <= num])

    return minus + num2words_b(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot == 0 else ' ' + num2words_b(num % pivot))


def d2wb(digits):
    number = str(digits)
    return num2words_b(decimal.Decimal(number))