from flask import Flask, render_template, request, jsonify
import json
import pyautogui as pi
from time import sleep

# pi.hotkey('win','1')
# sleep(1)
# pi.hotkey('ctrl','shift','n')
# sleep(0.5)
# pi.typewrite('127.0.0.1:5000')
# sleep(0.5)
# pi.press('enter')

app = Flask(__name__)


certificationName = "az-305"
iAmData = None
with open(f"{certificationName}-questionData.json", "r") as oldFile: iAmData = json.load(oldFile)

@app.route('/')
def index():
    return render_template('index.html', topics=get_unique_values('topicNumber'))

@app.route('/filter', methods=['POST'])
def dataFiltering():
    selectedTopics = request.form.getlist('topic')
    for i in range(len(selectedTopics)):
        if len(selectedTopics[i]) == 1:
            selectedTopics[i]= '0' + selectedTopics[i]
    print("selectedTopics", selectedTopics)
    filteredData = [d for d in iAmData if str(d['topicNumber']) in selectedTopics]
    print(len(filteredData))
    return render_template('results.html', filteredData=filteredData, currentIndex=0, selectedTopics=selectedTopics)

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


def get_unique_values(key):
    return sorted(list({int(d[key]) for d in iAmData}))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
