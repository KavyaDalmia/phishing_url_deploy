import { useState } from 'react';
import { FaHome, FaShieldAlt, FaEnvelope } from 'react-icons/fa';
import appLogo from './assets/Vector.svg';
import './App.css';

function App() {
  return (
    <div className='bg-gradient-custom w-full h-full flex flex-col'>
      {/* Navbar */}
      <nav className='navbar w-full py-4 px-6 text-white flex justify-between items-center'>
        <div className='text-2xl font-bold'>CyberSecurityApp</div>
        <div className='space-x-4'>
          <a href='#' className='hover:text-gray-300 flex items-center'>
            <FaHome className='mr-1' /> Home
          </a>
          <a href='#' className='hover:text-gray-300 flex items-center'>
            <FaShieldAlt className='mr-1' /> Features
          </a>
          <a href='#' className='hover:text-gray-300 flex items-center'>
            <FaEnvelope className='mr-1' /> Contact
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <main className='flex-grow flex items-center justify-center relative z-1'>
        <section className='w-full h-full py-28 px-6 flex flex-col items-center justify-center space-y-6 text-center'>
          <div className='w-full h-full flex flex-col justify-center items-center space-y-6'> 
            <img src={appLogo} className='w-[165px] h-[165px] shadow-lg' alt='App Logo' /> 
            <h1 className='text-4xl font-bold text-white'>Welcome to Our Cybersecurity App</h1>
            <p className='text-gray-200 max-w-md text-center'>This app helps you determine if a link is safe or not. It's designed to provide a quick overview of the safety status of your links.</p>
            <div className='space-x-4'>
              <button className='button px-4 py-2 text-white rounded'>Get Started</button>
              <button className='button px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 hover:border hover:border-gray-700'>Learn More</button>
            </div>
          </div>
        </section>
      </main>

      {/* Testimonials Section */}
      <section className='testimonial-section flex flex-col items-center justify-center'>
        <h2 className='text-3xl font-bold text-white mb-8'>What Our Users Say</h2>
        <div className='flex flex-wrap justify-center'>
          <div className='testimonial'>
            <p>"This app has saved me so many times! Highly recommend it for anyone who wants to stay safe online."</p>
            <p>- User A</p>
          </div>
          <div className='testimonial'>
            <p>"A must-have tool for checking links. It's fast and reliable."</p>
            <p>- User B</p>
          </div>
          <div className='testimonial'>
            <p>"Great app for cybersecurity. Easy to use and very effective."</p>
            <p>- User C</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className='w-full py-4 px-6 bg-gray-800 text-white flex justify-center'>
        <p>&copy; 2024 CyberSecurityApp. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
