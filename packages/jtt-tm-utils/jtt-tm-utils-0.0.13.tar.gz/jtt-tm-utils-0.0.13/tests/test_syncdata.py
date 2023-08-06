from jtt_tm_utils.sync_basedata import data_manager,SyncBasedataManage
import aioredis
import os
import asyncio

import functools


import unittest



class CliTestCase(unittest.TestCase):
    def setUp(self):
        async def _setup():
            redis = await aioredis.create_redis_pool('redis://192.168.101.70:6380/0')
            self.manager.config(redis,['vehicle'])
            #
        self.loop =asyncio.get_event_loop()
        self.manager = MySyncManager()
        self.loop.run_until_complete(_setup())



    # def test_up_project(self):
    #     os.chdir(os.path.join(self.projectname))
    #     up_project()


    def test_makemethod(self):
       self.loop.run_until_complete( self.manager.get_vehicle('D0001'))
       self.manager.custom_reload()
       self.manager.custom_reload_item('vehicle','D0001')
       self.loop.run_forever()


