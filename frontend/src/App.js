import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import EmotionRecognition from "./components/EmotionRecognition";
// import DemoCam from "./components/DemoCam";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path = "/fer" element = {<EmotionRecognition/>}/>
        </Routes>
      </Router>
      
      {/* <DemoCam/> */}
    </div>
  );
}

export default App;
