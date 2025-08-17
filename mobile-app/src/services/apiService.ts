import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';

const API_BASE_URL = 'https://found-it-app.onrender.com'; // Updated to your actual Render app URL

class ApiService {
  private token: string | null = null;
  private offlineQueue: Array<{ action: string; data: any; timestamp: number }> = [];

  constructor() {
    this.setupInterceptors();
    this.loadOfflineQueue();
  }

  private setupInterceptors() {
    // Request interceptor
    axios.interceptors.request.use(
      async (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expired, clear auth
          await this.clearToken();
        }
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string) {
    this.token = token;
  }

  clearToken() {
    this.token = null;
  }

  async login(email: string, password: string) {
    try {
      const response = await axios.post(`${API_BASE_URL}/login`, {
        email,
        password,
      });
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data || 'Login failed' };
    }
  }

  async register(userData: any) {
    try {
      const response = await axios.post(`${API_BASE_URL}/register`, userData);
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data || 'Registration failed' };
    }
  }

  async getItems(filters = {}) {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/items`, { params: filters });
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data || 'Failed to fetch items' };
    }
  }

  async postItem(itemData: any) {
    const isOnline = (await NetInfo.fetch()).isConnected;
    
    if (!isOnline) {
      // Store for later sync
      this.addToOfflineQueue('postItem', itemData);
      return { success: true, data: { id: Date.now(), ...itemData, isOffline: true } };
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/post_item`, itemData);
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data || 'Failed to post item' };
    }
  }

  async updateItem(id: number, itemData: any) {
    const isOnline = (await NetInfo.fetch()).isConnected;
    
    if (!isOnline) {
      this.addToOfflineQueue('updateItem', { id, ...itemData });
      return { success: true, data: { id, ...itemData, isOffline: true } };
    }

    try {
      const response = await axios.put(`${API_BASE_URL}/admin/items/edit/${id}`, itemData);
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data || 'Failed to update item' };
    }
  }

  async deleteItem(id: number) {
    const isOnline = (await NetInfo.fetch()).isConnected;
    
    if (!isOnline) {
      this.addToOfflineQueue('deleteItem', { id });
      return { success: true };
    }

    try {
      await axios.delete(`${API_BASE_URL}/admin/items/delete/${id}`);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data || 'Failed to delete item' };
    }
  }

  async getMatches() {
    try {
      const response = await axios.get(`${API_BASE_URL}/matches`);
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data || 'Failed to fetch matches' };
    }
  }

  private async addToOfflineQueue(action: string, data: any) {
    const queueItem = {
      action,
      data,
      timestamp: Date.now(),
    };
    
    this.offlineQueue.push(queueItem);
    await AsyncStorage.setItem('offline_queue', JSON.stringify(this.offlineQueue));
  }

  private async loadOfflineQueue() {
    try {
      const queue = await AsyncStorage.getItem('offline_queue');
      if (queue) {
        this.offlineQueue = JSON.parse(queue);
      }
    } catch (error) {
      console.error('Error loading offline queue:', error);
    }
  }

  async syncOfflineData() {
    if (this.offlineQueue.length === 0) return;

    const isOnline = (await NetInfo.fetch()).isConnected;
    if (!isOnline) return;

    const queueToProcess = [...this.offlineQueue];
    this.offlineQueue = [];

    for (const item of queueToProcess) {
      try {
        switch (item.action) {
          case 'postItem':
            await this.postItem(item.data);
            break;
          case 'updateItem':
            await this.updateItem(item.data.id, item.data);
            break;
          case 'deleteItem':
            await this.deleteItem(item.data.id);
            break;
        }
      } catch (error) {
        console.error('Error syncing offline data:', error);
        this.offlineQueue.push(item);
      }
    }

    await AsyncStorage.setItem('offline_queue', JSON.stringify(this.offlineQueue));
  }
}

export const apiService = new ApiService();
