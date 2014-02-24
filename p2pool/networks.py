from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
     mintcoin=math.Object(
        PARENT=networks.nets['mintcoin'],
        SHARE_PERIOD=5, # seconds target spacing
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares coinbase maturity
        SPREAD=45, # blocks
        IDENTIFIER='5F0183D62F69AA32'.decode('hex'),
        PREFIX='52F8CF5955E0AA34'.decode('hex'),
        P2P_PORT=23666,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=8866,
        BOOTSTRAP_ADDRS='us-east1.cryptovein.com'.split(' '),
        ANNOUNCE_CHANNEL='#cryptovein',
        VERSION_CHECK=lambda v: True,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
