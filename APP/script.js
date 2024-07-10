function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    document.getElementById('user-input').value = '';

    $.ajax({
        url: '/chat',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'user_input': userInput }),
        success: function(response) {
            var chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += '<p><strong>You:</strong> ' + userInput + '</p>';
            chatBox.innerHTML += '<p><strong>Bot:</strong> ' + response.response + '</p>';
            chatBox.scrollTop = chatBox.scrollHeight;
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}
