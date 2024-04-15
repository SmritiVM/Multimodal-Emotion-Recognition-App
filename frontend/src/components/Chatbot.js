import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './Chatbot.css'; // Import CSS file

const Chatbot = () => {
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const chatContainerRef = useRef(null);

    useEffect(() => {
        // Scroll to bottom when new message is added
        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }, [chatHistory]);

    const sendMessage = async () => {
        try {
            const userMessage = { text: message, isUser: true };
            setChatHistory(prevHistory => [...prevHistory, userMessage]);
            const res = await axios.post('http://localhost:5001/chatbot', { message });
            const botMessage = { text: res.data.response, isUser: false };
            setChatHistory(prevHistory => [...prevHistory, botMessage]);
            setMessage(''); // Clear input after sending message
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-messages" ref={chatContainerRef}>
                {chatHistory.map((msg, index) => (
                    <div
                        key={index}
                        className={`chat-message ${msg.isUser ? 'user-message' : 'bot-message'}`}
                    >
                        {msg.text}
                    </div>
                ))}
            </div>
            <div className="chat-input">
                <input
                    type="text"
                    className="message-input"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Enter your message..."
                />
                <button className="send-button" onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
};

export default Chatbot;
