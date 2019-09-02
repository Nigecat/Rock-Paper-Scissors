#0 + 0 = 0
#0 + 1 = 1
#0 + 2 = 2
#1 + 2 = 3
#2 + 2 = 4
#1 + 1 = 2 (5)

#Functions to format the data before it goes into the json file

# TODO these functions

def compress(data):
    '''Function to compress the input data

    data -- list of ints (0, 1, 2)
    '''
    newData = []
    for i in range(0, len(data) - 1, 2):
        if data[i] + data[i + 1] != 2:
            newData.append(data[i] + data[i + 1])
        else:
            if data[i] == 1 and data[i + 1] == 1:
                newData.append(5)
            else:
                newData.append(data[i] + data[i + 1])
                
    if len(data) != len(newData):
        newData.append(data[-1])

    return newData

def decompress(data):
    '''Function to decompress the input data

    data -- list of compressed data
    '''
    newData = []
    for i in range(len(data)):
        if data[i] == 0:
            newData.append(0)
            newData.append(0)
        elif data[i] == 1:
            newData.append(0)
            newData.append(1)
        elif data[i] == 2:
            newData.append(0)
            newData.append(2)
        elif data[i] == 3:
            newData.append(1)
            newData.append(2)
        elif data[i] == 4:
            newData.append(2)
            newData.append(2)
        elif data[i] == 5:
            newData.append(1)
            newData.append(1)

    return newData

if __name__ == "__main__":
    testStr = [0, 1, 0, 2, 2, 2, 1, 0, 2, 1, 2, 0, 2, 2, 2, 1, 1, 0, 2, 0, 1, 1, 2, 2, 2, 1, 0, 2, 0, 1, 2, 0, 0, 1, 2, 2, 1, 0, 1, 2, 0, 2, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 2, 2, 1, 0, 1, 0, 2, 2, 1, 0, 0, 0, 0, 0, 2, 2, 1, 0]
    print(f"INPUT: \n{testStr}")
    print(compress(testStr))
    print(decompress(compress(testStr)))
    input()