import ast


def whichAlgorithm(problem):
    problem = problem.strip()
    if "=" in problem:
        problem = problem[:-1]
    while True:
        if "+" in problem and "-" not in problem and "*" not in problem:
            problem = problem.replace("+", "")
            problem = problem.replace(" ", "")
            try:
                result = int(problem)
                return justAddition(problem)
            except: continue
        if "-" in problem and "+" not in problem and "*" not in problem:
            problem = problem.replace("-", "")
            problem = problem.replace(" ", "")
            try:
                result = int(problem)
                return justSubtraction(problem)
            except: continue
        if "*" in problem and "+" not in problem and "-" not in problem:
            problem = problem.replace("*", "")
            problem = problem.replace(" ", "")
        try:
            result = int(problem)
            return justMultiplication(problem)
        except:
            return None

def justAddition(problem):
    ans = 0
    values = list(problem)
    for num in values:
        ans += int(num)
    return ans

def justSubtraction(problem):
    subtract = 0
    values = list(problem)
    base = int(values[0])
    for num in values[1:]:
        subtract += int(num)
    return base - subtract

def justMultiplication(problem):
    answer = 1
    values = list(problem)
    for item in values:
        answer *= int(item)
    return answer

def useEval(problem):
    if "=" in problem:
        problem = problem[0:-1]
    problem = list(problem)
    if "+" in problem:
        while "+" in problem:
            index = problem.index("+")
            problem.pop(index)
    if "-" in problem:     
        while "-" in problem:
            index = problem.index("-")
            problem.pop(index)
    if "*" in problem:
        while "*" in problem:
            index = problem.index("*")
            problem.pop(index)
    if "/" in problem:
        while "/" in problem:
            index = problem.index("/")
            problem.pop(index)
    problem = "".join(problem)
    try:
        result = int(problem)
        return True
    except: return False


############################
#test functions
############################
def testWhichAl():
    test1 = "4+2+7"
    test2 = "6-4-2"
    test3 = "8*9"
    test4 = " 8+5 = "
    test5 = "8*3+4"
    assert(whichAlgorithm(test1) == 13)
    assert(whichAlgorithm(test2) == 0)
    assert(whichAlgorithm(test3) == 72)
    assert(whichAlgorithm(test4) == 13)
    assert (whichAlgorithm(test5) == None)

def testUseEval():
    test1 = "1+3+5*2-1"
    test2 = "integral(1/2+3)"
    test3 = "derivative(3-6+2/4)"
    test4 = "3+4/2-5*6"
    assert(useEval(test1) == True)
    assert(useEval(test2) == False)
    assert(useEval(test3) == False)
    assert(useEval(test4) == True)
    print("Passed!")

def testJustAddition():
    # print ("testingJustAddition...", end="")
    test1 = "12+2+30 = "
    test2 = "5+3+9+10"
    test3 = "3+9+2+1 ="
    assert(justAddition(test1) == 44)
    assert(justAddition(test2) == 27)
    assert(justAddition(test3) == 15)
    print ("Passed!")

def testJustSubtraction():
    test1 = "5-2-1"
    test2 = "9-2-3 = "
    test3 = "10-3-1 "
    assert(justSubtraction(test1) == 2)
    assert(justSubtraction(test2) == 4)
    assert(justSubtraction(test3) == 6)

def testJustMultiplication():
    test1 = "4*3*2="
    test2 = "12*2*1"
    test3 = "3*7*2"
    assert(justMultiplication(test1) == 24)
    assert(justMultiplication(test2) == 24)
    assert(justMultiplication(test3) == 42)

