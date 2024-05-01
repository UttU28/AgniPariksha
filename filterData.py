import json

certificationName = "az-305"

iAmData = None
with open(f"{certificationName}-rawData.json", "r") as oldFile: iAmData = json.load(oldFile)

dataCollector = []
# for questionBlock in iAmData[:2]:
for index, questionBlock in enumerate(iAmData):
    sampleData = questionBlock['questionNumber'].split('--')
    questionBlock['questionNumber'] = sampleData[0].replace('Question #','').strip()
    topicNumber = sampleData[-1].replace('Topic ', '').strip()

    if int(topicNumber) < 10:
        topicNumber = f"0{topicNumber}"
    questionBlock['topicNumber'] = topicNumber

    reformattedOptions = []
    correctAnswer = questionBlock['answersAre']
    votedAnswers = questionBlock['mostVotedAre']
    print("correctAnswer", correctAnswer, len(correctAnswer))
    # questionBlock['multipleAnswers'] = len(correctAnswer) >= 2 if '1' else 0
    questionBlock['multipleAnswers'] = False

    if questionBlock['isMCQ']:
        if len(correctAnswer) >= 2 : questionBlock['multipleAnswers'] = True
        for option in questionBlock['myOptionsAre']:
            # print(votedAnswers, questionBlock['questionNumber'])
            if votedAnswers == None or votedAnswers == []:
                # print("sdv")
                if option[0] in correctAnswer and votedAnswers == None:
                    reformattedOptions.append({'text': option[3:].replace(' Most Voted',''), 'correct': True, 'voted': True})
                elif option[0] not in correctAnswer and votedAnswers == None:
                    reformattedOptions.append({'text': option[3:].replace(' Most Voted',''), 'correct': False, 'voted': False})
            elif option[0] in correctAnswer and option[0] in votedAnswers:
                reformattedOptions.append({'text': option[3:].replace(' Most Voted',''), 'correct': True, 'voted': True})
            elif option[0] in correctAnswer and option[0] not in votedAnswers:
                reformattedOptions.append({'text': option[3:].replace(' Most Voted',''), 'correct': True, 'voted': False})
            elif option[0] not in correctAnswer and option[0] in votedAnswers:
                reformattedOptions.append({'text': option[3:].replace(' Most Voted',''), 'correct': False, 'voted': True})
            elif option[0] not in correctAnswer and option[0] not in votedAnswers:
                reformattedOptions.append({'text': option[3:].replace(' Most Voted',''), 'correct': False, 'voted': False})
        questionBlock['myOptionsAre'] = reformattedOptions

    questionBlock.pop('answersAre')
    questionBlock.pop('mostVotedAre')

    print(index)
    dataCollector.append(questionBlock)
    # break
with open(f"{certificationName}-questionData.json", "w") as updated_file: json.dump(dataCollector, updated_file, indent=4)