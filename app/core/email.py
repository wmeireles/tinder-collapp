import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger(__name__)

def send_password_reset_email(email: str, reset_token: str):
    """
    Envia email de reset de senha
    """
    try:
        # Configurações de email (usar variáveis de ambiente em produção)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("SMTP_EMAIL", "noreply@collapp.com")
        sender_password = os.getenv("SMTP_PASSWORD", "")
        
        if not sender_password:
            logger.warning("SMTP_PASSWORD não configurado, email não será enviado")
            return False
        
        # Criar mensagem
        message = MIMEMultipart("alternative")
        message["Subject"] = "Redefinir sua senha - Collapp"
        message["From"] = sender_email
        message["To"] = email
        
        # URL de reset (ajustar para produção)
        reset_url = f"https://collapp-frontend.onrender.com/auth/reset-password?token={reset_token}"
        
        # HTML do email
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
              <h1 style="color: white; margin: 0;">Collapp</h1>
            </div>
            
            <div style="padding: 30px; background: #f8f9fa;">
              <h2 style="color: #333;">Redefinir sua senha</h2>
              
              <p style="color: #666; line-height: 1.6;">
                Você solicitou a redefinição da sua senha no Collapp. 
                Clique no botão abaixo para criar uma nova senha:
              </p>
              
              <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; 
                          padding: 15px 30px; 
                          text-decoration: none; 
                          border-radius: 8px; 
                          display: inline-block;
                          font-weight: bold;">
                  Redefinir Senha
                </a>
              </div>
              
              <p style="color: #999; font-size: 14px;">
                Este link expira em 1 hora por segurança.
              </p>
              
              <p style="color: #999; font-size: 14px;">
                Se você não solicitou esta redefinição, pode ignorar este email.
              </p>
            </div>
            
            <div style="background: #333; color: #999; padding: 20px; text-align: center; font-size: 12px;">
              <p>© 2025 Collapp. Todos os direitos reservados.</p>
            </div>
          </body>
        </html>
        """
        
        # Anexar HTML
        html_part = MIMEText(html, "html")
        message.attach(html_part)
        
        # Enviar email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        
        logger.info(f"Email de reset enviado para: {email}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar email: {e}")
        return False

def send_welcome_email(email: str, name: str):
    """
    Envia email de boas-vindas
    """
    # Implementar se necessário
    pass