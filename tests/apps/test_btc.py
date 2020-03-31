#!/usr/bin/env python3

'''
Tests to ensure that speculos launches correctly the BTC apps.
'''

import binascii
import os
import pytest

class TestBtc:
    '''Tests for Bitcoin app.'''

    def test_btc_get_version(self, app, stop_app):
        '''Send a get_version APDU to the BTC app.'''

        app.run()

        packet = binascii.unhexlify('E0C4000000')
        data, status = app.exchange(packet)
        assert status == 0x9000

        app.stop()

    def test_btc_get_public_key_with_user_approval(self, app, stop_app, finger_client):
        if app.model != "blue":
            pytest.skip("Device not supported")

        app.run(finger_port=1236, headless=True)

        finger_client.eventsLoop = ["220,440,1", "220,440,0"]  # x,y,pressed
        finger_client.start()
       
        bip32_path = bytes.fromhex("8000002C" + "80000000" + "80000000" + "00000000" + "00000000")
        payload = bytes([len(bip32_path)//4]) + bip32_path
        apdu = bytes.fromhex("e0400100") +  bytes([len(payload)]) + payload

        response, status = app.exchange(apdu)
        assert status == 0x9000

class TestBtcTestnet:
    '''Tests for Bitcoin Testnet app.'''

    def test_btc_lib(self, app, stop_app):
        # assumes that the Bitcoin version of the app also exists.
        btc_app = app.path.replace('btc-test', 'btc')
        assert os.path.exists(btc_app)

        args = [ '-l', 'Bitcoin:%s' % btc_app ]
        app.run(args=args)

        packet = binascii.unhexlify('E0C4000000')
        data, status = app.exchange(packet)
        assert status == 0x9000