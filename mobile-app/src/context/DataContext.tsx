import React, { createContext, useContext, useState, useEffect } from 'react';
import { databaseService } from '../services/databaseService';
import { apiService } from '../services/apiService';
import NetInfo from '@react-native-community/netinfo';

interface DataContextType {
  items: any[];
  categories: any[];
  isLoading: boolean;
  refreshData: () => Promise<void>;
  addItem: (item: any) => Promise<void>;
  updateItem: (id: number, item: any) => Promise<void>;
  deleteItem: (id: number) => Promise<void>;
  searchItems: (query: string) => Promise<any[]>;
  syncOfflineData: () => Promise<void>;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export const useData = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};

export const DataProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadInitialData();
    setupNetworkListener();
  }, []);

  const setupNetworkListener = () => {
    NetInfo.addEventListener(state => {
      if (state.isConnected) {
        syncOfflineData();
      }
    });
  };

  const loadInitialData = async () => {
    setIsLoading(true);
    try {
      // Load local data first
      const localItems = await databaseService.getItems();
      const localCategories = await databaseService.getCategories();
      
      setItems(localItems);
      setCategories(localCategories);

      // Try to sync with server if online
      const isOnline = (await NetInfo.fetch()).isConnected;
      if (isOnline) {
        await syncWithServer();
      }
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const syncWithServer = async () => {
    try {
      const response = await apiService.getItems();
      if (response.success) {
        // Save server data locally
        for (const item of response.data) {
          await databaseService.saveItem(item);
        }
        setItems(response.data);
      }
    } catch (error) {
      console.error('Error syncing with server:', error);
    }
  };

  const refreshData = async () => {
    setIsLoading(true);
    try {
      await loadInitialData();
    } finally {
      setIsLoading(false);
    }
  };

  const addItem = async (item: any) => {
    try {
      const newItem = {
        ...item,
        id: Date.now(),
        created_at: new Date().toISOString(),
        isOffline: true,
        syncStatus: 'pending' as const,
      };

      await databaseService.saveItem(newItem);
      setItems(prev => [newItem, ...prev]);

      // Try to sync with server
      const isOnline = (await NetInfo.fetch()).isConnected;
      if (isOnline) {
        const response = await apiService.postItem(item);
        if (response.success) {
          // Update local item with server data
          const updatedItem = { ...newItem, ...response.data, isOffline: false, syncStatus: 'synced' as const };
          await databaseService.saveItem(updatedItem);
          setItems(prev => prev.map(i => i.id === newItem.id ? updatedItem : i));
        }
      }
    } catch (error) {
      console.error('Error adding item:', error);
      throw error;
    }
  };

  const updateItem = async (id: number, itemData: any) => {
    try {
      const updatedItem = { ...itemData, id, updated_at: new Date().toISOString() };
      await databaseService.saveItem(updatedItem);
      setItems(prev => prev.map(item => item.id === id ? updatedItem : item));

      // Try to sync with server
      const isOnline = (await NetInfo.fetch()).isConnected;
      if (isOnline) {
        await apiService.updateItem(id, itemData);
      }
    } catch (error) {
      console.error('Error updating item:', error);
      throw error;
    }
  };

  const deleteItem = async (id: number) => {
    try {
      await databaseService.deleteItem(id);
      setItems(prev => prev.filter(item => item.id !== id));

      // Try to sync with server
      const isOnline = (await NetInfo.fetch()).isConnected;
      if (isOnline) {
        await apiService.deleteItem(id);
      }
    } catch (error) {
      console.error('Error deleting item:', error);
      throw error;
    }
  };

  const searchItems = async (query: string) => {
    try {
      return await databaseService.searchItems(query);
    } catch (error) {
      console.error('Error searching items:', error);
      return [];
    }
  };

  const syncOfflineData = async () => {
    try {
      await apiService.syncOfflineData();
      await refreshData();
    } catch (error) {
      console.error('Error syncing offline data:', error);
    }
  };

  const value: DataContextType = {
    items,
    categories,
    isLoading,
    refreshData,
    addItem,
    updateItem,
    deleteItem,
    searchItems,
    syncOfflineData,
  };

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>;
};
