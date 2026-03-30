const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Add message to UI
function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "user-msg" : "bot-msg";
    msg.innerText = text;
    chatBox.appendChild(msg);

    // auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message to backend
async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    // loading message
    const loading = document.createElement("div");
    loading.className = "bot-msg";
    loading.innerText = "Thinking...";
    chatBox.appendChild(loading);

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        loading.remove();
        addMessage(data.reply, "bot");

    } catch (error) {
        loading.innerText = "Error connecting to server.";
        console.error(error);
    }
}

// Button click
sendBtn.addEventListener("click", sendMessage);

// Enter key support
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});
