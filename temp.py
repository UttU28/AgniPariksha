from flask import Flask, render_template, request, jsonify
import json
from time import sleep
import os

# import pyautogui as pi
# pi.hotkey('win','1')
# sleep(1)
# pi.hotkey('ctrl','shift','n')
# sleep(0.5)
# pi.typewrite('127.0.0.1:5000')
# sleep(0.5)
# pi.press('enter')

app = Flask(__name__)


# certificationName = "az-305"
iAmData = None
# with open(f"{certificationName}-questionData.json", "r") as oldFile: iAmData = json.load(oldFile)

# @app.route('/')
# def index():
#     return render_template('index.html', topics=get_unique_values('topicNumber'))

def get_certification_files():
    files = [f for f in os.listdir() if f.endswith('-questionData.json')]
    return [f for f in files]

@app.route('/')
def index():
    certification_files = get_certification_files()
    print(certification_files)
    return render_template('index.html', certification_files=certification_files)

@app.route('/selectCertification', methods=['POST'])
def selectCertification():
    certificationName = request.form['certification']
    file_name = f"{certificationName}"
    if file_name in os.listdir():
        with open(file_name, "r") as oldFile:
            iAmData = json.load(oldFile)
            # print(iAmData)
        return render_template('topics.html', topics=get_unique_values('topicNumber', iAmData), certificationName=certificationName)
    else:
        return "Error: File not found."

@app.route('/filter', methods=['POST'])
def dataFiltering():
    selectedTopics = request.form.getlist('topic')
    for i in range(len(selectedTopics)):
        if len(selectedTopics[i]) == 1:
            selectedTopics[i]= '0' + selectedTopics[i]
    print("selectedTopics", selectedTopics)
    certificationName = request.form['certificationName']
    print("certificationName", certificationName)
    with open(f"{certificationName}", "r") as oldFile: iAmData = json.load(oldFile)
    filteredData = [d for d in iAmData if str(d['topicNumber']) in selectedTopics]
    print(len(filteredData))
    return render_template('results.html', filteredData=filteredData, currentIndex=0, selectedTopics=selectedTopics, certificationName=certificationName)

@app.route('/navigate', methods=['POST'])
def navigate():
    currentIndex = int(request.form['currentIndex'])
    direction = request.form['direction']
    selectedTopics = request.form['selectedTopics']
    print("selectedTopics", selectedTopics)
    filteredData = [d for d in iAmData if str(d['topicNumber']) in selectedTopics]
    print(len(filteredData))
    # filteredData = [d for d in iAmData if str(d['topicNumber']) in selectedTopics]
    # filteredData = request.form['filteredData']
    print(currentIndex, direction, request.form['selectedTopics'], len(filteredData))
    if direction == 'next':
        currentIndex = (currentIndex + 1) % len(filteredData)
    elif direction == 'previous':
        currentIndex = (currentIndex - 1) % len(filteredData)
    return render_template('results.html', filteredData=filteredData, currentIndex=currentIndex, selectedTopics=selectedTopics)


def get_unique_values(key, thisData):
    return sorted(list({int(d[key]) for d in thisData}))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
