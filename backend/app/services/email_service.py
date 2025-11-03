# 邮件发送服务
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import List
import os
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """邮件发送服务"""
    
    @staticmethod
    def send_email(
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: str = None
    ) -> bool:
        """
        发送邮件
        
        Args:
            to_emails: 收件人邮箱列表（支持多个，逗号分隔）
            subject: 邮件主题
            html_content: HTML格式的邮件内容
            text_content: 纯文本格式的邮件内容（可选）
        
        Returns:
            bool: 发送是否成功
        """
        try:
            # 获取邮件配置
            smtp_host = os.getenv('MAIL_SERVER', 'smtp.163.com')
            smtp_port = int(os.getenv('MAIL_PORT', '465'))
            smtp_user = os.getenv('MAIL_USERNAME', '')
            smtp_password = os.getenv('MAIL_PASSWORD', '')
            mail_default_sender = os.getenv('MAIL_DEFAULT_SENDER', '')
            
            # 解析发件人信息（可能是 "名称 <email>" 格式或只有邮箱）
            if mail_default_sender:
                if '<' in mail_default_sender and '>' in mail_default_sender:
                    # 格式: "名称 <email@example.com>"
                    parts = mail_default_sender.split('<')
                    smtp_from_name = parts[0].strip().strip('"').strip("'")
                    smtp_from = parts[1].strip().strip('>')
                else:
                    # 只有邮箱地址
                    smtp_from = mail_default_sender
                    smtp_from_name = os.getenv('MAIL_FROM_NAME', 'ExamSphere系统')
            else:
                smtp_from = smtp_user
                smtp_from_name = os.getenv('MAIL_FROM_NAME', 'ExamSphere系统')
            
            if not smtp_user or not smtp_password:
                logger.warning('邮件配置不完整，跳过发送邮件（MAIL_USERNAME或MAIL_PASSWORD未设置）')
                return False
            
            if not smtp_from:
                logger.warning('发件人邮箱未配置，使用MAIL_USERNAME')
                smtp_from = smtp_user
            
            logger.info(f'准备发送邮件: 服务器={smtp_host}:{smtp_port}, 发件人={smtp_from}, 收件人={to_emails}')
            
            # 创建邮件消息
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{smtp_from_name} <{smtp_from}>"
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 处理收件人列表（支持逗号分隔的字符串或列表）
            if isinstance(to_emails, str):
                to_emails = [email.strip() for email in to_emails.split(',')]
            else:
                to_emails = [email.strip() for email in to_emails if email.strip()]
            
            msg['To'] = ', '.join(to_emails)
            
            # 添加纯文本内容（如果提供）
            if text_content:
                part1 = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(part1)
            
            # 添加HTML内容
            part2 = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part2)
            
            # 根据端口选择连接方式
            # 465端口使用SSL，587端口使用STARTTLS
            if smtp_port == 465:
                # 使用SSL连接
                logger.info('使用SSL连接发送邮件')
                with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg, from_addr=smtp_from, to_addrs=to_emails)
            else:
                # 使用STARTTLS连接
                logger.info('使用STARTTLS连接发送邮件')
                with smtplib.SMTP(smtp_host, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg, from_addr=smtp_from, to_addrs=to_emails)
            
            logger.info(f'邮件发送成功: {subject} -> {", ".join(to_emails)}')
            return True
            
        except Exception as e:
            logger.error(f'邮件发送失败: {str(e)}', exc_info=True)
            logger.error(f'邮件配置: 服务器={os.getenv("MAIL_SERVER")}, 端口={os.getenv("MAIL_PORT")}, 用户={os.getenv("MAIL_USERNAME")}')
            return False
    
    @staticmethod
    def send_course_application_email(
        user_info: dict,
        course_name: str,
        course_info: dict = None
    ) -> bool:
        """
        发送课程申请邮件
        
        Args:
            user_info: 用户信息字典，包含 username, email, real_name 等
            course_name: 课程名称
            course_info: 课程详细信息（可选）
        
        Returns:
            bool: 发送是否成功
        """
        try:
            # 获取收件人邮箱列表（从系统配置或环境变量）
            recipient_emails_str = os.getenv('COURSE_APPLICATION_RECIPIENTS', '')
            if not recipient_emails_str:
                logger.warning('未配置课程申请邮件收件人，跳过发送')
                return False
            
            # 解析收件人列表（支持逗号分隔）
            if isinstance(recipient_emails_str, str):
                recipient_emails = [email.strip() for email in recipient_emails_str.split(',') if email.strip()]
            else:
                recipient_emails = recipient_emails_str
            
            if not recipient_emails:
                logger.warning('收件人列表为空，跳过发送')
                return False
            
            logger.info(f'课程申请邮件收件人: {", ".join(recipient_emails)}')
            
            # 构建邮件主题
            subject = f'【ExamSphere】新课程申请通知 - {course_name}'
            
            # 构建邮件内容
            user_name = user_info.get('real_name') or user_info.get('username', '未知用户')
            user_email = user_info.get('email', '未知邮箱')
            user_phone = user_info.get('phone', '未填写')
            username = user_info.get('username', '未知')
            
            # HTML格式的邮件内容
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #e0e0e0; }}
                    .info-section {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #667eea; }}
                    .info-row {{ margin: 10px 0; }}
                    .info-label {{ font-weight: bold; color: #666; min-width: 100px; display: inline-block; }}
                    .info-value {{ color: #333; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>课程申请通知</h2>
                    </div>
                    <div class="content">
                        <p>您好，</p>
                        <p>系统收到一个新的课程申请，详细信息如下：</p>
                        
                        <div class="info-section">
                            <h3 style="margin-top: 0; color: #667eea;">申请人信息</h3>
                            <div class="info-row">
                                <span class="info-label">用户名：</span>
                                <span class="info-value">{username}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">姓名：</span>
                                <span class="info-value">{user_name}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">邮箱：</span>
                                <span class="info-value">{user_email}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">电话：</span>
                                <span class="info-value">{user_phone}</span>
                            </div>
                        </div>
                        
                        <div class="info-section">
                            <h3 style="margin-top: 0; color: #667eea;">申请课程信息</h3>
                            <div class="info-row">
                                <span class="info-label">课程名称：</span>
                                <span class="info-value"><strong>{course_name}</strong></span>
                            </div>
            """
            
            if course_info:
                course_code = course_info.get('code', '未知')
                course_price = course_info.get('price', 0)
                course_description = course_info.get('description', '无')
                
                html_content += f"""
                            <div class="info-row">
                                <span class="info-label">课程代码：</span>
                                <span class="info-value">{course_code}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">课程价格：</span>
                                <span class="info-value">¥{course_price}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">课程描述：</span>
                                <span class="info-value">{course_description}</span>
                            </div>
                """
            
            html_content += """
                        </div>
                        
                        <p style="margin-top: 20px;">请登录系统后台处理该申请。</p>
                        <p>此邮件由系统自动发送，请勿回复。</p>
                    </div>
                    <div class="footer">
                        <p>ExamSphere 考试管理系统</p>
                        <p>© 2024 ExamSphere. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # 纯文本格式（作为备选）
            text_content = f"""
课程申请通知

您好，

系统收到一个新的课程申请，详细信息如下：

申请人信息：
- 用户名：{username}
- 姓名：{user_name}
- 邮箱：{user_email}
- 电话：{user_phone}

申请课程信息：
- 课程名称：{course_name}
"""
            
            if course_info:
                text_content += f"""
- 课程代码：{course_info.get('code', '未知')}
- 课程价格：¥{course_info.get('price', 0)}
- 课程描述：{course_info.get('description', '无')}
"""
            
            text_content += """

请登录系统后台处理该申请。

此邮件由系统自动发送，请勿回复。

ExamSphere 考试管理系统
© 2025 ExamSphere. All rights reserved.
"""
            
            # 发送邮件（传递列表格式）
            return EmailService.send_email(
                to_emails=recipient_emails,  # 已经是列表格式
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f'发送课程申请邮件失败: {str(e)}', exc_info=True)
            return False


