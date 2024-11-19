from rcon.source import rcon
#from config import RCON_IP, RCON_PORT, RCON_PASSWORD

class rconConnector:
    async def sendCode(name, code, RCON_IP, RCON_PORT, RCON_PASSWORD):
        await rcon(
            f'tell {name} Ваш код верификации: {code}',
            host=RCON_IP, port=RCON_PORT, passwd=RCON_PASSWORD
        )

    async def command(text, RCON_IP, RCON_PORT, RCON_PASSWORD):
        try:
            await rcon(
                text,
                host=RCON_IP, port=RCON_PORT, passwd=RCON_PASSWORD
            )
            return True
        except:
            return False