from apscheduler.schedulers.background import BackgroundScheduler
import datetime

#sched.add_job(my_job, 'cron', year=2017, month=03, day=22, hour=17, minute=19, second=07)
#sched.add_job(my_job, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
#sched.add_job(my_job(), 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2014-05-30')
#sched.add_job(my_job, 'cron', second='*/5')


def event_analysis_task():
    print(f"start : {datetime.datetime.now()}")
    print(f"end : {datetime.datetime.now()}")

def cronjob_schedulers_running():
    scheduler = BackgroundScheduler()
    scheduler.add_job(event_analysis_task, 'cron', minute='*/5') # 
    #scheduler.add_job(test, 'cron', day_of_week='mon-fri', minute='*/1')
    #scheduler.add_job(wazuh_cluster_lookup, 'cron', day_of_week='mon-fri', hour=16, minute=55)
    scheduler.start()

