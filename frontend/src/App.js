import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Calculator, Brain, Search, CheckCircle, AlertCircle } from 'lucide-react';
import MathQuestionForm from './components/MathQuestionForm';
import MathResponse from './components/MathResponse';
import FeedbackForm from './components/FeedbackForm';
import LearningInsights from './components/LearningInsights';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import { MathProvider } from './context/MathContext';
import './App.css';
import { fetchBackendJson } from './api';

const AppContainer = styled.div`
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 250px;
  padding: 20px;
  max-width: calc(100vw - 250px);
`;

const ContentArea = styled.div`
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-bottom: 20px;
  min-height: 600px;
`;

const WelcomeSection = styled.div`
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  margin-bottom: 30px;
`;

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 30px;
`;

const FeatureCard = styled(motion.div)`
  background: white;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  border: 2px solid transparent;
  transition: all 0.3s ease;

  &:hover {
    border-color: #667eea;
    transform: translateY(-5px);
  }
`;

const FeatureIcon = styled.div`
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: white;
  font-size: 24px;
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: ${props => props.status === 'healthy' ? '#d4edda' : '#f8d7da'};
  color: ${props => props.status === 'healthy' ? '#155724' : '#721c24'};
  border-radius: 10px;
  margin-bottom: 20px;
`;

function App() {
    const [currentView, setCurrentView] = useState('home');
    const [systemStatus, setSystemStatus] = useState('checking');

    useEffect(() => {
        let isMounted = true;
        let pollId;

        const startPolling = async () => {
            await checkSystemHealthWithRetry();
            // keep polling every 5s until healthy
            pollId = setInterval(async () => {
                if (!isMounted || systemStatus === 'healthy') {
                    clearInterval(pollId);
                    return;
                }
                await checkSystemHealthWithRetry(1);
            }, 5000);
        };

        startPolling();

        return () => {
            isMounted = false;
            if (pollId) clearInterval(pollId);
        };
    }, [systemStatus]);

    const checkSystemHealthWithRetry = async (maxRetries = 5) => {
        for (let attempt = 0; attempt < maxRetries; attempt++) {
            try {
                const { res, data } = await fetchBackendJson('/health');
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                setSystemStatus(data.status === 'healthy' ? 'healthy' : 'unhealthy');
                return;
            } catch (error) {
                // wait with simple backoff before retrying
                await new Promise(resolve => setTimeout(resolve, 500 * (attempt + 1)));
            }
        }
        setSystemStatus('unhealthy');
    };

    const renderContent = () => {
        switch (currentView) {
            case 'ask':
                return (
                    <ContentArea>
                        <MathQuestionForm />
                    </ContentArea>
                );
            case 'insights':
                return (
                    <ContentArea>
                        <LearningInsights />
                    </ContentArea>
                );
            default:
                return (
                    <ContentArea>
                        <WelcomeSection>
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.6 }}
                            >
                                <Calculator size={60} style={{ marginBottom: '20px' }} />
                                <h1>Math Routing Agent</h1>
                                <p style={{ fontSize: '18px', marginBottom: '30px' }}>
                                    AI-powered mathematical problem solving with intelligent routing
                                </p>
                            </motion.div>
                        </WelcomeSection>

                        <StatusIndicator status={systemStatus}>
                            {systemStatus === 'healthy' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
                            System Status: {systemStatus === 'healthy' ? 'Healthy' : 'Unhealthy'}
                        </StatusIndicator>

                        <FeatureGrid>
                            <FeatureCard
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => setCurrentView('ask')}
                            >
                                <FeatureIcon>
                                    <Calculator size={24} />
                                </FeatureIcon>
                                <h3>Ask Math Questions</h3>
                                <p>Get step-by-step solutions to mathematical problems</p>
                            </FeatureCard>

                            <FeatureCard
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                <FeatureIcon>
                                    <Brain size={24} />
                                </FeatureIcon>
                                <h3>Intelligent Routing</h3>
                                <p>Automatically routes between knowledge base and web search</p>
                            </FeatureCard>

                            <FeatureCard
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                <FeatureIcon>
                                    <Search size={24} />
                                </FeatureIcon>
                                <h3>Comprehensive Search</h3>
                                <p>Finds solutions from multiple sources and formats</p>
                            </FeatureCard>

                            <FeatureCard
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => setCurrentView('insights')}
                            >
                                <FeatureIcon>
                                    <CheckCircle size={24} />
                                </FeatureIcon>
                                <h3>Learning Insights</h3>
                                <p>View system performance and learning analytics</p>
                            </FeatureCard>
                        </FeatureGrid>
                    </ContentArea>
                );
        }
    };

    return (
        <MathProvider>
            <AppContainer>
                <Sidebar currentView={currentView} setCurrentView={setCurrentView} />
                <MainContent>
                    <Header />
                    {renderContent()}
                </MainContent>
            </AppContainer>
        </MathProvider>
    );
}

export default App;

