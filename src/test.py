# Testing fizz buzz logic

fb_entry = int(input("enter number"))

fb_entry += 1

output = ""
divisor_1 = 3
divisor_2 = 5

if fb_entry % divisor_1 == 0:
    output += "fizz"
if fb_entry % divisor_2 == 0:
    output += "buzz"

if output == "":
    output = fb_entry

print(output)
