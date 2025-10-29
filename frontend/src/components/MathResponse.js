import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { CheckCircle, ExternalLink, Brain, Search, Clock, AlertTriangle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import FeedbackForm from './FeedbackForm';

const ResponseContainer = styled(motion.div)`
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 15px;
  padding: 30px;
  margin-top: 30px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
`;

const ResponseHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f8f9fa;
`;

const SourceInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  color: #6c757d;
  font-size: 14px;
`;

const SourceIcon = styled.div`
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: ${props => props.source === 'knowledge_base' ? '#28a745' : '#007bff'};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const ConfidenceBar = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

const ConfidenceLabel = styled.span`
  font-size: 14px;
  color: #6c757d;
`;

const ConfidenceValue = styled.div`
  width: 100px;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
`;

const ConfidenceFill = styled.div`
  height: 100%;
  background: ${props => {
        if (props.confidence >= 0.8) return '#28a745';
        if (props.confidence >= 0.6) return '#ffc107';
        return '#dc3545';
    }};
  width: ${props => props.confidence * 100}%;
  transition: width 0.3s ease;
`;

const AnswerSection = styled.div`
  margin-bottom: 30px;
`;

const SectionTitle = styled.h3`
  color: #333;
  margin-bottom: 15px;
  font-size: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const AnswerContent = styled.div`
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #667eea;
  font-size: 16px;
  line-height: 1.6;
`;

const StepsSection = styled.div`
  margin-bottom: 30px;
`;

const StepsList = styled.ol`
  counter-reset: step-counter;
  list-style: none;
  padding: 0;
`;

const StepItem = styled.li`
  counter-increment: step-counter;
  margin-bottom: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #667eea;
  position: relative;

  &::before {
    content: counter(step-counter);
    position: absolute;
    left: -15px;
    top: 15px;
    width: 30px;
    height: 30px;
    background: #667eea;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 14px;
  }
`;

const ExplanationSection = styled.div`
  margin-bottom: 30px;
`;

const ExplanationContent = styled.div`
  background: #e8f4fd;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #007bff;
  font-size: 16px;
  line-height: 1.6;
`;

const RoutingInfo = styled.div`
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
`;

const RoutingTitle = styled.h4`
  color: #333;
  margin-bottom: 10px;
  font-size: 16px;
`;

const RoutingDetails = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
`;

const RoutingItem = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #6c757d;
`;

const ValidationWarnings = styled.div`
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
`;

const WarningItem = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  color: #856404;
  font-size: 14px;
  margin-bottom: 5px;

  &:last-child {
    margin-bottom: 0;
  }
`;

const MathResponse = ({ response }) => {
    const formatConfidence = (confidence) => {
        return Math.round(confidence * 100);
    };

    const getSourceIcon = (source) => {
        return source === 'knowledge_base' ? <Brain size={16} /> : <Search size={16} />;
    };

    const getSourceLabel = (source) => {
        return source === 'knowledge_base' ? 'Knowledge Base' : 'Web Search';
    };

    return (
        <ResponseContainer
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <ResponseHeader>
                <SourceInfo>
                    <SourceIcon source={response.source}>
                        {getSourceIcon(response.source)}
                    </SourceIcon>
                    <span>{getSourceLabel(response.source)}</span>
                    <Clock size={14} />
                    <span>{new Date(response.timestamp).toLocaleTimeString()}</span>
                </SourceInfo>

                <ConfidenceBar>
                    <ConfidenceLabel>Confidence:</ConfidenceLabel>
                    <ConfidenceValue>
                        <ConfidenceFill confidence={response.confidence} />
                    </ConfidenceValue>
                    <span>{formatConfidence(response.confidence)}%</span>
                </ConfidenceBar>
            </ResponseHeader>

            <AnswerSection>
                <SectionTitle>
                    <CheckCircle size={20} color="#28a745" />
                    Answer
                </SectionTitle>
                <AnswerContent>
                    <ReactMarkdown>{response.answer}</ReactMarkdown>
                </AnswerContent>
            </AnswerSection>

            {response.solution_steps && response.solution_steps.length > 0 && (
                <StepsSection>
                    <SectionTitle>Solution Steps</SectionTitle>
                    <StepsList>
                        {response.solution_steps.map((step, index) => (
                            <StepItem key={index}>
                                <ReactMarkdown>{step}</ReactMarkdown>
                            </StepItem>
                        ))}
                    </StepsList>
                </StepsSection>
            )}

            {response.explanation && (
                <ExplanationSection>
                    <SectionTitle>Explanation</SectionTitle>
                    <ExplanationContent>
                        <ReactMarkdown>{response.explanation}</ReactMarkdown>
                    </ExplanationContent>
                </ExplanationSection>
            )}

            {response.routing_info && (
                <RoutingInfo>
                    <RoutingTitle>Routing Information</RoutingTitle>
                    <RoutingDetails>
                        <RoutingItem>
                            <strong>Decision:</strong> {response.routing_info.decision}
                        </RoutingItem>
                        <RoutingItem>
                            <strong>Confidence:</strong> {formatConfidence(response.routing_info.confidence)}%
                        </RoutingItem>
                        <RoutingItem>
                            <strong>Reasoning:</strong> {response.routing_info.reasoning}
                        </RoutingItem>
                    </RoutingDetails>
                </RoutingInfo>
            )}

            {response.validation_info && response.validation_info.output_warnings && response.validation_info.output_warnings.length > 0 && (
                <ValidationWarnings>
                    <WarningItem>
                        <AlertTriangle size={16} />
                        <strong>Validation Warnings:</strong>
                    </WarningItem>
                    {response.validation_info.output_warnings.map((warning, index) => (
                        <WarningItem key={index}>
                            • {warning}
                        </WarningItem>
                    ))}
                </ValidationWarnings>
            )}

            <FeedbackForm sessionId={response.session_id} />
        </ResponseContainer>
    );
};

export default MathResponse;

