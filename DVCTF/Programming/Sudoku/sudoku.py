# import requests module
import json
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from datetime import datetime

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

# create a session object
s = requests.Session()

def getSudoku(url,s) :

    # make a get request
    r = s.get(url)
    # check if cookie is still set
    soup = BeautifulSoup(r.content, 'html.parser')
    #print(soup.prettify())
    p = soup.find_all("input", {"class": re.compile(r"case[\s\S]*")})
    return p

def rememberInput(sud):
    listInput = []
    for i in range(len(sud)):
        r = re.findall("[name]*[\d]{1,2}", str(sud[i]))
        if (len(r) == 1):
             listInput.append(int(r[0])-1)
    return listInput
        
            
def createSudoku(sud):
    sudoku = np.zeros([9,9],dtype=int)
    for i in range(len(sud)):
        r = re.findall("[name]*[\d]{1,2}", str(sud[i]))
        if (len(r) == 2):
            #print("Regex match is : lines ",r[0]," and value : ",r[1])
            col = (int(r[0]) - 1) % 9
            row = (int(r[0]) - 1) // 9
            #print("Column Values is : ",col," and row :",row)
            sudoku[row][col]=r[1]
    return sudoku

M = 9

def solve(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
             
    for x in range(9):
        if grid[x][col] == num:
            return False
 
 
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True
 
def Suduko(grid, row, col):
 
    if (row == M - 1 and col == M):
        return True
    if col == M:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return Suduko(grid, row, col + 1)
    for num in range(1, M + 1, 1): 
     
        if solve(grid, row, col, num):
         
            grid[row][col] = num
            if Suduko(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False

def matrixToDict(matrix, listInput):
    myDict = {}
    for i in range(9):
        for j in range(9):
            if ( i*9+j in listInput):
                myDict[str(i*9+j+1)]=matrix[i][j]
    print(myDict) 
    return myDict   

def sendSudoku(url,sudokuGrid,session):
    inputSudoku = rememberInput(sud)
    data = matrixToDict(sudokuGrid,inputSudoku)
    print("Data sent to POST request")
    post = session.post(url, data = data)
    soup = BeautifulSoup(post.content, 'html.parser')
    print(soup.prettify())
    p = soup.find_all("div", {"class": "u4"})

bef = datetime.now()
print(" \nGetting the Sudoku ...")
sud = getSudoku("http://challs.dvc.tf:6002/home?",s)

print("Creating the Sudoku ...")
sudokuGrid = createSudoku(sud)
print(" \nThe sudoku is : \n",sudokuGrid)

print(" \nRemebering the input ...")
inputSudoku = rememberInput(sud)
print(" \nThe sudoku empty values are : \n",inputSudoku)


print(" \nSolving the Sudoku ...")
if (Suduko(sudokuGrid, 0, 0)):
    print(sudokuGrid)
else:
    print(" \nSolution does not exist:(")


print(" \nSending the Sudoku ...")
sendSudoku("http://challs.dvc.tf:6002/flag",sudokuGrid,s)

af = datetime.now()

print("Timme the program took : ",af-bef)