import { useState, useEffect } from 'react';
import Hero from './components/Hero';
import Story from './components/Story';
import Services from './components/Services';
import Process from './components/Process';
import About from './components/About';
import Contact from './components/Contact';
import Navigation from './components/Navigation';
import './App.css';

function App() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="app">
      <Navigation scrolled={scrolled} />
      <Hero />
      <Story />
      <Services />
      <Process />
      <About />
      <Contact />
    </div>
  );
}

export default App;
