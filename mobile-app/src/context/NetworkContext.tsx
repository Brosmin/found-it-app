import React, { createContext, useContext, useState, useEffect } from 'react';
import NetInfo from '@react-native-community/netinfo';

interface NetworkContextType {
  isOnline: boolean;
  connectionType: string | null;
  isConnected: boolean;
}

const NetworkContext = createContext<NetworkContextType | undefined>(undefined);

export const useNetwork = () => {
  const context = useContext(NetworkContext);
  if (!context) {
    throw new Error('useNetwork must be used within a NetworkProvider');
  }
  return context;
};

export const NetworkProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isOnline, setIsOnline] = useState(true);
  const [connectionType, setConnectionType] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected ?? false);
      setIsConnected(state.isConnected ?? false);
      setConnectionType(state.type);
    });

    // Get initial state
    NetInfo.fetch().then(state => {
      setIsOnline(state.isConnected ?? false);
      setIsConnected(state.isConnected ?? false);
      setConnectionType(state.type);
    });

    return unsubscribe;
  }, []);

  const value: NetworkContextType = {
    isOnline,
    connectionType,
    isConnected,
  };

  return <NetworkContext.Provider value={value}>{children}</NetworkContext.Provider>;
};
