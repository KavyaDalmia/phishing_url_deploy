import { useState } from 'react';
import appLogo from './assets/Vector.svg';
import './App.css';

function App() {
  return (
    <div className='bg-gradient-custom w-full h-full flex flex-col'>
      {/* Navbar */}
      <nav className='navbar w-full py-4 px-6 text-white flex justify-between items-center'>
        <div className='text-2xl font-bold'>CyberSecurityApp</div>
        <div className='space-x-4'>
          <a href='#' className='hover:text-gray-300'>Home</a>
          <a href='#' className='hover:text-gray-300'>Features</a>
          <a href='#' className='hover:text-gray-300'>Contact</a>
        </div>
      </nav>

      {/* Hero Section */}
      <main className='flex-grow flex items-center justify-center'>
        <section className='w-full h-full py-28 px-6 flex flex-col items-center justify-center space-y-6 text-center'>
          <div className='w-full h-full flex flex-col justify-center items-center space-y-6'> 
            <img src={appLogo} className='w-[165px] h-[165px] shadow-lg' alt='App Logo' /> 
            <h1 className='text-4xl font-bold text-white'>Welcome to Our Cybersecurity App</h1>
            <p className='text-gray-200 max-w-md text-center'>This app helps you determine if a link is safe or not. It's designed to provide a quick overview of the safety status of your links.</p>
            <div className='space-x-4'>
              <button className='button px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 hover:border hover:border-green-700'>Get Started</button>
              <button className='button px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 hover:border hover:border-gray-700'>Learn More</button>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className='w-full py-4 px-6 bg-gray-800 text-white flex justify-center'>
        <p>&copy; 2024 CyberSecurityApp. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
