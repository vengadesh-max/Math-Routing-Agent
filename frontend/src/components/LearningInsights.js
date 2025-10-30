import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, Users, Clock, Brain, Search, RefreshCw } from 'lucide-react';
import { useMath } from '../context/MathContext';

const InsightsContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const InsightsHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
`;

const InsightsTitle = styled.h2`
  color: #333;
  font-size: 28px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const RefreshButton = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
  }
`;

const MetricsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const MetricCard = styled(motion.div)`
  background: white;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: #667eea;
    transform: translateY(-5px);
  }
`;

const MetricIcon = styled.div`
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 15px;
`;

const MetricTitle = styled.h3`
  color: #333;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: 600;
`;

const MetricValue = styled.div`
  font-size: 24px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 5px;
`;

const MetricLabel = styled.div`
  color: #6c757d;
  font-size: 14px;
`;

const DetailedSection = styled.div`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
`;

const SectionTitle = styled.h3`
  color: #333;
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const PerformanceChart = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
`;

const PerformanceItem = styled.div`
  text-align: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
`;

const PerformanceValue = styled.div`
  font-size: 20px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 5px;
`;

const PerformanceLabel = styled.div`
  color: #6c757d;
  font-size: 14px;
`;

const SourceComparison = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
`;

const SourceCard = styled.div`
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid ${props => props.source === 'knowledge_base' ? '#28a745' : '#007bff'};
`;

const SourceTitle = styled.h4`
  color: #333;
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const SourceMetric = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 18px;
  color: #6c757d;
`;

const ErrorMessage = styled.div`
  background: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 10px;
  text-align: center;
`;

const LearningInsights = () => {
    const { learningInsights, loadLearningInsights } = useMath();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadInsights();
    }, []);

    const loadInsights = async () => {
        setLoading(true);
        setError(null);
        try {
            await loadLearningInsights();
        } catch (err) {
            setError('Failed to load learning insights');
        } finally {
            setLoading(false);
        }
    };

    const handleRefresh = () => {
        loadInsights();
    };

    if (loading) {
        return (
            <InsightsContainer>
                <LoadingSpinner>
                    <RefreshCw size={20} className="animate-spin" />
                    Loading insights...
                </LoadingSpinner>
            </InsightsContainer>
        );
    }

    if (error) {
        return (
            <InsightsContainer>
                <ErrorMessage>{error}</ErrorMessage>
            </InsightsContainer>
        );
    }

    if (!learningInsights) {
        return (
            <InsightsContainer>
                <ErrorMessage>No learning insights available</ErrorMessage>
            </InsightsContainer>
        );
    }

    const formatPercentage = (value) => {
        return `${Math.round(value * 100)}%`;
    };

    const formatNumber = (value) => {
        return typeof value === 'number' ? value.toFixed(2) : value;
    };

    return (
        <InsightsContainer>
            <InsightsHeader>
                <InsightsTitle>
                    <BarChart3 size={28} />
                    Learning Insights
                </InsightsTitle>
                <RefreshButton
                    onClick={handleRefresh}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    <RefreshCw size={16} />
                    Refresh
                </RefreshButton>
            </InsightsHeader>

            <MetricsGrid>
                <MetricCard
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <MetricIcon>
                        <Users size={24} />
                    </MetricIcon>
                    <MetricTitle>Total Interactions</MetricTitle>
                    <MetricValue>{learningInsights.total_interactions || 0}</MetricValue>
                    <MetricLabel>Questions processed</MetricLabel>
                </MetricCard>

                <MetricCard
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                >
                    <MetricIcon>
                        <TrendingUp size={24} />
                    </MetricIcon>
                    <MetricTitle>Average Rating</MetricTitle>
                    <MetricValue>{formatNumber(learningInsights.average_user_rating || 0)}</MetricValue>
                    <MetricLabel>Out of 5 stars</MetricLabel>
                </MetricCard>

                <MetricCard
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                >
                    <MetricIcon>
                        <Brain size={24} />
                    </MetricIcon>
                    <MetricTitle>Average Accuracy</MetricTitle>
                    <MetricValue>{formatPercentage(learningInsights.average_accuracy || 0)}</MetricValue>
                    <MetricLabel>Response accuracy</MetricLabel>
                </MetricCard>

                <MetricCard
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                >
                    <MetricIcon>
                        <Clock size={24} />
                    </MetricIcon>
                    <MetricTitle>Average Clarity</MetricTitle>
                    <MetricValue>{formatPercentage(learningInsights.average_clarity || 0)}</MetricValue>
                    <MetricLabel>Response clarity</MetricLabel>
                </MetricCard>
            </MetricsGrid>

            <DetailedSection>
                <SectionTitle>
                    <BarChart3 size={20} />
                    Performance Metrics
                </SectionTitle>
                <PerformanceChart>
                    <PerformanceItem>
                        <PerformanceValue>{formatPercentage(learningInsights.average_accuracy || 0)}</PerformanceValue>
                        <PerformanceLabel>Accuracy</PerformanceLabel>
                    </PerformanceItem>
                    <PerformanceItem>
                        <PerformanceValue>{formatPercentage(learningInsights.average_completeness || 0)}</PerformanceValue>
                        <PerformanceLabel>Completeness</PerformanceLabel>
                    </PerformanceItem>
                    <PerformanceItem>
                        <PerformanceValue>{formatPercentage(learningInsights.average_clarity || 0)}</PerformanceValue>
                        <PerformanceLabel>Clarity</PerformanceLabel>
                    </PerformanceItem>
                    <PerformanceItem>
                        <PerformanceValue>{formatPercentage(learningInsights.average_confidence || 0)}</PerformanceValue>
                        <PerformanceLabel>Confidence</PerformanceLabel>
                    </PerformanceItem>
                </PerformanceChart>
            </DetailedSection>

            {learningInsights.performance_by_source && (
                <DetailedSection>
                    <SectionTitle>
                        <Search size={20} />
                        Performance by Source
                    </SectionTitle>
                    <SourceComparison>
                        {Object.entries(learningInsights.performance_by_source).map(([source, metrics]) => (
                            <SourceCard key={source} source={source}>
                                <SourceTitle>
                                    {source === 'knowledge_base' ? <Brain size={16} /> : <Search size={16} />}
                                    {source.replace('_', ' ').toUpperCase()}
                                </SourceTitle>
                                <SourceMetric>
                                    <span>Count:</span>
                                    <span>{metrics.count || 0}</span>
                                </SourceMetric>
                                <SourceMetric>
                                    <span>Accuracy:</span>
                                    <span>{formatPercentage(metrics.accuracy || 0)}</span>
                                </SourceMetric>
                                <SourceMetric>
                                    <span>Avg Confidence:</span>
                                    <span>{formatPercentage(metrics.avg_confidence || 0)}</span>
                                </SourceMetric>
                            </SourceCard>
                        ))}
                    </SourceComparison>
                </DetailedSection>
            )}

            {learningInsights.common_improvements && learningInsights.common_improvements.length > 0 && (
                <DetailedSection>
                    <SectionTitle>
                        <TrendingUp size={20} />
                        Common Improvement Areas
                    </SectionTitle>
                    <div>
                        {learningInsights.common_improvements.map(([improvement, count], index) => (
                            <div key={index} style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                padding: '10px 0',
                                borderBottom: '1px solid #e9ecef'
                            }}>
                                <span>{improvement.replace('_', ' ').toUpperCase()}</span>
                                <span style={{ color: '#667eea', fontWeight: 'bold' }}>{count}</span>
                            </div>
                        ))}
                    </div>
                </DetailedSection>
            )}
        </InsightsContainer>
    );
};

export default LearningInsights;



