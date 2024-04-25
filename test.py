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
questionsBlocks = questionsContainer.find_elements(By.CLASS_NAME, "exam-question-card")

print(len(questionsBlocks))
for questionBlock in questionsBlocks:
    questionNumber = questionBlock.find_element(By.CSS_SELECTOR, ".card-header.text-white.bg-primary").text
    questionIs = questionBlock.find_elements(By.CLASS_NAME, "card-text")[0].text
    answerIs = questionBlock.find_element(By.CLASS_NAME, "correct-answer").text
    descriptionIs = questionBlock.find_element(By.CLASS_NAME, "answer-description").text
    linkIs = siteUrl

    try:
        votedAnswers = questionBlock.find_element(By.CLASS_NAME, "voted-answers-tally")
        optionsBlock = votedAnswers.find_elements(By.CSS_SELECTOR, "question-choices-container")
        scriptBlock = questionBlock.find_element(By.CLASS_NAME, "question-choices-container")
        optionsBlock = questionBlock.find_element(By.CLASS_NAME, "question-choices-container")
        
    except:
        # It has an image
        pass

    print(questionText)



# # html_content = questionsContainer.get_attribute('innerHTML')
html_content = driver.page_source
driver.quit()
# print(html_content)
