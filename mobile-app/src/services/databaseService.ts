import AsyncStorage from '@react-native-async-storage/async-storage';

interface LocalItem {
  id: number;
  title: string;
  description: string;
  status: 'found' | 'lost';
  location: string;
  image_path?: string;
  category_id: number;
  created_at: string;
  updated_at: string;
  isOffline?: boolean;
  syncStatus: 'synced' | 'pending' | 'failed';
}

interface LocalUser {
  id: number;
  username: string;
  email: string;
  role: string;
  phone?: string;
  created_at: string;
}

class DatabaseService {
  private static instance: DatabaseService;

  static getInstance(): DatabaseService {
    if (!DatabaseService.instance) {
      DatabaseService.instance = new DatabaseService();
    }
    return DatabaseService.instance;
  }

  async initializeDatabase(): Promise<void> {
    try {
      // Initialize default categories if they don't exist
      const categories = await this.getCategories();
      if (categories.length === 0) {
        await this.initializeDefaultCategories();
      }
    } catch (error) {
      console.error('Database initialization failed:', error);
    }
  }

  private async initializeDefaultCategories(): Promise<void> {
    const defaultCategories = [
      { id: 1, name: 'Electronics', color: '#2196F3', icon: 'phone' },
      { id: 2, name: 'Clothing', color: '#4CAF50', icon: 'tshirt' },
      { id: 3, name: 'Books', color: '#FF9800', icon: 'book' },
      { id: 4, name: 'Jewelry', color: '#9C27B0', icon: 'diamond' },
      { id: 5, name: 'Keys', color: '#F44336', icon: 'key' },
      { id: 6, name: 'Documents', color: '#607D8B', icon: 'file' },
      { id: 7, name: 'Other', color: '#795548', icon: 'help-circle' },
    ];

    await AsyncStorage.setItem('categories', JSON.stringify(defaultCategories));
  }

  // Items CRUD operations
  async saveItem(item: LocalItem): Promise<void> {
    try {
      const items = await this.getItems();
      const existingIndex = items.findIndex(i => i.id === item.id);
      
      if (existingIndex >= 0) {
        items[existingIndex] = { ...items[existingIndex], ...item };
      } else {
        items.push(item);
      }
      
      await AsyncStorage.setItem('items', JSON.stringify(items));
    } catch (error) {
      console.error('Error saving item:', error);
      throw error;
    }
  }

  async getItems(): Promise<LocalItem[]> {
    try {
      const items = await AsyncStorage.getItem('items');
      return items ? JSON.parse(items) : [];
    } catch (error) {
      console.error('Error getting items:', error);
      return [];
    }
  }

  async getItemById(id: number): Promise<LocalItem | null> {
    try {
      const items = await this.getItems();
      return items.find(item => item.id === id) || null;
    } catch (error) {
      console.error('Error getting item by id:', error);
      return null;
    }
  }

  async deleteItem(id: number): Promise<void> {
    try {
      const items = await this.getItems();
      const filteredItems = items.filter(item => item.id !== id);
      await AsyncStorage.setItem('items', JSON.stringify(filteredItems));
    } catch (error) {
      console.error('Error deleting item:', error);
      throw error;
    }
  }

  async searchItems(query: string): Promise<LocalItem[]> {
    try {
      const items = await this.getItems();
      const lowerQuery = query.toLowerCase();
      
      return items.filter(item =>
        item.title.toLowerCase().includes(lowerQuery) ||
        item.description.toLowerCase().includes(lowerQuery) ||
        item.location.toLowerCase().includes(lowerQuery)
      );
    } catch (error) {
      console.error('Error searching items:', error);
      return [];
    }
  }

  // Categories
  async getCategories(): Promise<any[]> {
    try {
      const categories = await AsyncStorage.getItem('categories');
      return categories ? JSON.parse(categories) : [];
    } catch (error) {
      console.error('Error getting categories:', error);
      return [];
    }
  }

  // Users
  async saveUser(user: LocalUser): Promise<void> {
    try {
      const users = await this.getUsers();
      const existingIndex = users.findIndex(u => u.id === user.id);
      
      if (existingIndex >= 0) {
        users[existingIndex] = { ...users[existingIndex], ...user };
      } else {
        users.push(user);
      }
      
      await AsyncStorage.setItem('users', JSON.stringify(users));
    } catch (error) {
      console.error('Error saving user:', error);
      throw error;
    }
  }

  async getUsers(): Promise<LocalUser[]> {
    try {
      const users = await AsyncStorage.getItem('users');
      return users ? JSON.parse(users) : [];
    } catch (error) {
      console.error('Error getting users:', error);
      return [];
    }
  }

  // Offline queue management
  async addToOfflineQueue(action: string, data: any): Promise<void> {
    try {
      const queue = await this.getOfflineQueue();
      queue.push({
        id: Date.now(),
        action,
        data,
        timestamp: new Date().toISOString(),
        retryCount: 0,
      });
      await AsyncStorage.setItem('offline_queue', JSON.stringify(queue));
    } catch (error) {
      console.error('Error adding to offline queue:', error);
      throw error;
    }
  }

  async getOfflineQueue(): Promise<any[]> {
    try {
      const queue = await AsyncStorage.getItem('offline_queue');
      return queue ? JSON.parse(queue) : [];
    } catch (error) {
      console.error('Error getting offline queue:', error);
      return [];
    }
  }

  async removeFromOfflineQueue(id: number): Promise<void> {
    try {
      const queue = await this.getOfflineQueue();
      const filteredQueue = queue.filter(item => item.id !== id);
      await AsyncStorage.setItem('offline_queue', JSON.stringify(filteredQueue));
    } catch (error) {
      console.error('Error removing from offline queue:', error);
      throw error;
    }
  }

  // Settings and preferences
  async saveSettings(settings: any): Promise<void> {
    try {
      await AsyncStorage.setItem('settings', JSON.stringify(settings));
    } catch (error) {
      console.error('Error saving settings:', error);
      throw error;
    }
  }

  async getSettings(): Promise<any> {
    try {
      const settings = await AsyncStorage.getItem('settings');
      return settings ? JSON.parse(settings) : {};
    } catch (error) {
      console.error('Error getting settings:', error);
      return {};
    }
  }

  // Search history
  async addSearchHistory(query: string): Promise<void> {
    try {
      const history = await this.getSearchHistory();
      const newHistory = [query, ...history.filter(h => h !== query)].slice(0, 10);
      await AsyncStorage.setItem('search_history', JSON.stringify(newHistory));
    } catch (error) {
      console.error('Error adding search history:', error);
    }
  }

  async getSearchHistory(): Promise<string[]> {
    try {
      const history = await AsyncStorage.getItem('search_history');
      return history ? JSON.parse(history) : [];
    } catch (error) {
      console.error('Error getting search history:', error);
      return [];
    }
  }

  // Clear all data (for logout)
  async clearAllData(): Promise<void> {
    try {
      const keysToKeep = ['auth_token', 'user_data', 'settings'];
      const allKeys = await AsyncStorage.getAllKeys();
      const keysToRemove = allKeys.filter(key => !keysToKeep.includes(key));
      await AsyncStorage.multiRemove(keysToRemove);
    } catch (error) {
      console.error('Error clearing data:', error);
      throw error;
    }
  }

  // Database statistics
  async getDatabaseStats(): Promise<any> {
    try {
      const items = await this.getItems();
      const users = await this.getUsers();
      const queue = await this.getOfflineQueue();
      
      return {
        totalItems: items.length,
        offlineItems: items.filter(item => item.isOffline).length,
        totalUsers: users.length,
        pendingSync: queue.length,
        lastSync: await AsyncStorage.getItem('last_sync'),
      };
    } catch (error) {
      console.error('Error getting database stats:', error);
      return {};
    }
  }
}

export const databaseService = DatabaseService.getInstance();
export const initializeDatabase = () => databaseService.initializeDatabase();
