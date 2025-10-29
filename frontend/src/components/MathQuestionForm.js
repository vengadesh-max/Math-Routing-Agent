import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Send, Loader, AlertCircle } from 'lucide-react';
import { useMath } from '../context/MathContext';
import MathResponse from './MathResponse';

const FormContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const FormTitle = styled.h2`
  color: #333;
  margin-bottom: 30px;
  text-align: center;
  font-size: 28px;
  font-weight: 600;
`;

const QuestionForm = styled.form`
  background: #f8f9fa;
  padding: 30px;
  border-radius: 15px;
  margin-bottom: 30px;
  border: 2px solid #e9ecef;
  transition: border-color 0.3s ease;

  &:focus-within {
    border-color: #667eea;
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  min-height: 120px;
  padding: 15px;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 16px;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
  }

  &::placeholder {
    color: #6c757d;
  }
`;

const ButtonContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 20px;
`;

const SubmitButton = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
  }
`;

const ErrorMessage = styled(motion.div)`
  background: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 10px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const ExampleQuestions = styled.div`
  margin-top: 30px;
`;

const ExampleTitle = styled.h3`
  color: #333;
  margin-bottom: 15px;
  font-size: 18px;
`;

const ExampleList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 10px;
`;

const ExampleItem = styled(motion.button)`
  background: white;
  border: 2px solid #e9ecef;
  padding: 15px;
  border-radius: 10px;
  text-align: left;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;

  &:hover {
    border-color: #667eea;
    background: #f8f9fa;
  }
`;

const MathQuestionForm = () => {
    const { askQuestion, loading, error, currentResponse } = useMath();
    const [question, setQuestion] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (question.trim()) {
            await askQuestion(question.trim());
        }
    };

    const handleExampleClick = (exampleQuestion) => {
        setQuestion(exampleQuestion);
    };

    const exampleQuestions = [
        "Solve the equation: 2x + 5 = 13",
        "Find the derivative of f(x) = x² + 3x + 2",
        "Calculate the area of a triangle with base 6 cm and height 8 cm",
        "What is the value of sin(30°)?",
        "Find the mean of the numbers: 2, 4, 6, 8, 10",
        "Evaluate the integral: ∫(2x + 3)dx",
        "Factor the quadratic: x² - 5x + 6",
        "Find the circumference of a circle with radius 5 cm"
    ];

    return (
        <FormContainer>
            <FormTitle>Ask a Math Question</FormTitle>

            <QuestionForm onSubmit={handleSubmit}>
                <TextArea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Enter your mathematical question here... (e.g., 'Solve the equation 2x + 5 = 13')"
                    disabled={loading}
                />

                <ButtonContainer>
                    <SubmitButton
                        type="submit"
                        disabled={loading || !question.trim()}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        {loading ? (
                            <>
                                <Loader size={20} className="animate-spin" />
                                Processing...
                            </>
                        ) : (
                            <>
                                <Send size={20} />
                                Ask Question
                            </>
                        )}
                    </SubmitButton>
                </ButtonContainer>
            </QuestionForm>

            {error && (
                <ErrorMessage
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                >
                    <AlertCircle size={20} />
                    {error}
                </ErrorMessage>
            )}

            <ExampleQuestions>
                <ExampleTitle>Example Questions</ExampleTitle>
                <ExampleList>
                    {exampleQuestions.map((example, index) => (
                        <ExampleItem
                            key={index}
                            onClick={() => handleExampleClick(example)}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                        >
                            {example}
                        </ExampleItem>
                    ))}
                </ExampleList>
            </ExampleQuestions>

            {currentResponse && <MathResponse response={currentResponse} />}
        </FormContainer>
    );
};

export default MathQuestionForm;

