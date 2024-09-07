// set realtime chat and auto downline
let url = `ws://${window.location.host}/ws/socket-server/`

const chatSocket = new WebSocket(url)

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    console.log("Data: ", data) 

    if (data.type === "chat") {
        let messages = document.getElementById("chatbox");
    
        messages.insertAdjacentHTML("beforeEnd",
            `<div class="mb-2 text-right">
                <p class="bg-blue-500 text-white rounded-lg py-2 px-4 inline-block">${data.message}</p>
            </div>`);
            
        messages.scrollTop = messages.scrollHeight;
        if (messages.children.length > 0) {
            // Fetch the streaming response from the Django server
            fetch('/stream_response/?prompt=' + encodeURIComponent(data.message))
                .then(response => {
                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();
                    
                    function typeEffect(element, text) {
                        let index = 0;
                        const speed = 50; // Speed of typing effect in milliseconds
    
                        function type() {
                            if (index < text.length) {
                                element.textContent += text.charAt(index);
                                index++;
                                
                                // Scroll to the bottom after each character is added
                                messages.scrollTop = messages.scrollHeight;
                                
                                setTimeout(type, speed);
                            }
                        }
                        type();
                    }
    
                    function readStream() {
                        reader.read().then(({ done, value }) => {
                            if (done) {
                                console.log("Stream finished.");
                                return;
                            }
    
                            // Decode and process the chunk
                            const chunk = decoder.decode(value, { stream: true });
    
                            // Create a new element for the chunk
                            const p = document.createElement("p");
                            p.className = "bg-gray-200 text-gray-700 rounded-lg py-2 px-4 inline-block";
                            messages.appendChild(p);
    
                            // Apply typing effect
                            typeEffect(p, chunk);
    
                            // Continue reading the stream
                            readStream();
                        }).catch(error => {
                            console.error('Stream reading error:', error);
                        });
                    }
                    // Start reading the stream
                    readStream();
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                });
        }
    }
}

let form = document.getElementById("form")
if (form) {
    form.addEventListener("submit", function(e) {
        e.preventDefault();
        let message = e.target.prompt.value;
        let temp = document.getElementById("temperature").value;
        let top_k = document.getElementById("top_k").value;
        let top_p = document.getElementById("top_p").value;
        let max = document.getElementById("max_output_tokens").value;
        chatSocket.send(JSON.stringify({
            'prompt': message,
            'top_p':top_p,
            'top_k':top_k,
            'temperature':temp,
            'max_output_tokens':max,
        }));
        // let config = document.getElementById("config");

        // if (config) {
        //     // Fetch values directly from the form inputs by using their 'name' attributes
            // let temp = document.getElementById("temperature").value;
            // let top_k = document.getElementById("top_k").value;
            // let top_p = document.getElementById("top_p").value;
            // let max = document.getElementById("max_output_tokens").value;

        //     console.log(temp, top_k, top_p, max);
        // } else {
        //     console.log("no config");
        // }
        form.reset();
    });
} else {
    console.log("id 'form' not found in the DOM.");
}



// let socket = new WebSocket('ws://' + window.location.host + '/ws/conversations/');

// socket.onmessage = function(e) {
//     let data = JSON.parse(e.data);
//     let conversationList = document.getElementById('chat_history');
//     let newElement = document.createElement('div');
//     newElement.innerText = data.response;
//     conversationList.appendChild(newElement);
// };

// // Optional: Send a message to the server (if needed)
// function sendMessage(message) {
//     socket.send(JSON.stringify({
//         'message': message
//     }));
// }

