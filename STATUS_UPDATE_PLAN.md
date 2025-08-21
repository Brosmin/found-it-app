# Adding New Item Statuses: 'recovered' and 'removed'

## Current Statuses
The current Item model in `app.py` has the following statuses:
- 'found' (default)
- 'lost'
- 'claimed'
- 'archived'

## New Statuses to Add
1. 'recovered' - For items that have been successfully recovered by their owners
2. 'removed' - For items that don't meet the standard and have been removed by admins

## Implementation Plan

### 1. Update Item Model
In `app.py`, update the Item model's status field comment to include the new statuses:

```python
class Item(db.Model):
    # ... other fields ...
    status = db.Column(db.String(20), default='found')  # found, lost, claimed, archived, recovered, removed
    # ... other fields ...
```

### 2. Update Status Filtering in Routes
Update the routes that filter items by status to include the new 'recovered' status for public views:

In the `home()` route:
```python
# Only show active items (found/lost/recovered) on public pages
items = Item.query.filter(
    Item.is_approved == True,
    Item.status.in_(['found', 'lost', 'recovered'])
).order_by(Item.created_at.desc()).limit(10).all()
```

In the `items()` route:
```python
# Only show active items (found/lost/recovered) on public pages
query = Item.query.filter(
    Item.is_approved == True,
    Item.status.in_(['found', 'lost', 'recovered'])
)
```

### 3. Update Templates
Update the templates to handle the new statuses:

In `templates/public/items.html` and `templates/public/home.html`:
```html
<span class="badge {% if item.status == 'found' %}bg-success{% elif item.status == 'lost' %}bg-warning{% elif item.status == 'recovered' %}bg-info{% else %}bg-secondary{% endif %} status-badge">
    {{ item.status.title() }}
</span>
```

In `templates/admin/dashboard.html`:
```html
<span class="badge {% if item.status == 'found' %}bg-success{% elif item.status == 'lost' %}bg-warning{% elif item.status == 'recovered' %}bg-info{% elif item.status == 'removed' %}bg-secondary{% else %}bg-info{% endif %}">
    {{ item.status.title() }}
</span>
```

### 4. Add Admin Functionality for New Statuses
Add new admin routes to handle setting items to 'recovered' and 'removed' statuses:

```python
@app.route('/admin/items/recover/<int:id>')
@login_required
def recover_item(id):
    """Mark an item as recovered"""
    item = Item.query.get_or_404(id)
    item.status = 'recovered'
    item.updated_at = datetime.utcnow()
    db.session.commit()
    flash('Item marked as recovered successfully!', 'success')
    return redirect(url_for('admin_items'))

@app.route('/admin/items/remove/<int:id>')
@login_required
def remove_item(id):
    """Mark an item as removed"""
    item = Item.query.get_or_404(id)
    item.status = 'removed'
    item.updated_at = datetime.utcnow()
    db.session.commit()
    flash('Item removed successfully!', 'success')
    return redirect(url_for('admin_items'))
```

### 5. Update Admin Templates
Add buttons in the admin interface to set items to the new statuses:

In `templates/admin/items.html`:
```html
<!-- Add these buttons in the item action section -->
{% if item.status in ['found', 'lost'] %}
<div class="mt-2">
    <a href="{{ url_for('recover_item', id=item.id) }}" 
       class="btn btn-sm btn-info"
       onclick="return confirm('Mark this item as recovered?')">
        <i class="fas fa-undo me-1"></i>Recover
    </a>
    <a href="{{ url_for('remove_item', id=item.id) }}" 
       class="btn btn-sm btn-secondary"
       onclick="return confirm('Remove this item? This action cannot be undone.')">
        <i class="fas fa-trash me-1"></i>Remove
    </a>
</div>
{% endif %}
```

### 6. Update Analytics
Update the analytics to include the new statuses:

In the `Analytics` model, add new fields:
```python
class Analytics(db.Model):
    # ... existing fields ...
    recovered_items = db.Column(db.Integer, default=0)
    removed_items = db.Column(db.Integer, default=0)
    # ... existing fields ...
```

In the `update_analytics()` function:
```python
def update_analytics():
    # ... existing code ...
    analytics.recovered_items = Item.query.filter_by(status='recovered').count()
    analytics.removed_items = Item.query.filter_by(status='removed').count()
```

### 7. Update Admin Dashboard
Update the admin dashboard to show statistics for the new statuses:

In `templates/admin/dashboard.html`, add new statistic cards:
```html
<div class="col-xl-3 col-md-6 mb-4">
    <div class="card stats-card border-0 shadow h-100 py-2">
        <div class="card-body">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-white-50 text-uppercase mb-1">
                        Recovered Items
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-white">{{ recovered_items }}</div>
                </div>
                <div class="col-auto">
                    <i class="fas fa-undo fa-2x text-white-50"></i>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="col-xl-3 col-md-6 mb-4">
    <div class="card stats-card border-0 shadow h-100 py-2">
        <div class="card-body">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-white-50 text-uppercase mb-1">
                        Removed Items
                    </div>
                    <div class="h5 mb-0 font-weight-bold text-white">{{ removed_items }}</div>
                </div>
                <div class="col-auto">
                    <i class="fas fa-trash fa-2x text-white-50"></i>
                </div>
            </div>
        </div>
    </div>
</div>
```

### 8. Update Admin Dashboard Route
Update the admin dashboard route to include the new statistics:

In the `admin_dashboard()` function:
```python
# Basic statistics
# ... existing code ...
recovered_items = Item.query.filter_by(status='recovered').count()
removed_items = Item.query.filter_by(status='removed').count()

return render_template('admin/dashboard.html', 
                     # ... existing variables ...
                     recovered_items=recovered_items,
                     removed_items=removed_items,
                     # ... existing variables ...)
```

## Benefits of New Statuses
1. 'recovered' status allows users to see items that have been successfully returned to their owners
2. 'removed' status helps admins manage items that don't meet the platform's standards
3. Better item lifecycle management and tracking
4. Improved user experience with clearer status information

## Testing
After implementing these changes:
1. Test that items can be set to 'recovered' and 'removed' statuses
2. Verify that the new statuses are displayed correctly in all views
3. Check that analytics are updated properly
4. Ensure that the new admin functionality works as expected