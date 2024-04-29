# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
import subprocess
import sys

certificationName = "az-305"

def writeData(questionsInJSON):
    try: 
        with open("questions.json", "r") as old_file: iAmData = json.load(old_file)
    except FileNotFoundError: iAmData = {}
    iAmData.update(questionsInJSON)
    with open("questions.json", "w") as updated_file:
        json.dump(iAmData, updated_file, indent=4)

    print("Updated JSON data saved to", "questions.json")


siteUrl = f"https://www.examtopics.com/exams/microsoft/{certificationName}/view/"
chrome_driver_path = "C:/chromeDriver/chromeDriver/chromedriver.exe"

subprocess.Popen(['C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', '--remote-debugging-port=8989', '--user-data-dir=C:/Users/iandm/Desktop/AgniPariksha/chromeData'])
sleep(2)
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:8989")

options.add_argument("--start-maximized")
options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
options.add_argument("--disable-notifications")
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get(siteUrl)
sleep(1)
pageIndex = 1
questionsJSON = []

while driver.title != "404 - Page not found":
# for i in range(2):
    questionsContainer = driver.find_element(By.CLASS_NAME, "questions-container")
    questionCard = questionsContainer.find_elements(By.CLASS_NAME, "exam-question-card")
    print(len(questionCard))

    for questionNumber, cardData in enumerate(questionCard):
        linkIs = siteUrl
        myOptionsAre, mostVotedAre, isMCQ = [], [], False
        questionImages, descriptionImages = [], []
        
        questionNumber = cardData.find_element(By.CSS_SELECTOR, ".card-header.text-white.bg-primary").text.replace("\n"," -- ")
        questionBody = cardData.find_element(By.CSS_SELECTOR, ".card-body.question-body")
        questionCard = questionBody.find_elements(By.CLASS_NAME, "card-text")[0]
        questionIs = questionCard.text
        imageBlocks = questionCard.find_elements(By.TAG_NAME, "img")
        if imageBlocks:
            for image in imageBlocks:
                questionImages.append(image.get_attribute("src"))

        
        revealSolution = cardData.find_element(By.CLASS_NAME, "reveal-solution").click()
        # sleep(1)
        answersAre = cardData.find_elements(By.CSS_SELECTOR, ".multi-choice-item.correct-hidden.correct-choice")
        correctOptions = []
        for answer in answersAre:
            thisOption = answer.find_element(By.CLASS_NAME, 'multi-choice-letter').get_attribute('data-choice-letter')
            print(thisOption)
            correctOptions.append(thisOption)
        descriptionCard = cardData.find_element(By.CLASS_NAME, "answer-description")
        descriptionIs = descriptionCard.text
        imageBlocks = descriptionCard.find_elements(By.TAG_NAME, "img")
        if imageBlocks:
            for image in imageBlocks:
                descriptionImages.append(image.get_attribute("src"))


        try: # For MultiChoice Questions babyyyyyyyyyy
            optionsBlock = questionBody.find_element(By.CLASS_NAME, "question-choices-container")
            optionsAre = optionsBlock.find_elements(By.CLASS_NAME, "multi-choice-item")
            for option in optionsAre:
                myOptionsAre.append(option.text.strip())
                # Check if the option is Most Votedd
                try:
                    mostVoted = option.find_element(By.CSS_SELECTOR, "span.most-voted-answer-badge")
                    if mostVoted:
                        mostVotedAre.append(option.text[0])
                except: pass
            isMCQ = True

        except: pass #It has an Image

        # print("\n\n-----------QUESTION START HERE-----------")
        # print(questionNumber)
        # print("QuestionIs:", questionIs)
        # print("QuestionImages: ", questionImages)
        # if isMCQ: print("My Options Are: ", myOptionsAre)
        # else:
        #     answersAre = descriptionIs + ", ".join(descriptionImages) 
        #     print("-----------IMAGE QUESTION-----------")
        # print("answersAre: ", answersAre)
        # print(f"Most Voted Answer is {mostVotedAre}")
        # print("DescriptionIs: ", descriptionIs)
        # print("DescriptionImages: ", descriptionImages)
        # print("LinkIs: ", linkIs)
        # print("-----------QUESTION END HERE----------- \n\n")

        questionData = {
            "questionNumber": questionNumber,
            "questionIs": questionIs,
            "questionImages": questionImages,
            "isMCQ": isMCQ,
            "myOptionsAre": myOptionsAre if isMCQ else None,
            "answersAre": descriptionIs + ", ".join(descriptionImages) if not isMCQ else correctOptions,
            "mostVotedAre": mostVotedAre,
            "descriptionIs": descriptionIs,
            "descriptionImages": descriptionImages,
            "linkIs": linkIs
        }
        questionsJSON.append(questionData)
        # print(questionData)
        # break
    pageIndex+=1
    linkIs = siteUrl + str(pageIndex)
    driver.get(linkIs)

# jsonData = json.dumps(questionsJSON, indent=4)
fileName = f"{certificationName}-rawData.json"
with open(fileName, "w") as questionData:
    json.dump(questionsJSON, questionData, indent=4)
# print("JSON data saved to", fileName)
# driver.quit()