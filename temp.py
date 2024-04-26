import json

certificationName = "az-400"

iAmData = None
with open(f"{certificationName}-rawData.json", "r") as oldFile: iAmData = json.load(oldFile)

dataCollector = []
# for questionBlock in iAmData[:2]:
for index, questionBlock in enumerate(iAmData):
    reformattedOptions = []
    correctAnswer = questionBlock['answerIs']
    votedAnswer = questionBlock['mostVotedIs']
    if questionBlock['isMCQ']:
        for option in questionBlock['myOptionsAre']:
            if option[0] == correctAnswer and votedAnswer == None:
                reformattedOptions.append({'text': option[3:], 'correct': True, 'voted': True})
            elif option[0] != correctAnswer and votedAnswer == None:
                reformattedOptions.append({'text': option[3:], 'correct': False, 'voted': False})
            elif option[0] == correctAnswer and option[0] == votedAnswer[0]:
                reformattedOptions.append({'text': option[3:], 'correct': True, 'voted': True})
            elif option[0] == correctAnswer and option[0] != votedAnswer[0]:
                reformattedOptions.append({'text': option[3:], 'correct': True, 'voted': False})
            elif option[0] != correctAnswer and option[0] == votedAnswer[0]:
                reformattedOptions.append({'text': option[3:], 'correct': False, 'voted': True})
            elif option[0] != correctAnswer and option[0] != votedAnswer[0]:
                reformattedOptions.append({'text': option[3:], 'correct': False, 'voted': False})
        questionBlock['myOptionsAre'] = reformattedOptions

    questionBlock.pop('answerIs')
    questionBlock.pop('mostVotedIs')

    print(index)
    dataCollector.append(questionBlock)
    # break
with open(f"{certificationName}-questionData.json", "w") as updated_file: json.dump(dataCollector, updated_file, indent=4)