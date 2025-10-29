import React, { useEffect, useState } from 'react';
import { fetchBackendJson } from '../api';
import styled from 'styled-components';
import { Calculator, Brain } from 'lucide-react';

const HeaderContainer = styled.header`
  background: white;
  padding: 20px 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const LogoIcon = styled.div`
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const LogoText = styled.div`
  h1 {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
    color: #333;
  }
  
  p {
    margin: 0;
    font-size: 14px;
    color: #6c757d;
  }
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: ${props => props.status === 'healthy' ? '#d4edda' : '#f8d7da'};
  color: ${props => props.status === 'healthy' ? '#155724' : '#721c24'};
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
`;

const Header = () => {
  const [status, setStatus] = useState('checking');

  useEffect(() => {
    let poll;
    const check = async () => {
      try {
        const { res, data } = await fetchBackendJson('/health');
        if (!res.ok) throw new Error('bad');
        setStatus(data.status === 'healthy' ? 'healthy' : 'unhealthy');
      } catch {
        setStatus('unhealthy');
      }
    };
    check();
    poll = setInterval(check, 5000);
    return () => clearInterval(poll);
  }, []);

  return (
    <HeaderContainer>
      <Logo>
        <LogoIcon>
          <Calculator size={24} />
        </LogoIcon>
        <LogoText>
          <h1>Math Routing Agent</h1>
          <p>AI-Powered Mathematical Problem Solving</p>
        </LogoText>
      </Logo>

      <StatusIndicator status={status}>
        <Brain size={16} />
        {status === 'healthy' ? 'System Online' : 'System Offline'}
      </StatusIndicator>
    </HeaderContainer>
  );
};

export default Header;

