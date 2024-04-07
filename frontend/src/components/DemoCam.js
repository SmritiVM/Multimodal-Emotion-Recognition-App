import React, { useState } from 'react';

function DemoCam() {
  const [emotions, setEmotions] = useState([]);
  const [imageFile, setImageFile] = useState(null);

  const handleImageUpload = (event) => {
    setImageFile(event.target.files[0]);
  };

  const handleDetectEmotions = async () => {
    if (!imageFile) {
      alert('Please upload an image.');
      return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);

    try {
      const response = await fetch('http://localhost:5000/detect_emotions', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Failed to detect emotions.');
      }

      const data = await response.json();
      setEmotions(data);
    } catch (error) {
      console.error('Error detecting emotions:', error.message);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      <button onClick={handleDetectEmotions}>Detect Emotions</button>
      <div>
        {emotions.map((emotion, index) => (
          <div key={index}>
            {emotion.label} - {emotion.position.toString()}
          </div>
        ))}
      </div>
    </div>
  );
}

export default DemoCam;
