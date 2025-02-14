import SERIAL.dict.normal as nomal

data = b'\xc9'
print("data is ", data)
if data in nomal.comand:
    print("True")
else:
    print("False")