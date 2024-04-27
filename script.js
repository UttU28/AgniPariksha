var questionsData;
let currentQuestionIndex = 0;
let userScore = 0;

const startButtonEl = document.querySelector(".start-btn");
const welcomeScreenEl = document.querySelector(".welcome-screen");
const quizScreenEl = document.querySelector(".quiz-screen");
const questionEl = document.querySelector(".question");
const answersButtons = document.querySelector(".answers-container");
const nextButtonEl = document.querySelector(".next-btn");
// const checkButtonEl = document.querySelector(".chk-asn");

startButtonEl.addEventListener("click", startQuiz);

function loadJSON() {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', 'az-400-questionData.json', true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            questionsData = JSON.parse(xobj.responseText);
            // Call the displayQuestion function after loading the JSON data
            displayQuestion(0); // Assuming currentQuestionIndex starts from 0
        }
    };
    xobj.send(null);
}

function startQuiz() {
    welcomeScreenEl.style.display = "none";
    // quizScreenEl.style.display = "block";
    quizScreenEl.style.display = "flex";
    currentQuestionIndex = 0;
    userScore = 0;
    nextButtonEl.innerHTML = "Next";
    nextButtonEl.style.display = "none";
    // startButtonEl.innerHTML = "Submit";
    // startButtonEl.style.display = "none";
    loadJSON();
    displayQuestion();
}


function displayQuestion() {
    resetContainer();
    questionEl.textContent = questionsData[currentQuestionIndex].questionIs;
    questionsData[currentQuestionIndex].myOptionsAre.forEach((answer) => {
        const buttonEl = document.createElement("button");
        buttonEl.innerHTML = answer.text;
        buttonEl.classList.add("ans-btn");
        answersButtons.appendChild(buttonEl);

        if (answer.correct) {
            buttonEl.dataset.correctAns = answer.correct;
        }

        // console.log(buttonEl);

        buttonEl.addEventListener("click", checkAnswer);
    });
}

function checkAnswer(e) {
    const selectedButton = e.target;
    if (selectedButton.dataset.correctAns) {
        userScore++;
        console.log(userScore);
        selectedButton.classList.add("correct-ans");
    } else {
        selectedButton.classList.add("wrong-ans");
    }

    Array.from(answersButtons.children).forEach((button) => {
        if (button.dataset.correctAns === "true") {
            button.classList.add("correct-ans");
        }
        button.disabled = "true";
    });

    nextButtonEl.style.display = "block";
}

function displayResult() {
    resetContainer();
    questionEl.innerHTML = `Quiz is Completed! <br> Your Score: <span class="score">${userScore}/${questionsData.length}</span>`;

    nextButtonEl.innerHTML = "Restart Quiz";
}

function nextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < questionsData.length) {
        displayQuestion();
        nextButtonEl.style.display = "none";
    } else {
        displayResult();
    }
}

nextButtonEl.addEventListener("click", function () {
    if (currentQuestionIndex < questionsData.length) {
        nextQuestion();
    } else {
        startQuiz();
    }
});

function resetContainer() {
    questionEl.textContent = "";
    answersButtons.innerHTML = "";
}