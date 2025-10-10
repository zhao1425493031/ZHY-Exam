from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.models.exam_monitoring import ExamMonitoring
from app.models.exam_record import ExamRecord
from app.models.exam import Exam
from app.models.user import User
from app import db
import json
import logging

logger = logging.getLogger(__name__)

class ExamMonitoringService:
    """考试监控服务"""
    
    @staticmethod
    def record_event(event_data: Dict[str, Any]) -> Dict[str, Any]:
        """记录考试监控事件"""
        try:
            # 创建监控记录
            monitoring = ExamMonitoring(
                exam_record_id=event_data['exam_record_id'],
                event_type=event_data['event_type'],
                event_data=event_data.get('event_data', {}),
                ip_address=event_data.get('ip_address', ''),
                user_agent=event_data.get('user_agent', '')
            )
            
            db.session.add(monitoring)
            db.session.commit()
            
            # 检查可疑行为
            ExamMonitoringService._check_suspicious_behavior(monitoring)
            
            return {
                'id': monitoring.id,
                'event_type': monitoring.event_type,
                'created_at': monitoring.created_at.isoformat()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Record event error: {str(e)}')
            raise Exception(f'记录监控事件失败: {str(e)}')
    
    @staticmethod
    def get_exam_events(exam_record_id: int) -> List[Dict[str, Any]]:
        """获取考试监控事件"""
        try:
            events = ExamMonitoring.query.filter_by(exam_record_id=exam_record_id)\
                .order_by(ExamMonitoring.created_at.desc()).all()
            
            return [{
                'id': event.id,
                'event_type': event.event_type,
                'event_data': event.event_data,
                'ip_address': event.ip_address,
                'user_agent': event.user_agent,
                'created_at': event.created_at.isoformat()
            } for event in events]
            
        except Exception as e:
            logger.error(f'Get exam events error: {str(e)}')
            raise Exception(f'获取监控事件失败: {str(e)}')
    
    @staticmethod
    def get_suspicious_behavior(page: int = 1, size: int = 20, 
                               exam_id: Optional[int] = None, 
                               user_id: Optional[int] = None) -> Dict[str, Any]:
        """获取可疑行为记录"""
        try:
            query = ExamMonitoring.query.filter_by(event_type='cheat')
            
            if exam_id:
                query = query.join(ExamRecord).filter(ExamRecord.exam_id == exam_id)
            
            if user_id:
                query = query.join(ExamRecord).filter(ExamRecord.user_id == user_id)
            
            # 分页
            pagination = query.order_by(ExamMonitoring.created_at.desc())\
                .paginate(page=page, per_page=size, error_out=False)
            
            events = []
            for event in pagination.items:
                exam_record = ExamRecord.query.get(event.exam_record_id)
                user = User.query.get(exam_record.user_id) if exam_record else None
                
                events.append({
                    'id': event.id,
                    'exam_record_id': event.exam_record_id,
                    'exam_id': exam_record.exam_id if exam_record else None,
                    'user_id': exam_record.user_id if exam_record else None,
                    'username': user.username if user else '未知用户',
                    'event_data': event.event_data,
                    'ip_address': event.ip_address,
                    'created_at': event.created_at.isoformat()
                })
            
            return {
                'items': events,
                'total': pagination.total,
                'page': page,
                'size': size,
                'pages': pagination.pages
            }
            
        except Exception as e:
            logger.error(f'Get suspicious behavior error: {str(e)}')
            raise Exception(f'获取可疑行为失败: {str(e)}')
    
    @staticmethod
    def get_monitoring_statistics(exam_id: Optional[int] = None,
                                 start_date: Optional[str] = None,
                                 end_date: Optional[str] = None) -> Dict[str, Any]:
        """获取监控统计信息"""
        try:
            query = ExamMonitoring.query
            
            if exam_id:
                query = query.join(ExamRecord).filter(ExamRecord.exam_id == exam_id)
            
            if start_date:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                query = query.filter(ExamMonitoring.created_at >= start_dt)
            
            if end_date:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                query = query.filter(ExamMonitoring.created_at <= end_dt)
            
            # 总事件数
            total_events = query.count()
            
            # 按事件类型统计
            event_types = db.session.query(
                ExamMonitoring.event_type,
                db.func.count(ExamMonitoring.id)
            ).group_by(ExamMonitoring.event_type).all()
            
            event_type_stats = {event_type: count for event_type, count in event_types}
            
            # 可疑行为统计
            suspicious_count = query.filter_by(event_type='cheat').count()
            
            # 按小时统计
            hourly_stats = db.session.query(
                db.func.date_format(ExamMonitoring.created_at, '%H'),
                db.func.count(ExamMonitoring.id)
            ).group_by(db.func.date_format(ExamMonitoring.created_at, '%H')).all()
            
            hourly_data = {hour: count for hour, count in hourly_stats}
            
            return {
                'total_events': total_events,
                'event_type_stats': event_type_stats,
                'suspicious_count': suspicious_count,
                'suspicious_rate': round(suspicious_count / total_events * 100, 2) if total_events > 0 else 0,
                'hourly_stats': hourly_data
            }
            
        except Exception as e:
            logger.error(f'Get monitoring statistics error: {str(e)}')
            raise Exception(f'获取监控统计失败: {str(e)}')
    
    @staticmethod
    def get_real_time_monitoring(exam_id: int) -> Dict[str, Any]:
        """获取实时监控数据"""
        try:
            # 获取正在进行的考试记录
            ongoing_records = ExamRecord.query.filter(
                ExamRecord.exam_id == exam_id,
                ExamRecord.status == 'in_progress'
            ).all()
            
            # 实时统计
            real_time_stats = {
                'total_participants': len(ongoing_records),
                'active_participants': 0,
                'suspicious_activities': 0,
                'recent_events': []
            }
            
            # 获取最近5分钟的事件
            five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
            recent_events = ExamMonitoring.query.join(ExamRecord)\
                .filter(ExamRecord.exam_id == exam_id)\
                .filter(ExamMonitoring.created_at >= five_minutes_ago)\
                .order_by(ExamMonitoring.created_at.desc())\
                .limit(10).all()
            
            for event in recent_events:
                exam_record = ExamRecord.query.get(event.exam_record_id)
                user = User.query.get(exam_record.user_id) if exam_record else None
                
                real_time_stats['recent_events'].append({
                    'id': event.id,
                    'event_type': event.event_type,
                    'username': user.username if user else '未知用户',
                    'event_data': event.event_data,
                    'created_at': event.created_at.isoformat()
                })
                
                if event.event_type == 'cheat':
                    real_time_stats['suspicious_activities'] += 1
            
            # 统计活跃参与者（最近1分钟有活动）
            one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
            active_participants = ExamMonitoring.query.join(ExamRecord)\
                .filter(ExamRecord.exam_id == exam_id)\
                .filter(ExamMonitoring.created_at >= one_minute_ago)\
                .distinct(ExamRecord.user_id).count()
            
            real_time_stats['active_participants'] = active_participants
            
            return real_time_stats
            
        except Exception as e:
            logger.error(f'Get real-time monitoring error: {str(e)}')
            raise Exception(f'获取实时监控数据失败: {str(e)}')
    
    @staticmethod
    def get_monitoring_alerts(page: int = 1, size: int = 20, 
                             status: str = 'active') -> Dict[str, Any]:
        """获取监控告警"""
        try:
            # 这里可以实现告警系统
            # 目前返回空数据，后续可以扩展
            return {
                'items': [],
                'total': 0,
                'page': page,
                'size': size,
                'pages': 0
            }
            
        except Exception as e:
            logger.error(f'Get monitoring alerts error: {str(e)}')
            raise Exception(f'获取监控告警失败: {str(e)}')
    
    @staticmethod
    def resolve_alert(alert_id: int, resolution_note: str) -> Dict[str, Any]:
        """处理监控告警"""
        try:
            # 这里可以实现告警处理逻辑
            # 目前返回成功状态
            return {
                'id': alert_id,
                'status': 'resolved',
                'resolution_note': resolution_note,
                'resolved_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f'Resolve alert error: {str(e)}')
            raise Exception(f'处理告警失败: {str(e)}')
    
    @staticmethod
    def _check_suspicious_behavior(monitoring: ExamMonitoring):
        """检查可疑行为"""
        try:
            event_type = monitoring.event_type
            event_data = monitoring.event_data
            
            # 检查切屏行为
            if event_type == 'switch_tab' and event_data.get('count', 0) > 3:
                ExamMonitoringService._create_cheat_event(monitoring, '频繁切屏')
            
            # 检查答题时间异常
            if event_type == 'answer_time' and event_data.get('time', 0) < 5:
                ExamMonitoringService._create_cheat_event(monitoring, '答题时间过短')
            
            # 检查IP地址变化
            if event_type == 'ip_change':
                ExamMonitoringService._create_cheat_event(monitoring, 'IP地址变化')
            
        except Exception as e:
            logger.error(f'Check suspicious behavior error: {str(e)}')
    
    @staticmethod
    def _create_cheat_event(original_monitoring: ExamMonitoring, reason: str):
        """创建作弊事件记录"""
        try:
            cheat_event = ExamMonitoring(
                exam_record_id=original_monitoring.exam_record_id,
                event_type='cheat',
                event_data={
                    'reason': reason,
                    'original_event_id': original_monitoring.id,
                    'original_event_type': original_monitoring.event_type
                },
                ip_address=original_monitoring.ip_address,
                user_agent=original_monitoring.user_agent
            )
            
            db.session.add(cheat_event)
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Create cheat event error: {str(e)}')
            db.session.rollback()
