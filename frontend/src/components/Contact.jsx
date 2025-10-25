import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { useState } from 'react';
import { Mail, Building, User, MessageSquare, Send, CheckCircle } from 'lucide-react';
import './Contact.css';

const Contact = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    message: '',
  });

  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError(''); // Clear error on input
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');
    
    try {
      const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
      const response = await fetch(`${API_URL}/api/v1/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();
      
      if (response.ok && data.success) {
        setSubmitted(true);
        setTimeout(() => {
          setSubmitted(false);
          setFormData({ name: '', email: '', company: '', message: '' });
        }, 5000);
      } else {
        setError(data.error?.message || 'Failed to submit. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section id="contact" className="contact" ref={ref}>
      <div className="contact-container">
        <motion.div
          className="contact-header"
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
        >
          <h2 className="contact-title">Let's Build Together</h2>
          <p className="contact-subtitle">
            Ready to transform your business with AI? Let's start the conversation.
          </p>
        </motion.div>

        <div className="contact-content">
          <motion.div
            className="contact-info"
            initial={{ opacity: 0, x: -30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h3>Get in Touch</h3>
            <p>
              Whether you're just exploring AI possibilities or ready to implement custom
              solutions, we're here to help. Tell us about your challenges, and let's
              figure out the best path forward together.
            </p>

            <div className="contact-details">
              <div className="contact-detail">
                <Mail />
                <div>
                  <strong>Email</strong>
                  <p>hello@attec.co.ke</p>
                </div>
              </div>
              <div className="contact-detail">
                <Building />
                <div>
                  <strong>Location</strong>
                  <p>Nairobi, Kenya</p>
                </div>
              </div>
            </div>

            <div className="contact-cta-box">
              <h4>What to Expect</h4>
              <ul>
                <li>Response within 24 hours</li>
                <li>Free initial consultation</li>
                <li>No-pressure conversation</li>
                <li>Clear next steps</li>
              </ul>
            </div>
          </motion.div>

          <motion.form
            className="contact-form"
            onSubmit={handleSubmit}
            initial={{ opacity: 0, x: 30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            {submitted ? (
              <div className="contact-success">
                <CheckCircle size={48} />
                <h3>Thank You!</h3>
                <p>We've received your message and will get back to you within 24 hours.</p>
                <p style={{ fontSize: '0.9rem', marginTop: '1rem', opacity: 0.8 }}>
                  Check your email for a confirmation message.
                </p>
              </div>
            ) : (
              <>
                {error && (
                  <div className="contact-error">
                    <p>{error}</p>
                  </div>
                )}
                
                <div className="form-group">
                  <label htmlFor="name">
                    <User size={18} />
                    Full Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    placeholder="John Doe"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email">
                    <Mail size={18} />
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="john@company.com"
                    disabled={isSubmitting}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="company">
                    <Building size={18} />
                    Company Name
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    placeholder="Your Company"
                    disabled={isSubmitting}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="message">
                    <MessageSquare size={18} />
                    Project Description *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows="5"
                    placeholder="Tell us about your project, challenges, or questions..."
                    disabled={isSubmitting}
                  />
                </div>

                <button 
                  type="submit" 
                  className="contact-submit"
                  disabled={isSubmitting}
                >
                  <Send size={20} />
                  {isSubmitting ? 'Sending...' : 'Send Message'}
                </button>
              </>
            )}
          </motion.form>
        </div>
      </div>

      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2025 ATTEC. Building Tomorrow's Technology Today.</p>
        </div>
      </footer>
    </section>
  );
};

export default Contact;
