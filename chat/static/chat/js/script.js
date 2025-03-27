document.addEventListener("DOMContentLoaded", function () {
    let socket = null;
    let currentRoomId = null;

    function connectWebSocket(roomId) {
        if (socket) {
            socket.close(); // Close previous socket if switching rooms
        }

        socket = new WebSocket(`ws://${window.location.host}/ws/group/${roomId}/`);

        socket.onmessage = function (event) {
            let data = JSON.parse(event.data);
            let messagesDiv = document.getElementById("messages");
            let newMessage = `<p><strong>${data.sender}:</strong> ${data.message}</p>`;
            messagesDiv.innerHTML += newMessage;
        };

        socket.onclose = function () {
            console.log("WebSocket Disconnected");
        };

        currentRoomId = roomId;
    }

    // Room Selection
    document.getElementById("rooms").addEventListener("click", function (event) {
        if (event.target.tagName === "LI") {
            let roomId = event.target.dataset.roomId;
            document.getElementById("chat-room-title").textContent = event.target.textContent;
            document.getElementById("input").classList.remove("hidden");

            // Load messages dynamically
            document.getElementById("messages").setAttribute("hx-get", `/chat/load_messages/${roomId}/`);
            document.getElementById("messages").dispatchEvent(new Event("roomChanged"));

            connectWebSocket(roomId);
        }
    });

    // Sending messages
    document.getElementById("sendButton").addEventListener("click", function () {
        let messageInput = document.getElementById("messageInput");
        let message = messageInput.value;

        if (socket && message.trim() !== "") {
            socket.send(JSON.stringify({ sender: 1, message: message })); // Change sender dynamically
            messageInput.value = "";
        }
    });
});
