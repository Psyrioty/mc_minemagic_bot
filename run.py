from app.handlers.base import router
from app.handlers.admin import routerAdmin
from app.database.models import async_main
from app.tgBot import bot

import asyncio

from aiogram import Dispatcher

async def main():
    await async_main()

    dp = Dispatcher()
    dp.include_routers(routerAdmin, router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())