from flask import Flask, request, jsonify
from collections import deque
from flask_cors import CORS
stack = deque()

app = Flask(__name__)
CORS(app)
@app.route('/process-data', methods=['POST'])
def process_data():
    data = request.json.get('data')
    
    file = data.strip().split('\n')
    def find(history, i, j):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        targets = ['E']
        for direction in directions:
            new_i = i + direction[0]
            new_j = j + direction[1]
            
            if 0 <= new_i < len(file) and 0 <= new_j < len(file[i]):
                if file[new_i][new_j] in targets and history != [new_i, new_j]:
                    list.append([[60,60], new_i, new_j, 3])
                    stack.clear()
                elif file[new_i][new_j] == '1' and history != [new_i, new_j]:
                    stack.append([[i, j], new_i, new_j])
    list = []

    for rangei, i in enumerate(file):
        for rangej, j in enumerate(i):
            if j == "S":
                list.append([[60,60],rangei, rangej, 3])
                find([60, 60], rangei, rangej)
            lenst=0    
            lenrange=1   
            while stack:
                item = stack.pop()
                list.append([item[0], item[1], item[2], 3])
                find(item[0], item[1], item[2])



            nelist1=[]
            for i in list:
                nelist1.append([i[1],i[2]])

            left=list.copy()
            for i in nelist1:
                indices = [index for index, item in enumerate(left) if item[0] == i]
                if(len(indices)>1):
                    del left[indices[0]:indices[-1]]

            for item in list:
                if item in left:
                    index = left.index(item)
                    item[3]=1
            newlist =[]
            for i in list:
                newlist.append(i[1:])
    return jsonify(newlist)


if __name__ == '__main__':
    app.run()
