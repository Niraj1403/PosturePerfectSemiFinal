import React, { useEffect, useRef, useState } from 'react';
import * as tf from '@tensorflow/tfjs';
import * as tmPose from '@teachablemachine/pose';
import "../../components/SuryaNamaskar/SuryaNamaskar.css";

const SuryaNamaskar = () => {
  const canvasRef = useRef(null);
  const webcamRef = useRef(null);
  const modelRef = useRef(null);
  const maxPredictionsRef = useRef(0);
  const [isCameraStarted, setIsCameraStarted] = useState(false);
  const [currentPose, setCurrentPose] = useState(null); // State to track the current pose

  // List of Surya Namaskar poses
  const suryaNamaskarPoses = [
    "Ashtang Namaskarasana",
    "Ashwa Sanchalasanaa",
    "Bhujgasana",
    "Dandasana",
    "Hastatautasana",
    "Padhastana",
    "Parvatasnaa",
  ];

  useEffect(() => {
    if (!isCameraStarted) return; // Only initialize if the camera is started

    const URL = process.env.PUBLIC_URL + '/models/surya-namaskar/';
    const modelURL = URL + 'model.json';
    const metadataURL = URL + 'metadata.json';

    const init = async () => {
      try {
        // Load the model and metadata
        modelRef.current = await tmPose.load(modelURL, metadataURL);
        maxPredictionsRef.current = modelRef.current.getTotalClasses();

        // Set up the webcam
        const size = 600; // Canvas size
        const flip = true; // Whether to flip the webcam
        webcamRef.current = new tmPose.Webcam(size, size, flip);
        await webcamRef.current.setup();
        await webcamRef.current.play();

        // Append elements to the DOM
        canvasRef.current.width = size;
        canvasRef.current.height = size;

        // Start the prediction loop
        requestAnimationFrame(loop);
      } catch (error) {
        console.error('Error initializing Surya Namaskar model:', error);
      }
    };

    const loop = async (timestamp) => {
      webcamRef.current.update(); // Update the webcam frame
      await predict();
      requestAnimationFrame(loop);
    };

    const predict = async () => {
      const { pose, posenetOutput } = await modelRef.current.estimatePose(webcamRef.current.canvas);
      const prediction = await modelRef.current.predict(posenetOutput);

      // Find the pose with the highest confidence score
      let maxScore = 0;
      let detectedPose = null;
      for (let i = 0; i < maxPredictionsRef.current; i++) {
        if (prediction[i].probability > maxScore) {
          maxScore = prediction[i].probability;
          detectedPose = prediction[i].className;
        }
      }

      // Update the current pose
      if (detectedPose && maxScore > 0.5) { // Only update if confidence is above 50%
        setCurrentPose(detectedPose);
      }

      // Draw the pose
      drawPose(pose);
    };

    const drawPose = (pose) => {
      const ctx = canvasRef.current.getContext('2d');
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      ctx.drawImage(webcamRef.current.canvas, 0, 0);

      if (pose) {
        const minPartConfidence = 0.5;
        tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
        tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
      }
    };

    init();

    // Cleanup on component unmount
    return () => {
      if (webcamRef.current) {
        webcamRef.current.stop();
      }
    };
  }, [isCameraStarted]); // Re-run effect when isCameraStarted changes

  const handleStartCamera = () => {
    setIsCameraStarted(true); // Start the camera
  };

  return (
    <div className="surya-namaskar-container">
      <h1>Surya Namaskar Detection</h1>

      {/* Button to start the camera */}
      {!isCameraStarted && (
        <button className="start-button" onClick={handleStartCamera}>
          Start Camera
        </button>
      )}
    {/* Flexbox container for side-by-side layout */}
    {isCameraStarted && (
      <div className="content-container">
        {/* Canvas for camera feed */}
        <canvas ref={canvasRef} className="camera-canvas"></canvas>

        {/* List of Surya Namaskar Poses */}
        <div className="pose-list">
          <h2>Surya Namaskar Poses</h2>
          <ul>
            {suryaNamaskarPoses.map((pose) => (
              <li
                key={pose}
                className={currentPose === pose ? "active-pose" : ""} // Highlight the current pose
              >
                {pose}
                {currentPose === pose && <span className="checkmark">✔️</span>}
              </li>
            ))}
          </ul>
        </div>
      </div>
    )}
  </div>
  );
};

export default SuryaNamaskar;