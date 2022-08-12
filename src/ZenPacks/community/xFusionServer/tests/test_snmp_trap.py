# -*- coding: utf-8 -*-
"""
功 能：测试类，该类主要涉及测试功能
版权信息：超聚变数字技术有限公司，版本所有(C) 2017-2022
"""

import unittest
import Globals
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp
from pyasn1.codec.ber import encoder
from pysnmp.proto import api
from Crypto.PublicKey.DSA import oid
from Products.ZenEvents.Event import Event
from Products.ZenEvents.ZenEventClasses import Status_Ping
from Products.ZenUtils.ZCmdBase import ZCmdBase

# Protocol version to use
ver_id = api.protoVersion2c
proto_mod = api.protoModules[ver_id]

# Build PDU
trap_pdu = proto_mod.TrapPDU()
proto_mod.apiTrapPDU.setDefaults(trap_pdu)

trapdip = '192.168.1.108'
community = 'public'


class TestTrap(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def teartrapevent(self):
        """teartrapevent"""
        evt = Event()
        evt.device = "/Service/XFUSION/BMC"
        evt.eventClass = 'hwOEMEvent'
        evt.summary = "XFUSION OEM event"
        evt.severity = 2
        zodb = ZCmdBase(noopts=True)
        zem = zodb.dmd.ZenEventManager
        zem.sendEvent(evt)
        self.assertTrue(True)

    def testtrapv2(self):
        """testtrapv2"""
        # Traps have quite different semantics among proto versions
        if ver_id == api.protoVersion2c:
            var = []
            oid_version = (1, 3, 6, 1, 4, 1, 58132, 2, 235, 1, 1, 4, 1, 0)
            # 1.3.6.1.4.1.58132.2.235.1.1.15.50.1.5(cpuClockRate).0
            # 1.3.6.1.4.1.58132.2.235.1.1.4.1.0  trapEnable
            proto_val = proto_mod.Integer(1)
            var.append((oid_version, proto_val))

            proto_mod.apiTrapPDU.setVarBinds(trap_pdu, var)

        # Build message
        trap_msg = proto_mod.Message()
        proto_mod.apiMessage.setDefaults(trap_msg)
        proto_mod.apiMessage.setCommunity(trap_msg, community)
        proto_mod.apiMessage.setPDU(trap_msg, trap_pdu)

        transport_dispatcher = AsynsockDispatcher()
        transport_dispatcher.registerTransport(
            udp.domainName, udp.UdpSocketTransport().openClientMode()
        )
        # 本机测试使用localhost，应为对应trap server 的IP地址。
        transport_dispatcher.sendMessage(
            encoder.encode(trap_msg), udp.domainName, (trapdip, 162)
        )
        transport_dispatcher.runDispatcher()
        transport_dispatcher.closeDispatcher()

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
