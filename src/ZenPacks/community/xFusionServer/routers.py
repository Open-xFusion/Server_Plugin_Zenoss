"""
功 能：该类主要涉及BMC,HMM路由相关配置
版权信息：超聚变数字技术有限公司，版本所有(C) 2017-2022
"""
from collections import namedtuple

from Products.ZenUtils.Ext import DirectRouter, DirectResponse
from Products import Zuul


class BmcRouter(DirectRouter):
    """
    BMC Router
    """

    # The method name - myRouterFunc - and its parameters - must match with
    #   the last part of the call for Zenoss.remote.myAppRouter.myRouterFunc
    #   in the javascript file myFooterMenu.js . The parameters will be
    #   populated by the items defined in the js file.

    # Note that the router function has 2 parameters, comments and rackSlot
    #  that are passed as the "opts" parameters from myFooterMenu.js.  The
    #  values of these fields were provided by the form input.

    def routerbs(self, deviceip, bootsequence, cfgboottype):
        """
        routerBS
        """
        facade = self._getFacade()

        # The object that is being operated on is in self.context

        devobject = self.context

        success, message = facade.bootsequence(
            devobject, deviceip, bootsequence, cfgboottype)

        if success:
            return DirectResponse.succeed(message)
        return DirectResponse.fail(message)

    def routerfpc(self, deviceip, frupowercontrol):
        """
        routerFPC
        """
        facade = self._getFacade()

        devobject = self.context

        frunum = 1
        success, message = facade.frupowerctrl(devobject, deviceip,
                                               frunum, frupowercontrol)

        if success:
            return DirectResponse.succeed(message)
        return DirectResponse.fail(message)

    def _getFacade(self):
        """
        getfacade
        """

        # The parameter in the next line - myAppAdapter - must match with
        #   the name field in an adapter stanza in configure.zcml

        return Zuul.getFacade('BMCAdapter', self.context)


class HmmRouter(DirectRouter):
    """
    HMM Router
    """

    def routerbbo(self, deviceip, hmmbladenum,
                  hmmbiosbootoption, hmmbotype):
        """
        routerBBO
        """
        facade = self._getFacade()

        # The object that is being operated on is in self.context
        devobject = self.context
        hmm_args = namedtuple('hmm_args', ['hmmbladenum', 'hmmbbo', 'hmmbotype'])
        hmm_info = hmm_args._make([hmmbladenum, hmmbiosbootoption, hmmbotype])

        success, message = facade.biosbootoption(devobject, deviceip, hmm_info)

        if success:
            return DirectResponse.succeed(message)

        return DirectResponse.fail(message)

    def routerfrucontrol(self, deviceip, hmmbladenum, hmmfrucontrol):
        """
        routerFruControl
        """
        facade = self._getFacade()

        devobject = self.context

        success, message = facade.frucontrol(devobject, deviceip,
                                             hmmbladenum, hmmfrucontrol)
        if success:
            return DirectResponse.succeed(message)

        return DirectResponse.fail(message)

    def _getFacade(self):
        """
        getfacade
        """
        return Zuul.getFacade('HMMAdapter', self.context)
