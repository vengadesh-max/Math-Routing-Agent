import React, { useState } from 'react';
import styled from 'styled-components';

const FormContainer = styled.div`
  margin-top: 20px;
  padding: 16px;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  background: #f8f9fa;
`;

const Title = styled.h4`
  margin: 0 0 12px 0;
  color: #333;
`;

const Row = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
`;

const RatingButton = styled.button`
  padding: 6px 10px;
  border-radius: 8px;
  border: 1px solid ${props => (props.active ? '#667eea' : '#dee2e6')};
  background: ${props => (props.active ? '#eef0ff' : 'white')};
  cursor: pointer;
`;

const TextArea = styled.textarea`
  width: 100%;
  min-height: 70px;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #dee2e6;
  resize: vertical;
`;

const SubmitButton = styled.button`
  margin-top: 10px;
  padding: 8px 14px;
  border-radius: 8px;
  border: none;
  background: #667eea;
  color: white;
  cursor: pointer;
`;

const StatusText = styled.div`
  margin-top: 8px;
  font-size: 14px;
  color: #6c757d;
`;

const FeedbackForm = ({ sessionId }) => {
    const [rating, setRating] = useState(5);
    const [comments, setComments] = useState('');
    const [status, setStatus] = useState('');
    const [submitting, setSubmitting] = useState(false);

    const submitFeedback = async () => {
        try {
            setSubmitting(true);
            setStatus('');
            const res = await fetch('/feedback', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId || 'unknown', rating, comments })
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            setStatus(data.message || 'Feedback submitted');
            setComments('');
        } catch (err) {
            setStatus('Failed to submit feedback');
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <FormContainer>
            <Title>Was this helpful?</Title>
            <Row>
                {[1, 2, 3, 4, 5].map((n) => (
                    <RatingButton key={n} active={rating === n} onClick={() => setRating(n)}>
                        {n}
                    </RatingButton>
                ))}
            </Row>
            <TextArea
                placeholder="Any comments to improve the answer?"
                value={comments}
                onChange={(e) => setComments(e.target.value)}
            />
            <SubmitButton onClick={submitFeedback} disabled={submitting}>
                {submitting ? 'Submitting...' : 'Submit Feedback'}
            </SubmitButton>
            {status && <StatusText>{status}</StatusText>}
        </FormContainer>
    );
};

export default FeedbackForm;



