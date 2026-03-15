# Public endpoint for Bhiksha Vandanam statistics (no auth required)
from flask import Blueprint, jsonify
import db

bv_stats_bp = Blueprint('bv_stats', __name__)

@bv_stats_bp.route('/api/bv-statistics', methods=['GET'])
def get_bv_statistics():
    """
    Public API endpoint to fetch Bhiksha Vandanam event statistics
    Returns: JSON with event data (Event ID, Amount, Members, Women, Men)
    """
    try:
        query = """
            SELECT
                bvcr.EVENT_ID as Event,
                sum(bvcr.Amount) as Amount,
                count(distinct bvcr.Member_ID) as Members,
                SUM(CASE WHEN bvcr.Gender = 'F' THEN 1 ELSE 0 END) as Women,
                SUM(CASE WHEN bvcr.Gender LIKE 'M' THEN 1 ELSE 0 END) as Men
            FROM
                bspdhyd_wp1.BSPD_View_Contribution_Report bvcr
            WHERE bvcr.EVENT_ID LIKE 'BVCY%'
            GROUP BY
                bvcr.EVENT_ID
            ORDER BY 1 
        """
        results = db.run_fetchall_query(query, ())
        statistics = []
        for row in results:
            statistics.append({
                'event': row['Event'],
                'amount': float(row['Amount']) if row['Amount'] else 0,
                'members': int(row['Members']) if row['Members'] else 0,
                'women': int(row['Women']) if row['Women'] else 0,
                'men': int(row['Men']) if row['Men'] else 0
            })
        return jsonify({'success': True, 'data': statistics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
