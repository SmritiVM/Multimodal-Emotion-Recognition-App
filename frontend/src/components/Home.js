import EmotionRecognition from "./EmotionRecognition";
import Chatbot from "./Chatbot";

import Background from "../assets/Background.jpg";

import "./style.css";
function Home(){
    return(
        <div className="container" style = {{"backgroundImage": `url(${Background})`}}>
            <div className="web-camera">
                <EmotionRecognition/>
            </div>
            <div className="chatbot">
                <Chatbot/>
            </div>
        </div>
    )
}
export default Home;