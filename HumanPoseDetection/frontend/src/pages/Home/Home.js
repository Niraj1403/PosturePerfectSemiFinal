import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";
import yogaImage from "../../assets/gtea-tea.gif";

const Home = () => {
  return (
    <div className="home-container">
      <div className="main-content">
        <div className="illustration-container">
          <div className="illustration-wrapper">
            <img
              src={yogaImage}
              alt="Yoga pose illustration"
              className="illustration-image"
            />
          </div>
        </div>

        <div className="content-container">
          <div className="explore-link">
            Explore different poses.{" "}
            <Link to="/start" className="poses-link">
              Yoga Poses
              <span className="arrow">→</span>
            </Link>
          </div>

          <h1 className="main-heading">
            Perfect Your Yoga Poses with AI-Powered Posture Detection
          </h1>

          <p className="description">
            Get instant feedback on your yoga posture and improve alignment.
            With real-time feedback, you'll receive immediate insights on your
            posture during practice. Our AI-powered posture analysis utilizes
            advanced technology to analyze and enhance your alignment, making it
            suitable for all levels of experience - from beginners to advanced
            practitioners.
          </p>

          <div className="cta-container">
            <Link to="/signup" className="signup-button">
              Sign Up
            </Link>
            <a href="#" className="how-it-works">
              How it Works →
            </a>
          </div>
        </div>
      </div>

      <div className="background-gradient"></div>
    </div>
  );
};

export default Home;
