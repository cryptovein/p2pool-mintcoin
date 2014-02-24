import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

@defer.inlineCallbacks
def get_subsidy(bitcoind, target):
    res = yield bitcoind.rpc_getblock(target)

    defer.returnValue(res)

nets = dict(
    mintcoin=math.Object(
        P2P_PREFIX='ced5dbfa'.decode('hex'), #pchmessagestart
        P2P_PORT=12788,
        ADDRESS_VERSION=51, #pubkey_address
        RPC_PORT=12789,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'MintCoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
SUBSIDY_FUNC=lambda height: 900000*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=30, # s
        SYMBOL='MINT',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'MintCoin')
if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/MintCoin/')
if platform.system() == 'Darwin' else os.path.expanduser('~/.MintCoin'), 'MintCoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://mintcoin-explorer.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://mintcoin-explorer.info/address/',
        TX_EXPLORER_URL_PREFIX='http://mintcoin-explorer.info/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.000001,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
