from datetime import datetime

from discord_webhook import DiscordEmbed, DiscordWebhook
from flask import current_app, request

from backend.database.config_db import Config as cfg


def log(content, color, web=True):
    with current_app.app_context():
        if cfg.get_by_name('DISCORD_WEBHOOK_ENABLE'):
            try:
                webhook = DiscordWebhook(
                    cfg.get_by_name('DISCORD_WEBHOOK_URL'))
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                embed = DiscordEmbed(
                    title=f"🔒 {content}",
                    description=f"```{date}```",
                    color=int(color[1:], 16),
                )
                if web:
                    remote_addr = request.remote_addr
                    endpoint = request.endpoint
                    embed.add_embed_field(
                        name="🔧 IP:",
                        value=f'`{remote_addr}`',
                        inline=False
                    )
                    embed.add_embed_field(
                        name="🎫 Endpoint:",
                        value=f'`{endpoint}`',
                        inline=False
                    )
                embed.set_footer(
                    text="HypeEngine", icon_url=r'https://www.dropbox.com/scl/fi/oqyv9292z6i40as535pfn/HypeEngine_smaller.png?rlkey=l79k3hbuzr0bjo2qol0tgk3td&dl=0')
                webhook.add_embed(embed)
                webhook.execute()
            except Exception as e:
                print(e)
