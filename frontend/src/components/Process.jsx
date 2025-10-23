import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { Search, Lightbulb, Wrench, Package } from 'lucide-react';
import './Process.css';

const Process = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const steps = [
    {
      icon: <Search />,
      title: 'Discovery',
      description: 'Deep dive into your business challenges and opportunities. We listen, analyze, and understand what success looks like for you.',
    },
    {
      icon: <Lightbulb />,
      title: 'Strategy',
      description: 'Collaborative roadmap aligned with your goals and resources. Clear milestones, realistic timelines, measurable outcomes.',
    },
    {
      icon: <Wrench />,
      title: 'Build',
      description: 'Implementation with precision and constant communication. We build, test, and refine until it\'s exactly right.',
    },
    {
      icon: <Package />,
      title: 'Deliver',
      description: 'Deployment, training, and long-term success setup. Your team is empowered, and the solution is production-ready.',
    },
  ];

  return (
    <section id="process" className="process" ref={ref}>
      <div className="process-container">
        <motion.div
          className="process-header"
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
        >
          <h2 className="process-title">How We Work</h2>
          <p className="process-subtitle">
            A proven process built on transparency, collaboration, and results.
          </p>
        </motion.div>

        <div className="process-timeline">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              className="process-step"
              initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
              animate={inView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.6, delay: index * 0.2 }}
            >
              <div className="process-step-number">{index + 1}</div>
              <div className="process-step-content">
                <div className="process-step-icon">{step.icon}</div>
                <h3 className="process-step-title">{step.title}</h3>
                <p className="process-step-description">{step.description}</p>
              </div>
              {index < steps.length - 1 && <div className="process-connector"></div>}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Process;
