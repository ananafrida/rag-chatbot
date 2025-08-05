// script.js


const systemContext = `
MIT App Inventor Control Blocks
if & else if
for each number from to
for each item in list
for each key with value in dictionary
while
if then else
do with result
evaluate but ignore result
open another screen
open another screen with start value
get plain start text
get start value
close screen
close screen with plain text
close screen with value
close application
break
if & else if
Tests a given condition. If the condition is true, performs the actions in a given sequence of blocks; otherwise, the blocks are ignored.

Tests a given condition. If the condition is true, performs the actions in the -then sequence of blocks; otherwise, performs the actions in the -else equence of blocks.

Tests a given condition. If the result is true, performs the actions in the -then sequence of blocks; otherwise tests the statement in the -else if section. If the result is true, performs the actions in the -then sequence of blocks; otherwise, performs the actions in the -else sequence of blocks.

The animation below shows how to use the if else mutator block.



for each number from to


Runs the blocks in the do section for each numeric value in the range starting from from and ending at to, incrementing number by the value of by each time. Use the given variable name, number, to refer to the current value. You can change the name number to something else if you wish.

for each item in list


Runs the blocks in the do section for each item in the list. Use the given variable name, item, to refer to the current list item. You can change the name item to something else if you wish.

for each key with value in dictionary


Runs the blocks in the do section for each key-value entry in the dictionary. Use the given variables, key and value, to refer to the key and value of the current dictionary entry. You can change the names key and value to something else if you wish.

while


Tests the -test condition. If true, performs the action given in -do , then tests again. When test is false, the block ends and the action given in -do is no longer performed.

if then else
Tests a given condition. If the statement is true, performs the actions in the then-return sequence of blocks and returns the then-return value; otherwise, performs the actions in the else-return sequence of blocks and returns the else-return value. This block is similar to the ternary operator (?:) found in some languages.

do with result


Sometimes in a procedure or another block of code, you may need to do something and return something, but for various reasons you may choose to use this block instead of creating a new procedure.

evaluate but ignore result


Provides a “dummy socket” for fitting a block that has a plug on its left into a place where there is no socket, such as one of the sequence of blocks in the do part of a procedure or an if block. The block you fit in will be run, but its returned result will be ignored. This can be useful if you define a procedure that returns a result, but want to call it in a context that does not accept a result.

open another screen


Opens the screen with the provided name.

The screenName must be one of the Screens created using the Designer. The screenName should be selected from the connected screen name dropdown block.

If you do open another screen, you should close it when returning to your main screen to free system memory. Failure to close a screen upon leaving it will eventually lead to memory problems.

App developers should never close Screen1 or use this block to return to Screen1. Use the close screen block instead.

open another screen with start value


Opens another screen and passes a value to it.

get plain start text


Returns the plain text that was passed to this screen when it was started by another app. If no value was passed, it returns the empty text. For multiple screen apps, use get start value rather than get plain start text.

get start value


Returns the start value given to the current screen.

This value is given from using open another screen with start value or close screen with value.

close screen


Closes the current screen.

close screen with plain text


Closes the current screen and passes text to the app that opened this one. This command is for returning text to non-App Inventor activities, not to App Inventor screens. For App Inventor Screens, as in multiple screen apps, use close screen with value, not close screen with plain text.

close screen with value


Closes the current screen and returns a value to the screen that opened this one.

close application


Closes the application.

break



All the following blocks are text blocks:
string
join
length
is empty
compare texts
trim
upcase
downcase
starts at
contains
contains any
contains all
split at first
split at first of any
split
split at any
split at spaces
segment
replace all
obfuscated text
is a string?
reverse
replace all mappings
Also, the color of any text block or any blocks under the "text" drawer is Magenta.


About "Set to" blocks:
"Set to" is not located under built-in block. It is a command block in dark green color. It can be found under any component (e.g. screen, Label) you included in your app. You can click on whichever component you want to command.


When looping using the for range, for each, or while blocks it is sometimes useful to be able to exit the loop early. The break allows you to escape the loop. When executed, this will exit the loop and continue the app with the statements that occur after the loop in the blocks.
Do not proactively mention this information. Only refer to it if the user's query relates to App Inventor and close screen or close screen blocks.
`;

const chatInput =
    document.querySelector('.chat-input textarea');
const sendChatBtn =
    document.querySelector('.chat-input button');
const chatbox = document.querySelector(".chatbox");

let userMessage;
const API_KEY = "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";

//OpenAI Free APIKey

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent =
        className === "chat-outgoing" ? `<p>${message}</p>` : `<p>${message}</p>`;
    chatLi.innerHTML = chatContent;
    return chatLi;
}

const generateResponse = (incomingChatLi) => {
    const API_URL = "https://api.openai.com/v1/chat/completions";
    const messageElement = incomingChatLi
    .querySelector("p");
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${API_KEY}`
        },
        body: JSON.stringify({
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    role: "system",
                    content: systemContext
                },
                {
                    role: "user",
                    content: userMessage
                }
            ]
        })
    };

    fetch(API_URL, requestOptions)
        .then(res => {
            if (!res.ok) {
                throw new Error("Network response was not ok");
            }
            return res.json();
        })
        .then(data => {
            messageElement
            .textContent = data.choices[0].message.content;
        })
        .catch((error) => {
            messageElement
            .classList.add("error");
            messageElement
            .textContent = "Oops! Something went wrong. Please try again!";
        })
        .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
};


const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) {
        return;
    }
    chatbox
    .appendChild(createChatLi(userMessage, "chat-outgoing"));
    chatbox
    .scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        const incomingChatLi = createChatLi("Thinking...", "chat-incoming")
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

// this is where everything start after the user hits the chat button
sendChatBtn.addEventListener("click", handleChat);

function cancel() {
    let chatbotcomplete = document.querySelector(".chatBot");
    if (chatbotcomplete.style.display != 'none') {
        chatbotcomplete.style.display = "none";
        let lastMsg = document.createElement("p");
        lastMsg.textContent = 'Thanks for using our Chatbot!';
        lastMsg.classList.add('lastMessage');
        document.body.appendChild(lastMsg)
    }
}
