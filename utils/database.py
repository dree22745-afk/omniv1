# utils/database.py

import json
import os
import hashlib
from datetime import datetime

class Database:
    """Database Manager for User Management"""
    
    @staticmethod
    def hash_password(password):
        """Hash password with SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def get_users():
        """Get all users from database"""
        try:
            users_db = os.environ.get('USERS_DB', '{}')
            return json.loads(users_db)
        except:
            return {}
    
    @staticmethod
    def save_users(users_dict):
        """Save users to database"""
        os.environ['USERS_DB'] = json.dumps(users_dict)
    
    @staticmethod
    def get_user(email):
        """Get single user by email"""
        users = Database.get_users()
        return users.get(email, None)
    
    @staticmethod
    def create_user(email, password):
        """Create new user"""
        users = Database.get_users()
        
        if email in users:
            return False, "User already exists!"
        
        users[email] = {
            "email": email,
            "password": Database.hash_password(password),
            "role": "user",
            "status": "pending",
            "credits": 0,
            "joined_date": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "videos_created": [],
            "last_login": None
        }
        
        Database.save_users(users)
        return True, "Account created successfully! Pending admin approval."
    
    @staticmethod
    def verify_login(email, password):
        """Verify user login"""
        # Check admin first
        admin_emails = os.environ.get('ADMIN_EMAILS', '').split(',')
        admin_emails = [e.strip() for e in admin_emails]
        admin_password = os.environ.get('ADMIN_PASSWORD', '')
        
        if email in admin_emails and password == admin_password:
            return "admin", "Login successful!"
        
        # Check user
        users = Database.get_users()
        if email in users:
            user = users[email]
            if user['password'] == Database.hash_password(password):
                if user['status'] == 'approved':
                    # Update last login
                    users[email]['last_login'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    Database.save_users(users)
                    return "user", "Login successful!"
                elif user['status'] == 'pending':
                    return "pending", "Account pending approval!"
                else:
                    return "rejected", "Account rejected!"
            else:
                return None, "Invalid password!"
        
        return None, "User not found!"
    
    @staticmethod
    def update_status(email, status):
        """Update user status (approve/reject)"""
        users = Database.get_users()
        if email in users:
            users[email]['status'] = status
            if status == 'approved':
                users[email]['credits'] = 50  # Welcome credits
            Database.save_users(users)
            return True
        return False
    
    @staticmethod
    def add_credits(email, amount):
        """Add credits to user"""
        users = Database.get_users()
        if email in users:
            users[email]['credits'] += amount
            Database.save_users(users)
            return True, users[email]['credits']
        return False, 0
    
    @staticmethod
    def deduct_credits(email, amount):
        """Deduct credits from user"""
        users = Database.get_users()
        if email in users:
            if users[email]['credits'] >= amount:
                users[email]['credits'] -= amount
                Database.save_users(users)
                return True, users[email]['credits']
            return False, users[email]['credits']
        return False, 0
    
    @staticmethod
    def remove_user(email):
        """Remove user"""
        users = Database.get_users()
        if email in users:
            del users[email]
            Database.save_users(users)
            return True
        return False
    
    @staticmethod
    def add_video_to_history(email, video_data):
        """Add video to user's history"""
        users = Database.get_users()
        if email in users:
            video_data['created_at'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            users[email]['videos_created'].append(video_data)
            Database.save_users(users)
            return True
        return False
    
    @staticmethod
    def get_pending_users():
        """Get all pending users"""
        users = Database.get_users()
        return {email: data for email, data in users.items() if data['status'] == 'pending'}
    
    @staticmethod
    def get_approved_users():
        """Get all approved users"""
        users = Database.get_users()
        return {email: data for email, data in users.items() if data['status'] == 'approved'}
    
    @staticmethod
    def get_stats():
        """Get system statistics"""
        users = Database.get_users()
        total = len(users)
        pending = len([u for u in users.values() if u['status'] == 'pending'])
        approved = len([u for u in users.values() if u['status'] == 'approved'])
        rejected = len([u for u in users.values() if u['status'] == 'rejected'])
        total_videos = sum([len(u.get('videos_created', [])) for u in users.values()])
        total_credits = sum([u.get('credits', 0) for u in users.values()])
        
        return {
            "total_users": total,
            "pending_users": pending,
            "approved_users": approved,
            "rejected_users": rejected,
            "total_videos": total_videos,
            "total_credits": total_credits
        }