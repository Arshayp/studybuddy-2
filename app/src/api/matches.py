from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from app.src.database import db
from app.src.models import Match

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/api/matches/total', methods=['GET'])
def get_total_matches():
    try:
        # Calculate date 30 days ago
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # Query total matches in the last 30 days
        total_matches = Match.query.filter(
            Match.created_at >= thirty_days_ago
        ).count()
        
        return jsonify({
            'total_matches': total_matches,
            'time_period': 'Last 30 days'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'total_matches': 0,
            'time_period': 'Error fetching data'
        }), 500

@matches_bp.route('/api/analytics/retention', methods=['GET'])
def get_retention_rate():
    try:
        # TODO: Replace with actual retention calculation
        # For now, returning a mock response
        return jsonify({
            'retention_rate': 86,
            'change': '+3% vs last month'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'retention_rate': 0,
            'change': 'Error fetching data'
        }), 500 