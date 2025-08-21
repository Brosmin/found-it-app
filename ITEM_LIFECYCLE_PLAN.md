# Item Lifecycle Management Enhancement Plan

## Current Item Lifecycle
The current item lifecycle in the FOUND IT app has the following statuses:
- 'found' (default) - Item found by someone
- 'lost' - Item reported as lost
- 'claimed' - Item claimed by owner
- 'archived' - Item archived (found by owner or claimed)

## Enhanced Item Lifecycle
The enhanced lifecycle will include:
- 'found' - Item found by someone
- 'lost' - Item reported as lost
- 'recovered' - Item successfully recovered by owner
- 'claimed' - Item claimed by owner (pending admin approval)
- 'removed' - Item removed by admin (doesn't meet standards)
- 'archived' - Item archived (final state)

## Lifecycle Flow

### Found Items Flow
```
found → claimed → approved → archived
found → recovered
found → removed
```

### Lost Items Flow
```
lost → claimed → approved → archived
lost → recovered
lost → removed
```

## Implementation Plan

### 1. Update Status Transitions
Define clear rules for status transitions:

1. Items in 'found' or 'lost' status can be:
   - Claimed (moves to 'claimed' status)
   - Marked as 'recovered'
   - Marked as 'removed'

2. Items in 'claimed' status can be:
   - Approved (moves to 'archived' status)
   - Rejected (returns to original status - 'found' or 'lost')

3. Items in 'recovered' status:
   - Final state, no further transitions

4. Items in 'removed' status:
   - Final state, no further transitions

5. Items in 'archived' status:
   - Final state, no further transitions

### 2. Add Status History Tracking
Add a new model to track status changes:

```python
class ItemStatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    from_status = db.Column(db.String(20))
    to_status = db.Column(db.String(20))
    changed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relationships
    item = db.relationship('Item', backref='status_history')
    user = db.relationship('User', backref='status_changes')
```

### 3. Add Status Change Function
Add a helper function to handle status changes with history tracking:

```python
def change_item_status(item_id, new_status, user_id=None, notes=None):
    """Change item status and record history"""
    item = Item.query.get_or_404(item_id)
    old_status = item.status
    item.status = new_status
    item.updated_at = datetime.utcnow()
    
    # Record status change
    history = ItemStatusHistory(
        item_id=item_id,
        from_status=old_status,
        to_status=new_status,
        changed_by=user_id,
        notes=notes
    )
    db.session.add(history)
    db.session.commit()
    
    return history
```

### 4. Update Admin Interface
Add a status history view in the admin panel:

```python
@app.route('/admin/items/<int:item_id>/history')
@login_required
def item_history(item_id):
    """View item status history"""
    item = Item.query.get_or_404(item_id)
    history = ItemStatusHistory.query.filter_by(item_id=item_id).order_by(ItemStatusHistory.changed_at.desc()).all()
    return render_template('admin/item_history.html', item=item, history=history)
```

### 5. Add Status History Template
Create `templates/admin/item_history.html` to display the status history:

```html
{% extends "admin/base.html" %}

{% block admin_title %}Item Status History{% endblock %}

{% block admin_content %}
<div class="row">
    <div class="col-12">
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Status History for "{{ item.title }}"</h6>
            </div>
            <div class="card-body">
                {% if history %}
                <div class="table-responsive">
                    <table class="table table-bordered" width="100%" cellspacing="0">
                        <thead>
                            <tr>
                                <th>Date/Time</th>
                                <th>Status Change</th>
                                <th>Changed By</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for record in history %}
                            <tr>
                                <td>{{ record.changed_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                                <td>
                                    <span class="badge bg-secondary">{{ record.from_status or 'N/A' }}</span>
                                    →
                                    <span class="badge bg-primary">{{ record.to_status }}</span>
                                </td>
                                <td>{{ record.user.username if record.user else 'System' }}</td>
                                <td>{{ record.notes or 'N/A' }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <div class="text-center py-4">
                    <i class="fas fa-history fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">No status history found</h5>
                    <p class="text-muted">This item has not had any status changes yet.</p>
                </div>
                {% endif %}
                
                <div class="mt-3">
                    <a href="{{ url_for('admin_items') }}" class="btn btn-secondary">
                        <i class="fas fa-arrow-left me-1"></i>Back to Items
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6. Update Item Detail View
Add a link to view status history in the item detail view:

In `templates/admin/edit_item.html` or a new item detail template:
```html
<a href="{{ url_for('item_history', item_id=item.id) }}" class="btn btn-info btn-sm">
    <i class="fas fa-history me-1"></i>View History
</a>
```

### 7. Add Status Summary Dashboard
Enhance the admin dashboard to show status distribution:

In `admin_dashboard()` function:
```python
# Status distribution
status_distribution = {
    'found': Item.query.filter_by(status='found').count(),
    'lost': Item.query.filter_by(status='lost').count(),
    'claimed': Item.query.filter_by(status='claimed').count(),
    'archived': Item.query.filter_by(status='archived').count(),
    'recovered': Item.query.filter_by(status='recovered').count(),
    'removed': Item.query.filter_by(status='removed').count()
}
```

In `templates/admin/dashboard.html`:
```html
<div class="row">
    <div class="col-12">
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Item Status Distribution</h6>
            </div>
            <div class="card-body">
                <div class="row">
                    {% for status, count in status_distribution.items() %}
                    <div class="col-md-2 mb-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title">{{ count }}</h5>
                                <p class="card-text">
                                    <span class="badge {% if status == 'found' %}bg-success{% elif status == 'lost' %}bg-warning{% elif status == 'claimed' %}bg-info{% elif status == 'archived' %}bg-secondary{% elif status == 'recovered' %}bg-primary{% elif status == 'removed' %}bg-danger{% endif %}">
                                        {{ status.title() }}
                                    </span>
                                </p>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
```

## Benefits of Enhanced Lifecycle Management
1. Clear status transitions with defined rules
2. Complete audit trail of all status changes
3. Better visibility into item lifecycle
4. Improved admin oversight and control
5. Enhanced reporting capabilities

## Testing
After implementing these changes:
1. Test all status transitions work correctly
2. Verify status history is recorded properly
3. Check that the dashboard displays status distribution accurately
4. Ensure all admin functions work as expected