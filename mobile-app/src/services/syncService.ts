import { apiService } from './apiService';
import { databaseService } from './databaseService';
import NetInfo from '@react-native-community/netinfo';

export const syncOfflineData = async () => {
  try {
    const isOnline = (await NetInfo.fetch()).isConnected;
    if (!isOnline) {
      console.log('Device is offline, skipping sync');
      return;
    }

    console.log('Starting offline data sync...');
    await apiService.syncOfflineData();
    
    // Update last sync timestamp
    const now = new Date().toISOString();
    await databaseService.saveSettings({ lastSync: now });
    
    console.log('Offline data sync completed');
  } catch (error) {
    console.error('Error syncing offline data:', error);
  }
};
