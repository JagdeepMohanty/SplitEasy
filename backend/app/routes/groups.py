from flask import Blueprint, request, jsonify, current_app
from app.models.group import Group
from bson import ObjectId

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/groups', methods=['POST'])
def create_group():
    """Create new group"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Request body is required'}), 400
    
    name = data.get('name', '').strip()
    
    if not name:
        return jsonify({'success': False, 'error': 'Group name is required'}), 400
    
    try:
        if current_app.db is None:
            return jsonify({'error': 'Database not available'}), 503
        
        group_model = Group(current_app.db)
        group_id, group_code = group_model.create_group(name)
        
        return jsonify({
            'success': True,
            'message': 'Group created successfully',
            'data': {
                '_id': str(group_id),
                'name': name,
                'group_code': group_code
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f'Create group error: {e}')
        return jsonify({'success': False, 'error': 'Failed to create group'}), 500


@groups_bp.route('/groups', methods=['GET'])
def get_groups():
    """Get all groups or find by code"""
    group_code = request.args.get('code')
    
    try:
        if current_app.db is None:
            return jsonify({'error': 'Database not available'}), 503
        
        group_model = Group(current_app.db)
        
        if group_code:
            # Find specific group by code
            group = group_model.get_group_by_code(group_code)
            if not group:
                return jsonify({'error': 'Group not found'}), 404
            
            group['_id'] = str(group['_id'])
            group['created_at'] = group['created_at'].isoformat()
            return jsonify(group), 200
        else:
            # Get all groups
            groups = group_model.get_all_groups()
            
            for group in groups:
                group['_id'] = str(group['_id'])
                group['created_at'] = group['created_at'].isoformat()
            
            return jsonify(groups), 200
        
    except Exception as e:
        current_app.logger.error(f'Get groups error: {e}')
        return jsonify({'error': 'Failed to fetch groups'}), 500


@groups_bp.route('/groups/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Delete group and all associated data"""
    try:
        if current_app.db is None:
            return jsonify({'error': 'Database not available'}), 503
        
        # Delete group
        group_model = Group(current_app.db)
        deleted = group_model.delete_group(group_id)
        
        if not deleted:
            return jsonify({'error': 'Group not found'}), 404
        
        # Delete associated data
        current_app.db.expenses.delete_many({'group_id': group_id})
        current_app.db.friends.delete_many({'group_id': group_id})
        current_app.db.settlements.delete_many({'group_id': group_id})
        
        return jsonify({
            'success': True,
            'message': 'Group and associated data deleted successfully'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Delete group error: {e}')
        return jsonify({'error': 'Failed to delete group'}), 500
