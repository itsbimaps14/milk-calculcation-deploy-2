def format_idr(amount):
    s = f"{amount:,.2f}"  # Format like 347,453,460.00
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"IDR {s}"