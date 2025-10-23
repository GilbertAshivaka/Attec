import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { MapPin, Target, Users, Cpu } from 'lucide-react';
import './About.css';

const About = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const values = [
    {
      icon: <Cpu />,
      title: 'Technical Excellence',
      description: 'We understand AI from the ground up—ML pipelines, LLMs, computer vision, and production deployment.',
    },
    {
      icon: <Users />,
      title: 'Builder Mentality',
      description: 'We don\'t just advise—we build. Every solution is crafted with precision and tested in real-world conditions.',
    },
    {
      icon: <Target />,
      title: 'Results-Driven',
      description: 'Every project is measured by tangible business outcomes, not just technical achievements.',
    },
  ];

  return (
    <section id="about" className="about" ref={ref}>
      <div className="about-container">
        <motion.div
          className="about-header"
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
        >
          <h2 className="about-title">About ATTEC</h2>
          <p className="about-acronym">
            <strong>A</strong>dvancing <strong>T</strong>echnology for <strong>T</strong>omorrow's{' '}
            <strong>E</strong>ngineering and <strong>C</strong>omputing
          </p>
        </motion.div>

        <div className="about-content">
          <motion.div
            className="about-mission"
            initial={{ opacity: 0, x: -30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="about-logo-section">
              <img src="/logo.jpg" alt="ATTEC Logo" className="about-logo" />
              <div className="about-logo-text">
                <p className="about-location">
                  <MapPin size={20} />
                  Based in Kenya, Serving the World
                </p>
              </div>
            </div>

            <h3>Our Mission</h3>
            <p>
              Transform businesses through intelligent AI integration, building tomorrow's
              technology today. We bridge the gap between cutting-edge AI capabilities and
              practical business applications.
            </p>

            <h3>Why ATTEC?</h3>
            <p>
              We're not another consultancy repackaging ChatGPT tutorials. Our team of
              passionate AI engineers and strategists genuinely loves this work and stays
              current with the latest developments in artificial intelligence and technology.
            </p>

            <p>
              Based in Kenya with a deep understanding of local business contexts, we deliver
              world-class AI expertise that competes globally while remaining accessible and
              practical for businesses at every stage.
            </p>
          </motion.div>

          <div className="about-values">
            {values.map((value, index) => (
              <motion.div
                key={index}
                className="about-value-card"
                initial={{ opacity: 0, y: 30 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
              >
                <div className="about-value-icon">{value.icon}</div>
                <h4>{value.title}</h4>
                <p>{value.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
