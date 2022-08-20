from products.option import Option

call_option = Option(100, 100, 0.01, 0.2, 1)
print(call_option.model().delta())
