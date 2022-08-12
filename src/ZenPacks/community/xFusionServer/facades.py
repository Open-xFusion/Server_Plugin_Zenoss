# -*- coding: utf-8 -*-
"""
功 能：Facade类，该类主要涉及配置OS上下电,设置启动顺序功能
版权信息：超聚变数字技术有限公司，版本所有(C) 2017-2022
"""
import os
import logging
from collections import namedtuple
from zope.interface import implements
from Products.Zuul.facades import ZuulFacade
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.ZenUtils.Utils import executeCommand
from interfaces import IBMCFacade
from interfaces import IHMMFacade

LOG = logging.getLogger('.'.join(['', __name__]))
ARGS = namedtuple('ARGS', ['arg1', 'arg2', 'arg3', 'arg4', 'arg5',
                           'arg6', 'arg7', 'arg8', 'arg9', 'arg10'])


class BMCFacade(ZuulFacade):
    """
    BMC Facade
    """
    implements(IBMCFacade)

    def extractips(self, ips, iplist):
        """
        extractips
        """
        deviceip1 = ips.replace(' ', '')
        for ipstr in deviceip1.split(","):
            if ipstr == '':
                continue
            deviceip = ipstr.split('-')
            if len(deviceip) == 2:
                if deviceip[0].count('.') == 3:
                    rangestart = int(deviceip[0][deviceip[0].rfind('.') + 1:])
                    rangeend = int(deviceip[1])
                    part1 = deviceip[0][:deviceip[0].rfind('.') + 1]
                    for iptmp in range(rangestart, rangeend + 1):
                        iplist.append(part1 + str(iptmp))
            else:
                iplist.append(ipstr)

    # Note that the the facade function, myFacadeFunc has 3 parameters
    #  The object is passed in addition to the comment and rackSlot

    def bootsequencesingle(self, deviceip, bootsequence, allbmcdevice):
        """
        bootsequencesingle
        """
        deviceroot = self._dmd.getDmdRoot("Devices")
        device = deviceroot.findDevice(deviceip)
        if device is None:
            return [deviceip, "device Not found!"]
        LOG.debug("myFacadeFunc data %s %s %s %s", deviceip,
                  allbmcdevice, device.__class__, device.zSnmpVer)
        arg1 = deviceip
        arg2 = "-" + device.zSnmpVer
        arg3 = "-c" + device.zSnmpCommunity
        arg4 = "-u" + device.zSnmpSecurityName
        arg5 = "-a" + device.zSnmpAuthType
        arg6 = "-A" + device.zSnmpAuthPassword
        arg7 = "-x" + device.zSnmpPrivType
        arg8 = "-X" + device.zSnmpPrivPassword
        bootsequencearg = str(bootsequence)
        arg9 = bootsequencearg

        libexec = os.path.join(os.path.dirname(__file__), 'libexec')
        predefinedcmd = []
        if arg2 == "-v2c":
            predefinedcmd = [
                os.path.join(
                    libexec, 'bmcbootsequence.sh'), arg1, arg2, arg3, arg4,
                arg5, arg6, arg7, arg8, arg9]
        else:
            predefinedcmd = [
                os.path.join(
                    libexec, 'bmcbootsequence.sh'), arg1, arg2, arg3, arg4,
                arg5, arg6, arg7, arg8, arg9]
        result = executeCommand(predefinedcmd, None, None)
        retstr = "Fail"
        if result == 0:
            retstr = "Success"
        LOG.info("executeCommand result %s ", result)
        return [deviceip, retstr]

    def bootsequencetype(self, deviceip, bootsequence, allbmcdevice):
        """
        bootsequencetype
        """
        deviceroot = self._dmd.getDmdRoot("Devices")
        device = deviceroot.findDevice(deviceip)
        if device is None:
            return [deviceip, "device Not found!"]
        LOG.debug("myFacadeFunc data %s %s %s %s", deviceip,
                  allbmcdevice, device.__class__, device.zSnmpVer)
        arg1 = deviceip
        arg2 = "-" + device.zSnmpVer
        arg3 = "-c" + device.zSnmpCommunity
        arg4 = "-u" + device.zSnmpSecurityName
        arg5 = "-a" + device.zSnmpAuthType
        arg6 = "-A" + device.zSnmpAuthPassword
        arg7 = "-x" + device.zSnmpPrivType
        arg8 = "-X" + device.zSnmpPrivPassword
        arg9 = bootsequence

        if not bootsequence.isdigit():
            return [deviceip, 'option not in range']
        if int(bootsequence) > 20:
            return [deviceip, 'option not in range']

        libexec = os.path.join(os.path.dirname(__file__), 'libexec')
        predefinedcmd = []
        if arg2 == "-v2c":
            predefinedcmd = [
                os.path.join(
                    libexec, 'bmcboottype.sh'), arg1, arg2, arg3, arg4,
                arg5, arg6, arg7, arg8, arg9]
        else:
            predefinedcmd = [
                os.path.join(
                    libexec, 'bmcboottype.sh'), arg1, arg2, arg3, arg4,
                arg5, arg6, arg7, arg8, arg9]
        result = executeCommand(predefinedcmd, None, None)

        retstr = "Fail"
        if result == 0:
            retstr = "Success"
        LOG.info("executeCommand result %s ", result)
        return [deviceip, retstr]

    def bootsequence(self, devobj, deviceip, bootsequence, boottype):
        """ Modifies bootsequence and boottype attributes for a device """
        iplist = []
        self.extractips(deviceip, iplist)
        ipret = []
        for ipstr in iplist:
            if boottype == 1:
                self.bootsequencetype(ipstr, "1", boottype)
            elif boottype == 2:
                self.bootsequencetype(ipstr, "2", boottype)
            result = self.bootsequencesingle(ipstr, bootsequence, boottype)
            ipret.append(result)
        return True, _t("BMC Boot Sequence set device %s" % ipret)

    def frupowerctrlsingle(self, deviceip, frupowercontrol):
        """
        frupowerctrlsingle
        """
        deviceroot = self._dmd.getDmdRoot("Devices")
        device = deviceroot.findDevice(deviceip)
        if device is None:
            return [deviceip, "device Not found!"]
        arg1 = deviceip
        arg2 = "-" + device.zSnmpVer
        arg3 = "-c" + device.zSnmpCommunity
        arg4 = "-u" + device.zSnmpSecurityName
        arg5 = "-a" + device.zSnmpAuthType
        arg6 = "-A" + device.zSnmpAuthPassword
        arg7 = "-x" + device.zSnmpPrivType
        arg8 = "-X" + device.zSnmpPrivPassword
        frupowercontrolarg = str(frupowercontrol)
        arg9 = frupowercontrolarg

        if not frupowercontrolarg.isdigit():
            return [deviceip, 'option not in range']
        if int(frupowercontrolarg) > 10:
            return [deviceip, 'option not in range']

        libexec = os.path.join(os.path.dirname(__file__), 'libexec')
        predefinedcmd = []
        if arg2 == "-v2c":
            predefinedcmd = [
                os.path.join(
                    libexec, 'bmcfrupowercontrol.sh'), arg1, arg2, arg3, arg4,
                arg5, arg6, arg7, arg8, arg9]
        else:
            predefinedcmd = [
                os.path.join(
                    libexec, 'bmcfrupowercontrol.sh'), arg1, arg2, arg3, arg4,
                arg5, arg6, arg7, arg8, arg9]
        result = executeCommand(predefinedcmd, None, None)
        retstr = "Fail"
        if result == 0:
            retstr = "Success"
        LOG.info("executeCommand result %s ", result)
        return [deviceip, retstr]

    def frupowerctrl(self, devobj, deviceip, frunum, frupowercontrol):
        """ Modifies frunum and frupowercontrol attributes for a device """
        frunum = frunum
        devobj = devobj
        iplist = []
        self.extractips(deviceip, iplist)
        ipret = []
        for ipstr in iplist:
            ret = self.frupowerctrlsingle(ipstr, frupowercontrol)
            ipret.append(ret)
        return True, _t("BMC FRU Power Control set for device %s" % (ipret))


class HMMFacade(ZuulFacade):
    """
    HMM Facade
    """
    implements(IHMMFacade)

    # deprecated class for can not link with URL router

    def extractips(self, ips, iplist):
        """
        extractips
        """
        deviceip1 = ips.replace(' ', '')
        for ipstr in deviceip1.split(","):
            if ipstr == '':
                continue
            deviceip = ipstr.split('-')
            if len(deviceip) == 2:
                if deviceip[0].count('.') == 3:
                    rangestart = int(deviceip[0][deviceip[0].rfind('.') + 1:])
                    rangeend = int(deviceip[1])
                    part1 = deviceip[0][:deviceip[0].rfind('.') + 1]
                    for iptmp in range(rangestart, rangeend + 1):
                        iplist.append(part1 + str(iptmp))
            else:
                iplist.append(ipstr)

    def biosbootoptionsingleblade(self, args):
        """
        biosbootoptionsingleblade
        """
        LOG.info("biosbootoptionsingleblade entry")
        libexec = os.path.join(os.path.dirname(__file__), 'libexec')
        predefinedcmd = []
        if args.arg2 == "-v2c":
            predefinedcmd = [
                os.path.join(
                    libexec, 'hmmbladebiosbootoption.sh'), args.arg1, args.arg2,
                args.arg3, args.arg4, args.arg5, args.arg6, args.arg7,
                args.arg8, args.arg9, args.arg10]
        else:
            predefinedcmd = [
                os.path.join(
                    libexec, 'hmmbladebiosbootoption.sh'), args.arg1, args.arg2,
                args.arg3, args.arg4, args.arg5, args.arg6, args.arg7,
                args.arg8, args.arg9, args.arg10]
        result = executeCommand(predefinedcmd, None, None)
        LOG.info("executeCommand result %s ", result)
        return result

    def biosbootoptionsingle(self, devobj, deviceip, hmm_info):
        """
        biosbootoptionsingle
        """
        devobj = devobj
        deviceroot = self._dmd.getDmdRoot("Devices")
        device = deviceroot.findDevice(deviceip)
        if device is None:
            LOG.info("device Not found")
            return [deviceip, "device Not found!"]
        LOG.info("myFacadeFunc data %s %s %s", deviceip,
                 device.__class__, device.zSnmpVer)
        arg1 = deviceip
        arg2 = "-" + device.zSnmpVer
        arg3 = "-c" + device.zSnmpCommunity
        arg4 = "-u" + device.zSnmpSecurityName
        arg5 = "-a" + device.zSnmpAuthType
        arg6 = "-A" + device.zSnmpAuthPassword
        arg7 = "-x" + device.zSnmpPrivType
        arg8 = "-X" + device.zSnmpPrivPassword
        arg9 = hmm_info.hmmbladenum
        arg10 = str(hmm_info.hmmbbo)

        if hmm_info.hmmbotype == 0:
            arg10 = "disable"
        elif hmm_info.hmmbotype == 1:
            arg10 = "once," + str(hmm_info.hmmbbo)
        else:
            arg10 = "persistent," + str(hmm_info.hmmbbo)

        bladelist = []
        if hmm_info.hmmbladenum.isdigit():
            bladelist.append(hmm_info.hmmbladenum)
        elif ',' in hmm_info.hmmbladenum:
            bladelist = hmm_info.hmmbladenum.split(",")
        elif '-' in hmm_info.hmmbladenum:
            bladeliststr = hmm_info.hmmbladenum.split("-")
            if len(bladeliststr) == 2:
                rangestart = int(bladeliststr[0])
                rangeend = int(bladeliststr[1])
                if rangestart == rangeend:
                    bladelist.append(str(rangestart))
                else:
                    for iptmp in range(rangestart, rangeend + 1):
                        bladelist.append(str(iptmp))
        args = ARGS._make([arg1, arg2, arg3, arg4, arg5,
                           arg6, arg7, arg8, arg9, arg10])
        return self.biosbootoptionsingleresult(deviceip, bladelist, args)

    def biosbootoptionsingleresult(self, deviceip, bladelist, args):
        ipret = []
        for bladen in bladelist:
            if not bladen.isdigit():
                continue
            if int(bladen) < 1 or int(bladen) > 32:
                continue

            arg9 = str(bladen)
            args = args._replace(arg9=str(bladen))
            retstr = "Fail"
            ret = self.biosbootoptionsingleblade(args)
            if ret == 0:
                retstr = "Success"
            ipret.append([arg9, retstr])
        return [deviceip, ipret]

    def biosbootoption(self, devobj, deviceip, hmm_info):
        """ Modifies bladenum and biosbootoption attributes for a device """
        iplist = []
        ipret = []
        self.extractips(deviceip, iplist)

        for ipstr in iplist:
            ipret.append(self.biosbootoptionsingle(devobj, ipstr, hmm_info))

        return True, _t("HMM Bios Boot Option set device %s" % ipret)

    def frucontrolsingleblade(self, args):
        """
        frucontrolsingleblade
        """
        libexec = os.path.join(os.path.dirname(__file__), 'libexec')
        predefinedcmd = []
        # 2018-01-12 add power on and off oid
        valarg = int(args.arg10)
        if valarg >= 100:
            if valarg == 100:
                arg10 = "poweron"
            if valarg == 101:
                arg10 = "poweroff"
            args = args._replace(arg10=arg10)
            if args.arg2 == "-v2c":
                predefinedcmd = [
                    os.path.join(
                        libexec, 'hmmbladefruonoff.sh'), args.arg1, args.arg2,
                    args.arg3, args.arg4, args.arg5, args.arg6,
                    args.arg7, args.arg8, args.arg9, args.arg10]
            else:
                predefinedcmd = [
                    os.path.join(
                        libexec, 'hmmbladefruonoff.sh'), args.arg1, args.arg2,
                    args.arg3, args.arg4, args.arg5, args.arg6,
                    args.arg7, args.arg8, args.arg9, args.arg10]
        else:
            if args.arg2 == "-v2c":
                predefinedcmd = [
                    os.path.join(
                        libexec, 'hmmbladefrucontrol.sh'), args.arg1, args.arg2,
                    args.arg3, args.arg4, args.arg5, args.arg6,
                    args.arg7, args.arg8, args.arg9, args.arg10]
            else:
                predefinedcmd = [
                    os.path.join(
                        libexec, 'hmmbladefrucontrol.sh'), args.arg1, args.arg2,
                    args.arg3, args.arg4, args.arg5, args.arg6,
                    args.arg7, args.arg8, args.arg9, args.arg10]
        result = executeCommand(predefinedcmd, None, None)
        LOG.info("executeCommand result %s ", result)
        return result

    def frucontrolsingle(self, devobj, deviceip, hmmbladenum, hmmfrucontrol):
        """
        frucontrolsingle
        """
        devobj = devobj
        deviceroot = self._dmd.getDmdRoot("Devices")
        device = deviceroot.findDevice(deviceip)
        if device is None:
            return [deviceip, "device Not found!"]
        arg1 = deviceip
        arg2 = "-" + device.zSnmpVer
        arg3 = "-c" + device.zSnmpCommunity
        arg4 = "-u" + device.zSnmpSecurityName
        arg5 = "-a" + device.zSnmpAuthType
        arg6 = "-A" + device.zSnmpAuthPassword
        arg7 = "-x" + device.zSnmpPrivType
        arg8 = "-X" + device.zSnmpPrivPassword
        arg9 = hmmbladenum
        hmmfrucontrol = str(hmmfrucontrol)
        arg10 = hmmfrucontrol

        if not hmmfrucontrol.isdigit():
            return 'option not in range'
        if int(hmmfrucontrol) > 1000:
            return 'option not in range'

        bladelist = []
        if hmmbladenum.isdigit():
            bladelist.append(hmmbladenum)
        elif ',' in hmmbladenum:
            bladelist = hmmbladenum.split(",")
        elif '-' in hmmbladenum:
            bladeliststr = hmmbladenum.split("-")
            if len(bladeliststr) == 2:
                rangestart = int(bladeliststr[0])
                rangeend = int(bladeliststr[1])
                if rangestart == rangeend:
                    bladelist.append(str(rangestart))
                else:
                    for iptmp in range(rangestart, rangeend + 1):
                        bladelist.append(str(iptmp))
        args = ARGS._make([arg1, arg2, arg3, arg4, arg5,
                           arg6, arg7, arg8, arg9, arg10])
        return self.frucontrolsingleresult(deviceip, bladelist, args)

    def frucontrolsingleresult(self, deviceip, bladelist, args):
        ipret = []
        for bladen in bladelist:
            if not bladen.isdigit():
                continue
            if int(bladen) < 1 or int(bladen) > 32:
                continue
            args = args._replace(arg9=str(bladen))
            retstr = "Fail"
            ret = self.frucontrolsingleblade(args)
            if ret == 0:
                retstr = "Success"
            ipret.append([args.arg9, retstr])
        return [deviceip, ipret]

    def frucontrol(self, devobj, deviceip, hmmbladenum, hmmfrucontrol):
        """ Modifies frunum and frupowercontrol attributes for a device """
        iplist = []
        ipret = []
        self.extractips(deviceip, iplist)
        for ipstr in iplist:
            ipret.append(self.frucontrolsingle(
                devobj, ipstr, hmmbladenum, hmmfrucontrol))

        return True, _t("HMM FRU Control set for device %s" % (ipret))
