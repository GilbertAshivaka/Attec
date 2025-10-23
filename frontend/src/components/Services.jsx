import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { Sparkles, Workflow, Rocket, CheckCircle, Clock, DollarSign } from 'lucide-react';
import './Services.css';

const Services = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const services = [
    {
      icon: <Sparkles />,
      title: 'AI Foundations',
      duration: '1-2 weeks',
      price: 'Starting at $2,500',
      description: 'Perfect for companies just beginning their AI journey.',
      features: [
        'Comprehensive AI readiness assessment',
        'Customized tool recommendations',
        'Hands-on team training',
        'Actionable implementation roadmap',
        '30-day action plan',
      ],
      popular: false,
    },
    {
      icon: <Workflow />,
      title: 'AI Integration',
      duration: '4-6 weeks',
      price: 'Starting at $8,000',
      description: 'Embed AI into your operations with custom workflows.',
      features: [
        'Custom workflow automation design',
        'AI tool integration with existing systems',
        'Process optimization and redesign',
        'API integrations where needed',
        '30 days post-launch support',
      ],
      popular: true,
    },
    {
      icon: <Rocket />,
      title: 'Custom AI Development',
      duration: '8-12+ weeks',
      price: 'Custom pricing',
      description: 'Bespoke AI solutions for unique business challenges.',
      features: [
        'Bespoke AI application development',
        'Custom model training or fine-tuning',
        'Full-stack integration',
        'Production deployment and scaling',
        'Extended support and maintenance',
      ],
      popular: false,
    },
  ];

  return (
    <section id="services" className="services" ref={ref}>
      <div className="services-container">
        <motion.div
          className="services-header"
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
        >
          <h2 className="services-title">Our Services</h2>
          <p className="services-subtitle">
            From AI fundamentals to custom development, we offer solutions at every stage of your journey.
          </p>
        </motion.div>

        <div className="services-grid">
          {services.map((service, index) => (
            <motion.div
              key={index}
              className={`service-card ${service.popular ? 'popular' : ''}`}
              initial={{ opacity: 0, y: 30 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: index * 0.2 }}
            >
              {service.popular && <div className="popular-badge">Most Popular</div>}
              
              <div className="service-icon">{service.icon}</div>
              
              <h3 className="service-title">{service.title}</h3>
              
              <div className="service-meta">
                <span className="service-duration">
                  <Clock size={16} />
                  {service.duration}
                </span>
                <span className="service-price">
                  <DollarSign size={16} />
                  {service.price}
                </span>
              </div>

              <p className="service-description">{service.description}</p>

              <ul className="service-features">
                {service.features.map((feature, i) => (
                  <li key={i}>
                    <CheckCircle size={18} />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              <a href="#contact" className="service-cta">
                Get Started
              </a>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;
