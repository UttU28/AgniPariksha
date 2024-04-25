# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep


siteUrl = "https://www.examtopics.com/exams/microsoft/az-400/view/"
chrome_driver_path = "C:/chromeDriver/chromedriver.exe"
options = Options()
options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
driver = webdriver.Chrome(options=options)
driver.get(siteUrl)  # Replace "https://example.com" with the URL of the website you want to fetch HTML from

sleep(2)
questionsContainer = driver.find_element(By.CLASS_NAME, "questions-container")
questionCard = questionsContainer.find_elements(By.CLASS_NAME, "exam-question-card")

print(len(questionCard))
for cardData in questionCard:
    questionNumber = cardData.find_element(By.CSS_SELECTOR, ".card-header.text-white.bg-primary").text

    questionBody = cardData.find_element(By.CSS_SELECTOR, ".card-body.question-body")
    questionIs = questionBody.find_elements(By.CLASS_NAME, "card-text")[0].text
    
    answerIs = cardData.find_element(By.CLASS_NAME, "correct-answer").text
    descriptionIs = cardData.find_element(By.CLASS_NAME, "answer-description").text

    linkIs = siteUrl
    mostVotedIs, correctAnswerIs = None, None

    try:
        # For MultiChoice Questions babyyyyyyyyyy
        optionsBlock = questionBody.find_element(By.CLASS_NAME, "question-choices-container")
        optionsAre = optionsBlock.find_elements(By.CLASS_NAME, "multi-choice-item")
        for option in optionsAre:
            print(option.text)
            # Check if the option is Most Votedd
            try:
                mostVoted = option.find_element(By.CSS_SELECTOR, "span.most-voted-answer-badge")
                if mostVoted:
                    mostVotedIs = option.text
            except: pass
        print(f"Most Voted Answer is {mostVotedIs}")
        print(f"Correct Answer is {correctAnswerIs}")
        print(questionNumber)
        print("QuestionIs:", questionIs)
        print("AnswerIs: ", answerIs)
        print("DescriptionIs: ", descriptionIs)
        print("LinkIs: ", linkIs)

        print()
        print()
        print()
        
    except:
        # It has an image
        pass

    break

# html_content = driver.page_source
driver.quit()
# print(html_content)
