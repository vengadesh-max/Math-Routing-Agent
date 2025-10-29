import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Home, Calculator, BarChart3, Settings } from 'lucide-react';

const SidebarContainer = styled.div`
  position: fixed;
  left: 0;
  top: 0;
  width: 250px;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  z-index: 1000;
  overflow-y: auto;
`;

const SidebarHeader = styled.div`
  text-align: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
`;

const SidebarTitle = styled.h2`
  margin: 0;
  font-size: 20px;
  font-weight: 700;
`;

const SidebarSubtitle = styled.p`
  margin: 5px 0 0 0;
  font-size: 12px;
  opacity: 0.8;
`;

const Navigation = styled.nav`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const NavItem = styled(motion.button)`
  background: ${props => props.active ? 'rgba(255, 255, 255, 0.2)' : 'transparent'};
  border: none;
  color: white;
  padding: 15px 20px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  text-align: left;
  width: 100%;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateX(5px);
  }
`;

const NavIcon = styled.div`
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Sidebar = ({ currentView, setCurrentView }) => {
    const navItems = [
        { id: 'home', label: 'Home', icon: Home },
        { id: 'ask', label: 'Ask Question', icon: Calculator },
        { id: 'insights', label: 'Insights', icon: BarChart3 },
        { id: 'settings', label: 'Settings', icon: Settings }
    ];

    return (
        <SidebarContainer>
            <SidebarHeader>
                <SidebarTitle>Math Agent</SidebarTitle>
                <SidebarSubtitle>AI-Powered Learning</SidebarSubtitle>
            </SidebarHeader>

            <Navigation>
                {navItems.map((item) => {
                    const Icon = item.icon;
                    return (
                        <NavItem
                            key={item.id}
                            active={currentView === item.id}
                            onClick={() => setCurrentView(item.id)}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <NavIcon>
                                <Icon size={20} />
                            </NavIcon>
                            {item.label}
                        </NavItem>
                    );
                })}
            </Navigation>
        </SidebarContainer>
    );
};

export default Sidebar;


