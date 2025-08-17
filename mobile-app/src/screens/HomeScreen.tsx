import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  RefreshControl,
  Alert,
  Image,
  ScrollView,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Searchbar,
  Chip,
  FAB,
  Text,
  Badge,
} from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/apiService';
import NetInfo from '@react-native-community/netinfo';

interface Item {
  id: number;
  title: string;
  description: string;
  status: 'found' | 'lost';
  location: string;
  image_path?: string;
  category: {
    name: string;
    color: string;
  };
  created_at: string;
  isOffline?: boolean;
}

export default function HomeScreen() {
  const [items, setItems] = useState<Item[]>([]);
  const [filteredItems, setFilteredItems] = useState<Item[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<string>('all');
  const [isLoading, setIsLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  const navigation = useNavigation();
  const { user } = useAuth();

  useEffect(() => {
    loadItems();
    checkNetworkStatus();
  }, []);

  useEffect(() => {
    filterItems();
  }, [items, searchQuery, selectedStatus]);

  const checkNetworkStatus = async () => {
    const state = await NetInfo.fetch();
    setIsOnline(state.isConnected);
  };

  const loadItems = async () => {
    setIsLoading(true);
    try {
      const response = await apiService.getItems();
      if (response.success) {
        setItems(response.data);
      } else {
        Alert.alert('Error', 'Failed to load items');
      }
    } catch (error) {
      Alert.alert('Error', 'Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadItems();
    setRefreshing(false);
  };

  const filterItems = () => {
    let filtered = items;

    // Filter by status
    if (selectedStatus !== 'all') {
      filtered = filtered.filter(item => item.status === selectedStatus);
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(item =>
        item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.location.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredItems(filtered);
  };

  const renderItem = ({ item }: { item: Item }) => (
    <Card style={styles.card} onPress={() => navigation.navigate('ItemDetail', { item })}>
      <Card.Content>
        <View style={styles.itemHeader}>
          <Title style={styles.itemTitle}>{item.title}</Title>
          <Chip
            mode="outlined"
            style={[
              styles.statusChip,
              { backgroundColor: item.status === 'found' ? '#4CAF50' : '#FF9800' }
            ]}
            textStyle={{ color: 'white' }}
          >
            {item.status.toUpperCase()}
          </Chip>
        </View>

        {item.image_path && (
          <Image source={{ uri: item.image_path }} style={styles.itemImage} />
        )}

        <Paragraph style={styles.itemDescription} numberOfLines={2}>
          {item.description}
        </Paragraph>

        <View style={styles.itemFooter}>
          <Text style={styles.location}>📍 {item.location}</Text>
          <Text style={styles.date}>
            {new Date(item.created_at).toLocaleDateString()}
          </Text>
        </View>

        {item.isOffline && (
          <View style={styles.offlineIndicator}>
            <Text style={styles.offlineText}>📱 Offline</Text>
          </View>
        )}
      </Card.Content>
    </Card>
  );

  return (
    <View style={styles.container}>
      {!isOnline && (
        <View style={styles.offlineBanner}>
          <Text style={styles.offlineBannerText}>
            📱 You're offline. Changes will sync when connected.
          </Text>
        </View>
      )}

      <View style={styles.header}>
        <Searchbar
          placeholder="Search items..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchbar}
        />
      </View>

      <View style={styles.filters}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <Chip
            selected={selectedStatus === 'all'}
            onPress={() => setSelectedStatus('all')}
            style={styles.filterChip}
          >
            All
          </Chip>
          <Chip
            selected={selectedStatus === 'found'}
            onPress={() => setSelectedStatus('found')}
            style={styles.filterChip}
          >
            Found
          </Chip>
          <Chip
            selected={selectedStatus === 'lost'}
            onPress={() => setSelectedStatus('lost')}
            style={styles.filterChip}
          >
            Lost
          </Chip>
        </ScrollView>
      </View>

      <FlatList
        data={filteredItems}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Text style={styles.emptyStateText}>
              {isLoading ? 'Loading items...' : 'No items found'}
            </Text>
          </View>
        }
      />

      <FAB
        style={styles.fab}
        icon="plus"
        onPress={() => navigation.navigate('Post')}
        label="Post Item"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  offlineBanner: {
    backgroundColor: '#FF9800',
    padding: 10,
    alignItems: 'center',
  },
  offlineBannerText: {
    color: 'white',
    fontWeight: 'bold',
  },
  header: {
    padding: 16,
    backgroundColor: 'white',
  },
  searchbar: {
    elevation: 2,
  },
  filters: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: 'white',
  },
  filterChip: {
    marginRight: 8,
  },
  list: {
    padding: 16,
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  itemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  itemTitle: {
    flex: 1,
    fontSize: 18,
  },
  statusChip: {
    marginLeft: 8,
  },
  itemImage: {
    width: '100%',
    height: 200,
    borderRadius: 8,
    marginBottom: 8,
  },
  itemDescription: {
    marginBottom: 8,
    color: '#666',
  },
  itemFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  location: {
    color: '#2196F3',
    fontWeight: '500',
  },
  date: {
    color: '#999',
    fontSize: 12,
  },
  offlineIndicator: {
    position: 'absolute',
    top: 8,
    right: 8,
    backgroundColor: '#FF9800',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  offlineText: {
    color: 'white',
    fontSize: 10,
    fontWeight: 'bold',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 50,
  },
  emptyStateText: {
    fontSize: 16,
    color: '#666',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
  },
});
