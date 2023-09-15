# from pywinauto import application

# app1 = application.Application()
# class notepadAuto():

#     def __init__(self):
#         self.app = application.Application()

#     def open(self):
#         self.app.start("Notepad.exe")


#     def write(self,voice_input):
#         self.app.Notepad.Edit.type_keys(voice_input,with_spaces=True)


#     def close(self):
#         self.app.kill()


def minNum(threshold, points):
    if points[-1] - points[0] < threshold:
        return len(points)

    minProblemCount = 0

    for i in range(1, len(points)):

        if points[i] - points[0] >= threshold:
            minProblemCount = ((i+1)//2) + 1
            break
        
    return minProblemCount


def sumFunc(a, b, carry):

    if a == "1" and b == "1" and carry == "0":
        return "0", "1"
    if a == "0" and b == "0" and carry == "0": 
        return "0", "0"
    if a == "1" and b == "0" and carry == "0":
        return "1", "0"
    if a == "0" and b == "1" and carry == "0":
        return "1", "0"
    if a == "1" and b == "1" and carry == "1":
        return "1", "1"
    if a == "0" and b == "0" and carry == "1":
        return "1", "0"
    if a == "1" and b == "0" and carry == "1":
        return "0", "1"
    if a == "0" and b == "1" and carry == "1":
        return "0", "1"

def solution(a, b):

    i = len(a) - 1
    j = len(b) - 1
    carry = "0"
    output = ""
    sumOfChars = "0"
    while i >=0  or j >= 0:

    
        charA = "0" if i < 0 else a[i]
        charB = "0" if j < 0 else b[j]

        sumOfChars, carry = sumFunc(charA, charB, carry)
        # finalSum, carry = sumFunc(sumOfChars, carry)
        output = sumOfChars+""+output

        i-=1
        j-=1

    if carry == "1":
        output = carry+""+output

    print(output)

def main():

    # points = [1, 2, 3, 4, 5]
    # # minNum(2, points)
    # print(minNum(4, points))
    solution("1", "10")

  
if __name__ == '__main__':
    main()