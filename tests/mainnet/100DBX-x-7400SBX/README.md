# Offer 100 DBX for 7400 SBX
## Create
```bash
❯ chia wallet show -f $partial_fp
Wallet height: 6450498
...
Chia Wallet:
   -Total Balance:         0.859999999999 xch (859999999999 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         999.08  (999080 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         0.0  (0 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3

❯ partial create -f $partial_fp --offer db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20:100 --request a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913:7400 -p 100DBX-x-7400SBX.offer
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                   │ Yes                                                                │
│ MOD_HASH:                │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name: │ 0x1fe62834cf93c9318d4f8f55f9266b6c0ff6b96d23013ce38f2a8652a4a415f5 │
│ Clawback Puzzle Hash:    │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:          │ 0xdb1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20 │
│ Request Asset Id:        │ 0xa628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913 │
│ Offer Amount:            │ 100 DBX                                                            │
│ Request Amount:          │ 7400 SBX                                                           │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:           │ xch1hs0kud8mc4tdy7djugv872mjw804gzfx7g0hfcnt5gfv0zjkhxus4ugkkf     │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯

The partial offer file is 100DBX-x-7400SBX.offer
```
- [100DBX-x-7400SBX.offer](100DBX-x-7400SBX.offer)

## Show
```bash
❯ partial show ./100DBX-x-7400SBX.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x1fe62834cf93c9318d4f8f55f9266b6c0ff6b96d23013ce38f2a8652a4a415f5 │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0xdb1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20 │
│ Request Asset Id:            │ 0xa628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913 │
│ Offer Amount:                │ 100000 mojos                                                       │
│ Request Amount:              │ 7400000 mojos                                                      │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1hs0kud8mc4tdy7djugv872mjw804gzfx7g0hfcnt5gfv0zjkhxus4ugkkf     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 100000/7400000                                                     │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯
```

## Take
```bash
❯ chia wallet show -f $partial_taker_fp
Wallet height: 6450531
...
Chia Wallet:
   -Total Balance:         0.113243099994 xch (113243099994 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         0.0  (0 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         303.467  (303467 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3

❯ partial take -f $partial_taker_fp -a (4e3) -m (1) ./100DBX-x-7400SBX.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x1fe62834cf93c9318d4f8f55f9266b6c0ff6b96d23013ce38f2a8652a4a415f5 │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0xdb1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20 │
│ Request Asset Id:            │ 0xa628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913 │
│ Offer Amount:                │ 100000 mojos                                                       │
│ Request Amount:              │ 7400000 mojos                                                      │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1hs0kud8mc4tdy7djugv872mjw804gzfx7g0hfcnt5gfv0zjkhxus4ugkkf     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 100000/7400000                                                     │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

 296 SBX -> 4 DBX
 Sending 296 SBX
 Paying 0.04 DBX in fees
 Receiving 3.96 DBX
 ...

 ❯ chia wallet show -f $partial_taker_fp
Wallet height: 6450543
Sync status: Synced
Balances, fingerprint: 2866421833

Chia Wallet:
   -Total Balance:         0.113243099993 xch (113243099993 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         3.96  (3960 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         7.467  (7467 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3

❯ chia wallet show -f $partial_fp
Wallet height: 6450546
...
Chia Wallet:
   -Total Balance:         0.859999999999 xch (859999999999 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         899.08  (899080 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         296.0  (296000 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3
```

- [1st take spend bundle](1st-take-sb.json)
- [after 1st take offer](after-1st-take.offer)
- [xch.events](https://xch.events/transactions/aa8cafded1e8e6a08a0321de871d5b61b9f208e4d17b61091222cab1277b3cdf)
- [fee transaction](https://spacescan.io/en/coin/0x9fa3c835581eaef99d0a9749877949dc3a34112de97794a837a63895328f7f83)

## Clawback
```bash
❯ partial clawback -f $partial_fp -m (1) ./after-1st-take.offer
...
❯ chia wallet show -f $partial_fp
Wallet height: 6450606
...

Chia Wallet:
   -Total Balance:         0.859999999998 xch (859999999998 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         995.08  (995080 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         296.0  (296000 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3
```

- [clawback spend bundle](clawback.json)
- [xch.events](https://xch.events/transactions/dd064a8b3221d8fde070f0d8da3f56d2335f780ae013e0ac26daa9cc08a60250)