from model import BookingLine

def test_amount_formatted_bookingline():
    bookingline = BookingLine(amount=1234.56)
    assert bookingline.amount_formatted == "1.234,56"