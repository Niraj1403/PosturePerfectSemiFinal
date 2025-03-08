import React from 'react';

const YogaLandingPage = () => {
  return (
    <div className="w-full h-screen bg-gradient-to-br from-[#87CEEB] to-[#A0DED0] flex items-center justify-center">
      <div className="max-w-4xl mx-auto px-8 py-10 bg-white rounded-xl shadow-lg">
        <div className="grid grid-cols-2 gap-8">
          <div>
            <h1 className="text-4xl font-bold mb-4">Yoga Pose Categorization</h1>
            <p className="text-lg mb-6">Explore the comprehensive categorization of yoga poses based on physical condition, mental health, body position, and movement type.</p>
            <div className="flex flex-col space-y-4">
              <a href="#physical" className="flex items-center space-x-2 text-[#A0DED0] hover:underline">
                <span>By Physical Condition</span>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </a>
              <a href="#mental" className="flex items-center space-x-2 text-[#A0DED0] hover:underline">
                <span>By Mental Health Condition</span>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </a>
              <a href="#position" className="flex items-center space-x-2 text-[#A0DED0] hover:underline">
                <span>By Body Position</span>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </a>
              <a href="#movement" className="flex items-center space-x-2 text-[#A0DED0] hover:underline">
                <span>By Movement Type</span>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
          </div>
          <div className="flex justify-center items-center">
            <img src="/api/placeholder/400/400" alt="Yoga Pose" className="w-full max-w-xs" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default YogaLandingPage;