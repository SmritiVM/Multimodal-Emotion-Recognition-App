import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');

    const sendMessage = async () => {
        try {
            const res = await axios.post('http://localhost:5001/chatbot', { message });
            setResponse(res.data.response);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Enter your message..."
            />
            <button onClick={sendMessage}>Send</button>
            {response && <p>Chatbot: {response}</p>}
        </div>
    );
};

export default Chatbot;
