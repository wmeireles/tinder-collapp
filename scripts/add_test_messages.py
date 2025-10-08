#!/usr/bin/env python3
"""
Script para adicionar mensagens de teste
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import User, Chat, Message, WantedPost, WantedApplication
from datetime import datetime
import uuid

def add_test_messages():
    db = SessionLocal()
    
    try:
        # Find demo user
        demo_user = db.query(User).filter(User.email == "demo@collapp.com").first()
        if not demo_user:
            print("Demo user not found")
            return
        
        # Find any chat
        chat = db.query(Chat).first()
        if not chat:
            print("No chat found")
            return
        
        print(f"Adding messages to chat {chat.id}")
        
        # Add test messages
        messages = [
            {
                "content": "Oi! Vi seu post sobre colaboração de lifestyle. Tenho interesse!",
                "sender_id": demo_user.id,
                "message_type": "text"
            },
            {
                "content": "Olá! Que bom que se interessou. Podemos conversar sobre os detalhes?",
                "sender_id": demo_user.id,  # For now, same user
                "message_type": "text"
            },
            {
                "content": "Claro! Qual seria o formato da colaboração?",
                "sender_id": demo_user.id,
                "message_type": "text"
            }
        ]
        
        for msg_data in messages:
            message = Message(
                chat_id=chat.id,
                sender_id=msg_data["sender_id"],
                content=msg_data["content"],
                message_type=msg_data["message_type"],
                created_at=datetime.utcnow()
            )
            db.add(message)
        
        db.commit()
        print("✅ Test messages added successfully!")
        
        # Show messages
        all_messages = db.query(Message).filter(Message.chat_id == chat.id).all()
        print(f"Total messages in chat: {len(all_messages)}")
        for msg in all_messages:
            print(f"- {msg.content}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error adding test messages: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Adding test messages...")
    add_test_messages()
    print("🎉 Done!")