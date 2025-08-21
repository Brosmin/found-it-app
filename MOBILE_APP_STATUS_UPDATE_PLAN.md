# Mobile App Status Update Plan

## Current Status Implementation
The mobile app currently handles basic item statuses but needs to be updated to support the new 'recovered' and 'removed' statuses.

## Implementation Plan

### 1. Update Item Interface
Update the Item interface in the mobile app to include the new statuses:

In `mobile-app/src/context/DataContext.tsx`:
```typescript
interface Item {
  id: number;
  title: string;
  description: string;
  status: 'found' | 'lost' | 'claimed' | 'archived' | 'recovered' | 'removed';
  location: string;
  image_path?: string;
  category: {
    name: string;
    color: string;
  };
  created_at: string;
  isOffline?: boolean;
}
```

### 2. Update Status Display
Update the status display logic in all components that show item statuses:

In `mobile-app/src/screens/HomeScreen.tsx` and other screens:
```typescript
// Update status badge rendering
const getStatusColor = (status: string) => {
  switch (status) {
    case 'found':
      return '#4CAF50'; // Green
    case 'lost':
      return '#FF9800'; // Orange
    case 'claimed':
      return '#2196F3'; // Blue
    case 'archived':
      return '#9E9E9E'; // Gray
    case 'recovered':
      return '#3F51B5'; // Indigo
    case 'removed':
      return '#F44336'; // Red
    default:
      return '#9E9E9E'; // Gray
  }
};

const getStatusText = (status: string) => {
  switch (status) {
    case 'found':
      return 'Found';
    case 'lost':
      return 'Lost';
    case 'claimed':
      return 'Claimed';
    case 'archived':
      return 'Archived';
    case 'recovered':
      return 'Recovered';
    case 'removed':
      return 'Removed';
    default:
      return status.charAt(0).toUpperCase() + status.slice(1);
  }
};
```

### 3. Update Item Detail Screen
Update `mobile-app/src/screens/ItemDetailScreen.tsx` to properly display the new statuses:

```typescript
// In the status chip rendering
<Chip
  mode="outlined"
  style={[
    styles.statusChip,
    { 
      backgroundColor: getStatusColor(item.status)
    }
  ]}
  textStyle={{ color: 'white' }}
>
  {getStatusText(item.status)}
</Chip>
```

### 4. Update API Service
Update the API service to handle the new statuses:

In `mobile-app/src/services/apiService.ts`:
```typescript
// Update any status-related API calls to handle new statuses
// For example, when filtering items by status
const getItemsByStatus = async (status: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/items?status=${status}`);
    const data = await response.json();
    return { success: response.ok, data };
  } catch (error) {
    console.error('API Error:', error);
    return { success: false, error };
  }
};
```

### 5. Update Database Service
Update the database service to handle the new statuses:

In `mobile-app/src/services/databaseService.ts`:
```typescript
// Update any database queries that filter by status
const getItemsByStatus = async (status: string) => {
  try {
    const items = await database.getItems({
      where: [{ field: 'status', value: status }]
    });
    return items;
  } catch (error) {
    console.error('Database Error:', error);
    return [];
  }
};
```

### 6. Update Search Functionality
Update the search functionality to include the new statuses:

In `mobile-app/src/context/DataContext.tsx`:
```typescript
const searchItems = async (query: string, status?: string) => {
  try {
    // Update search to handle new statuses
    const results = await database.searchItems(query, status);
    return results;
  } catch (error) {
    console.error('Search Error:', error);
    return [];
  }
};
```

### 7. Update Admin Functionality
If the mobile app includes admin functionality, update it to handle the new statuses:

```typescript
// Add functions to update item statuses
const updateItemStatus = async (itemId: number, newStatus: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/items/${itemId}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify({ status: newStatus })
    });
    
    if (response.ok) {
      // Update local database
      await database.updateItem(itemId, { status: newStatus });
      return { success: true };
    } else {
      return { success: false, error: 'Failed to update status' };
    }
  } catch (error) {
    console.error('Update Status Error:', error);
    return { success: false, error };
  }
};
```

### 8. Update UI Components
Update any UI components that display item statuses:

In components that show item lists:
```typescript
// Update item list rendering to show new statuses
{items.map(item => (
  <View key={item.id} style={styles.itemCard}>
    <Text style={styles.itemTitle}>{item.title}</Text>
    <Chip
      mode="outlined"
      style={[
        styles.statusChip,
        { 
          backgroundColor: getStatusColor(item.status)
        }
      ]}
      textStyle={{ color: 'white' }}
    >
      {getStatusText(item.status)}
    </Chip>
    {/* Other item details */}
  </View>
))}
```

### 9. Update Filtering Options
Update any filtering options to include the new statuses:

```typescript
// Update status filter options
const statusOptions = [
  { label: 'All', value: '' },
  { label: 'Found', value: 'found' },
  { label: 'Lost', value: 'lost' },
  { label: 'Recovered', value: 'recovered' },
  { label: 'Removed', value: 'removed' },
  { label: 'Claimed', value: 'claimed' },
  { label: 'Archived', value: 'archived' }
];
```

### 10. Update Offline Sync
Update offline sync functionality to handle the new statuses:

In `mobile-app/src/services/syncService.ts`:
```typescript
// Update sync logic to handle new statuses
const syncItems = async () => {
  try {
    // Get local items that need syncing
    const localItems = await database.getUnsyncedItems();
    
    // Sync each item
    for (const item of localItems) {
      // Handle status updates
      if (item.status === 'recovered' || item.status === 'removed') {
        // Special handling for new statuses if needed
        await syncItemWithSpecialStatus(item);
      } else {
        await syncRegularItem(item);
      }
    }
    
    return { success: true };
  } catch (error) {
    console.error('Sync Error:', error);
    return { success: false, error };
  }
};
```

## Benefits of These Updates
1. Mobile app properly displays all item statuses
2. Consistent status representation across web and mobile
3. Better user experience with clear status indicators
4. Support for enhanced item lifecycle management

## Testing
After implementing these changes:
1. Test that all statuses display correctly in the mobile app
2. Verify that status filtering works properly
3. Check that offline functionality works with new statuses
4. Ensure that API calls handle new statuses correctly
5. Test admin functionality if applicable