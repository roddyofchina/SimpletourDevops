#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

class ServerBaseInfo(object):
    def __init__(self,data,minion):
        self.ServerHardInfo = {}
        self.serverbaseinfo={}
        self.data = data
        self.minion = minion
        self.serverbaseinfo['sn'] = self.data[self.minion]['serialnumber']
        self.serverbaseinfo['hostname'] = self.data[self.minion]['nodename']
        self.serverbaseinfo['cpu_count'] = self.data[self.minion]['CPU_COUNT']
        self.serverbaseinfo['cpu_core_count'] = self.data[self.minion]['CPU_Info']['cpu processor']
        self.serverbaseinfo['saltid'] = self.data[self.minion]['id']
        self.serverbaseinfo['mem'] = self.data[self.minion]['Mem_Total']
        self.serverbaseinfo['swap'] = self.data[self.minion]['Swap_Total']
        self.serverbaseinfo['platform'] = self.data[self.minion]['osarch']
        self.serverbaseinfo['system'] = self.data[self.minion]['oscodename']
        self.serverbaseinfo['version'] = self.data[self.minion]['osrelease']
        self.ServerHardInfo['Serverbaseinfo']=self.serverbaseinfo
class ServerCPUInfo(ServerBaseInfo):
    def __init__(self,data,minion):
        super(ServerCPUInfo,self).__init__(data,minion)

    def ServerCPU(self):
        servercpuinfo ={}
        servercpuinfo['uuid'] = self.data[self.minion]['cpu_uuid']
        servercpuinfo['parent_sn'] = self.data[self.minion]['serialnumber']
        servercpuinfo['architecture'] = self.data[self.minion]['cpuarch']
        servercpuinfo['model'] = self.data[self.minion]['cpu_model']
        servercpuinfo['cpu_mhz'] = self.data[self.minion]['cpu MHz']
        servercpuinfo['L1cache'] = self.data[self.minion]['CPU_Info']['L1 cache']
        servercpuinfo['L2cache'] = self.data[self.minion]['CPU_Info']['L2 cache']
        servercpuinfo['L3cache'] = self.data[self.minion]['CPU_Info']['L3 cache']
        servercpuinfo['thread'] = self.data[self.minion]['CPU_Info']['cpu processor']
        self.ServerHardInfo['servercpuinfo'] =  servercpuinfo
        return self.ServerHardInfo

class ServerNICInfo(ServerBaseInfo):
    def __init__(self,data,minion):
        super(ServerNICInfo,self).__init__(data,minion)

    def ServerNIC(self):
        servernicinfo={}
        servernicinfo['nicinfo'] = self.data[self.minion]['nicinfo']
        self.ServerHardInfo['servernicinfo'] = servernicinfo
        return self.ServerHardInfo
class ServerDiskInfo(ServerBaseInfo):
    def __init__(self,data,minion):
        super(ServerDiskInfo,self).__init__(data,minion)

    def ServerDISK(self):
        serverdiskinfo={}
        serverdiskinfo['diskinfo'] = self.data[self.minion]['disk']
        self.ServerHardInfo['serverdiskinfo'] = serverdiskinfo
        return self.ServerHardInfo












