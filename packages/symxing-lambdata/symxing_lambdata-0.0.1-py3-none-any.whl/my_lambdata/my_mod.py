def enlarge(n):
    """
    Param n is a number
    Function will enlarge the number
    """
    return n * 100

#y = int(input("Please choose a number"))

#print(y, enlarge(y))

if __name__ == "__main__":
    # only run the code below IF this script is invoked from THIS .py
    # not if imported from other script
    print("HELLO")
    y = int(input("Please choose a number"))
    print(y, enlarge(y))