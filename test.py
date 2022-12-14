import pytz

from time import sleep

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import asyncio

tz = pytz.timezone('Asia/Tashkent')

job_defaults = {
    "misfire_grace_time": 3600
}

jobstores = {
    "default": SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

scheduler = AsyncIOScheduler(
    timezone=tz,
    jobstores=jobstores,
    job_defaults=job_defaults
)


async def jobs():
    print('Hello world')


# scheduler.add_job(jobs, trigger='cron', day_of_week='*', hour=15, minute=26) # Haftaning barcha kunlari soat 15:26 da ishga tushadi
# scheduler.add_job(jobs, trigger='cron', day_of_week='mon-fri', hour=15, minute=26) # Haftaning dushanbadan jumagacha kunlari soat 15:26 da ishga tushadi
# scheduler.add_job(jobs, trigger='interval', hours=1) # Har 1 soatda qayta ishni bajaradi
# scheduler.add_job(jobs, trigger='interval', seconds=1) # Har 1 soatda qayta ishni bajaradi


if __name__ == '__main__':
    scheduler.add_job(jobs, trigger='interval', seconds=1) # Har 1 soatda qayta ishni bajaradi
    scheduler.start()

    asyncio.get_event_loop().run_forever()
