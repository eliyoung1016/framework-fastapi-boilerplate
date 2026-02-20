import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from mjml import mjml_to_html

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Jinja2 environment pointing to email templates folder
TEMPLATE_DIR = Path(__file__).parent.parent / "email-templates"
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

def render_email_template(template_name: str, **kwargs) -> str:
    """Renders a Jinja2 MJML template and converts it to HTML."""
    template = env.get_template(template_name)
    mjml_content = template.render(**kwargs)
    result = mjml_to_html(mjml_content)
    return result.html

def send_test_email(email_to: str, subject: str = "", html_content: str = "") -> None:
    # This is a dummy email sender
    logger.info("--- DUMMY EMAIL ---")
    logger.info(f"To: {email_to}")
    logger.info(f"Subject: {subject}")
    logger.info(f"Content: \n{html_content}")
    logger.info("-------------------")

def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    subject = "Password recovery"
    link = f"http://localhost:3000/reset-password?token={token}"
    html_content = render_email_template("reset_password.mjml", email=email, link=link)
    send_test_email(email_to, subject, html_content)

def send_new_account_email(email_to: str, username: str) -> None:
    subject = "Welcome to our platform!"
    dashboard_link = "http://localhost:3000/dashboard"
    html_content = render_email_template("new_account.mjml", username=username, dashboard_link=dashboard_link)
    send_test_email(email_to, subject, html_content)
