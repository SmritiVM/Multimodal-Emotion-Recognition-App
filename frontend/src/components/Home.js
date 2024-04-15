import { useState, useEffect } from "react";

import EmotionRecognition from "./EmotionRecognition";
import Chatbot from "./Chatbot";

import Background from "../assets/Background.jpg";

import "./style.css";
function Home(){
    const [enableVideo, setEnableVideo] = useState(false);

    const handleVideo = () => {
        setEnableVideo(true);
    }

    return(
        <div className="container" style = {{"backgroundImage": `url(${Background})`}}>
            {enableVideo && (
            <div className="web-camera">
                <EmotionRecognition/>
            </div>
            )}
            {!enableVideo && (
                <div className="no-video">
                    <button onClick={handleVideo}>Enable Video</button>
                </div>

            )}
            <div className="chatbot">
                <Chatbot/>
            </div>
        </div>
    )
}
export default Home;