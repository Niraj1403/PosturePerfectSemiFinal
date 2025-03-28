import React, { useEffect, useRef } from "react";
import * as tf from "@tensorflow/tfjs";
import * as tmPose from "@teachablemachine/pose";
import "./SuryaNamaskar.css"; // ✅ CSS file in the same folder

const SuryaNamaskarComponent = () => {
  const canvasRef = useRef(null);
  const labelContainerRef = useRef(null);
  const webcamRef = useRef(null);
  const modelRef = useRef(null);
  const maxPredictionsRef = useRef(0);

  useEffect(() => {
    const URL = process.env.PUBLIC_URL + "/models/surya-namaskar/";
    const modelURL = URL + "model.json";
    const metadataURL = URL + "metadata.json";

    const init = async () => {
      try {
        // Load the model and metadata
        modelRef.current = await tmPose.load(modelURL, metadataURL);
        maxPredictionsRef.current = modelRef.current.getTotalClasses();

        // Set up the webcam
        const size = 400; // Adjust size as needed
        const flip = true; // Whether to flip the webcam
        webcamRef.current = new tmPose.Webcam(size, size, flip);
        await webcamRef.current.setup();
        await webcamRef.current.play();

        // Append elements to the DOM
        canvasRef.current.width = size;
        canvasRef.current.height = size;
        labelContainerRef.current.innerHTML = ""; // Clear previous labels
        for (let i = 0; i < maxPredictionsRef.current; i++) {
          labelContainerRef.current.appendChild(document.createElement("div"));
        }

        // Start the prediction loop
        requestAnimationFrame(loop);
      } catch (error) {
        console.error("Error initializing Surya Namaskar model:", error);
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

      // Display predictions
      for (let i = 0; i < maxPredictionsRef.current; i++) {
        const classPrediction =
          prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        labelContainerRef.current.childNodes[i].innerHTML = classPrediction;
      }

      // Draw the pose
      drawPose(pose);
    };

    const drawPose = (pose) => {
      const ctx = canvasRef.current.getContext("2d");
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
  }, []);

  return (
    <div className="surya-namaskar-container">
      <h1>Surya Namaskar Detection</h1>
      <canvas ref={canvasRef}></canvas>
      <div ref={labelContainerRef} id="label-container"></div>
    </div>
  );
};

export default SuryaNamaskarComponent;