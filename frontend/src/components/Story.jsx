import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { Zap, Target, TrendingUp, Shield } from 'lucide-react';
import './Story.css';

const Story = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const highlights = [
    {
      icon: <Zap />,
      title: 'The AI Revolution Is Here',
      description: 'Every day, businesses lose ground to AI-enabled competitors.',
    },
    {
      icon: <Target />,
      title: 'Bridge the Gap',
      description: 'From AI potential to business reality with the right partner.',
    },
    {
      icon: <TrendingUp />,
      title: 'Strategy to Execution',
      description: 'We don\'t just tell you what to do—we build it with you.',
    },
    {
      icon: <Shield />,
      title: 'Built on Fundamentals',
      description: 'ML pipelines, LLMs, computer vision, production deployment.',
    },
  ];

  return (
    <section id="story" className="story" ref={ref}>
      <div className="story-container">
        <motion.div
          className="story-header"
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
        >
          <h2 className="story-title">Not Another AI Consultancy</h2>
          <p className="story-subtitle">
            We're engineers, builders, and strategists who understand AI from first principles.
            <br />
            No buzzwords. No PowerPoints. Just results.
          </p>
        </motion.div>

        <div className="story-content">
          <motion.div
            className="story-main"
            initial={{ opacity: 0, x: -30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h3>The Problem</h3>
            <p>
              Most businesses know AI is important but don't know how to start. 
              They're overwhelmed by new tools launching constantly and skeptical 
              of consultancies making empty promises.
            </p>

            <h3>Our Approach</h3>
            <p>
              ATTEC bridges the gap between AI potential and business reality. 
              We're not here to peddle buzzwords—we're here to build. Our team 
              understands technology fundamentally: machine learning pipelines, 
              large language models, computer vision, and production deployment.
            </p>

            <h3>What Makes Us Different</h3>
            <p>
              We meet you where you are and take you where you need to be. Whether 
              you're just starting your AI journey or ready for custom solutions, 
              we combine technical depth with strategic thinking to deliver real, 
              measurable business value.
            </p>
          </motion.div>

          <div className="story-highlights">
            {highlights.map((item, index) => (
              <motion.div
                key={index}
                className="story-highlight-card"
                initial={{ opacity: 0, y: 30 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
              >
                <div className="story-highlight-icon">{item.icon}</div>
                <h4>{item.title}</h4>
                <p>{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Story;
