import EmotionRecognition from "./EmotionRecognition";
import Chatbot from "./Chatbot";

import "./style.css";
function Home(){
    return(
        <div className="container">
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