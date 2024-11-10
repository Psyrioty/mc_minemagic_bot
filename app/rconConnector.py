from rcon.source import rcon
from config import RCON_IP, RCON_PORT, RCON_PASSWORD

async def sendCode(name, code):
    await rcon(
        f'tell {name} Ваш код верификации: {code}',
        host=RCON_IP, port=RCON_PORT, passwd=RCON_PASSWORD
    )