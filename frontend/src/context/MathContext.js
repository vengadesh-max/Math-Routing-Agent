import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { fetchBackendJson } from '../api';

const MathContext = createContext();

const initialState = {
    currentQuestion: '',
    currentResponse: null,
    sessionId: null,
    feedbackSubmitted: false,
    loading: false,
    error: null,
    conversationHistory: [],
    learningInsights: null
};

const mathReducer = (state, action) => {
    switch (action.type) {
        case 'SET_QUESTION':
            return {
                ...state,
                currentQuestion: action.payload,
                error: null
            };

        case 'SET_LOADING':
            return {
                ...state,
                loading: action.payload
            };

        case 'SET_RESPONSE':
            return {
                ...state,
                currentResponse: action.payload,
                sessionId: action.payload.session_id,
                loading: false,
                error: null,
                conversationHistory: [
                    ...state.conversationHistory,
                    {
                        question: state.currentQuestion,
                        response: action.payload,
                        timestamp: new Date().toISOString()
                    }
                ]
            };

        case 'SET_ERROR':
            return {
                ...state,
                error: action.payload,
                loading: false
            };

        case 'SUBMIT_FEEDBACK':
            return {
                ...state,
                feedbackSubmitted: true
            };

        case 'RESET_FEEDBACK':
            return {
                ...state,
                feedbackSubmitted: false
            };

        case 'SET_LEARNING_INSIGHTS':
            return {
                ...state,
                learningInsights: action.payload
            };

        case 'CLEAR_CONVERSATION':
            return {
                ...state,
                conversationHistory: [],
                currentResponse: null,
                currentQuestion: '',
                sessionId: null
            };

        default:
            return state;
    }
};

export const MathProvider = ({ children }) => {
    const [state, dispatch] = useReducer(mathReducer, initialState);

    const askQuestion = async (question) => {
        dispatch({ type: 'SET_QUESTION', payload: question });
        dispatch({ type: 'SET_LOADING', payload: true });

        try {
            const { data } = await fetchBackendJson('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question })
            });

            if (data.success) {
                dispatch({ type: 'SET_RESPONSE', payload: data.response });
            } else {
                dispatch({ type: 'SET_ERROR', payload: data.error });
            }
        } catch (error) {
            dispatch({ type: 'SET_ERROR', payload: 'Failed to connect to the server' });
        }
    };

    const submitFeedback = async (rating, comments = '') => {
        if (!state.sessionId) return;

        try {
            const { data } = await fetchBackendJson('/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: state.sessionId,
                    rating,
                    comments
                })
            });

            if (data.success) {
                dispatch({ type: 'SUBMIT_FEEDBACK' });
            }
        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    };

    const loadLearningInsights = async () => {
        try {
            const { data } = await fetchBackendJson('/insights');
            dispatch({ type: 'SET_LEARNING_INSIGHTS', payload: data.insights });
        } catch (error) {
            console.error('Error loading learning insights:', error);
        }
    };

    const clearConversation = () => {
        dispatch({ type: 'CLEAR_CONVERSATION' });
    };

    const resetFeedback = () => {
        dispatch({ type: 'RESET_FEEDBACK' });
    };

    useEffect(() => {
        loadLearningInsights();
    }, []);

    const value = {
        ...state,
        askQuestion,
        submitFeedback,
        loadLearningInsights,
        clearConversation,
        resetFeedback
    };

    return (
        <MathContext.Provider value={value}>
            {children}
        </MathContext.Provider>
    );
};

export const useMath = () => {
    const context = useContext(MathContext);
    if (!context) {
        throw new Error('useMath must be used within a MathProvider');
    }
    return context;
};

