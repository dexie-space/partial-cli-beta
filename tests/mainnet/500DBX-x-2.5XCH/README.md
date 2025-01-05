# Offer 500 DBX for 2.5 XCH
## Create
```bash
❯ chia wallet show -f $partial_fp
Wallet height: 6450215
...
Chia Wallet:
   -Total Balance:         0.4 xch (400000000000 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         1000.0  (1000000 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         80.0  (80000 mojo)
   ...
   -Wallet ID:             3

❯ partial create -f $partial_fp --offer db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20:500 --request 1:2.5 -p 500DBX-x-2.5XCH.offer
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                   │ Yes                                                                │
│ MOD_HASH:                │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name: │ 0x29afabb516014c5ff0f9df3a3a72631ee253aefdcb88dd93c7cb80455398be7b │
│ Clawback Puzzle Hash:    │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:          │ 0xdb1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20 │
│ Request Asset Id:        │ XCH                                                                │
│ Offer Amount:            │ 500 DBX                                                            │
│ Request Amount:          │ 2.5 XCH                                                            │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:           │ xch1hs0kud8mc4tdy7djugv872mjw804gzfx7g0hfcnt5gfv0zjkhxus4ugkkf     │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯

The partial offer file is 500DBX-x-2.5XCH.offer
```
- [500DBX-x-2.5XCH.offer](./500DBX-x-2.5XCH.offer)

## Show
```bash
❯ partial show ./500DBX-x-2.5XCH.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x29afabb516014c5ff0f9df3a3a72631ee253aefdcb88dd93c7cb80455398be7b │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0xdb1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20 │
│ Request Asset Id:            │ XCH                                                                │
│ Offer Amount:                │ 500000 mojos                                                       │
│ Request Amount:              │ 2500000000000 mojos                                                │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1hs0kud8mc4tdy7djugv872mjw804gzfx7g0hfcnt5gfv0zjkhxus4ugkkf     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 500000/2500000000000                                               │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯
```

## Take
```bash
❯ chia wallet show -f $partial_taker_fp
Wallet height: 6450229
...
Chia Wallet:
   -Total Balance:         0.573243099997 xch (573243099997 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         0.0  (0 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         223.467  (223467 mojo)
   ...
   -Wallet ID:             3

❯ partial take -f $partial_taker_fp -a (50e3) -m (1) ./500DBX-x-2.5XCH.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x29afabb516014c5ff0f9df3a3a72631ee253aefdcb88dd93c7cb80455398be7b │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0xdb1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20 │
│ Request Asset Id:            │ XCH                                                                │
│ Offer Amount:                │ 500000 mojos                                                       │
│ Request Amount:              │ 2500000000000 mojos                                                │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1hs0kud8mc4tdy7djugv872mjw804gzfx7g0hfcnt5gfv0zjkhxus4ugkkf     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 500000/2500000000000                                               │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

 0.25 XCH -> 50 DBX
 Sending 0.25 XCH
 Paying 0.5 DBX in fees
 Receiving 49.5 DBX
 ...
 ❯ chia wallet show -f $partial_taker_fp
Wallet height: 6450248
...

Chia Wallet:
   -Total Balance:         0.323243099996 xch (323243099996 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         49.5  (49500 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         223.467  (223467 mojo)
   ...
   -Wallet ID:             3

❯ chia wallet show -f $partial_fp
Wallet height: 6450255
...
Chia Wallet:
   -Total Balance:         0.65 xch (650000000000 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         500.0  (500000 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         80.0  (80000 mojo)
   ...
   -Wallet ID:             3
```
- [1st spend bundle](./1st-taker-sb.json)
- [after 1st take offer](./after-1st-take.offer)
- [xch.events](https://xch.events/transactions/31109021e6be7324312625146d7a4085aeece709f27574c1db1a7081d7d02250)
- [fee transaction](https://spacescan.io/en/coin/0x874a14a8875449050eb7694d1a6f20e70c83b4fa2e477ffa3b3308df65ad6782)

```bash
❯ partial show ./after-1st-take.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x81d6fdf957e49bbf8d25d9af79040fc1fd347a10ede7c48d1574c8036aa62fc5 │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0xdb1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20 │
│ Request Asset Id:            │ XCH                                                                │
│ Offer Amount:                │ 450000 mojos                                                       │
│ Request Amount:              │ 2250000000000 mojos                                                │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1hs0kud8mc4tdy7djugv872mjw804gzfx7g0hfcnt5gfv0zjkhxus4ugkkf     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 500000/2500000000000                                               │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯
```

## 2nd Take
```bash
❯ partial take -f $partial_taker_fp -a (42e3) -m (1) ./after-1st-take.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x81d6fdf957e49bbf8d25d9af79040fc1fd347a10ede7c48d1574c8036aa62fc5 │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0xdb1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20 │
│ Request Asset Id:            │ XCH                                                                │
│ Offer Amount:                │ 450000 mojos                                                       │
│ Request Amount:              │ 2250000000000 mojos                                                │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1hs0kud8mc4tdy7djugv872mjw804gzfx7g0hfcnt5gfv0zjkhxus4ugkkf     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 500000/2500000000000                                               │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

 0.21 XCH -> 42 DBX
 Sending 0.21 XCH
 Paying 0.42 DBX in fees
 Receiving 41.58 DBX
 ...

 ❯ chia wallet show -f $partial_taker_fp
Wallet height: 6450312
...
Chia Wallet:
   -Total Balance:         0.113243099995 xch (113243099995 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         91.08  (91080 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         223.467  (223467 mojo)
   ...
   -Wallet ID:             3

❯ chia wallet show -f $partial_fp
Wallet height: 6450322
...
Chia Wallet:
   -Total Balance:         0.86 xch (860000000000 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         500.0  (500000 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         80.0  (80000 mojo)
   ...
   -Wallet ID:             3
```

- [2nd spend bundle](./2nd-take-sb.json)
- [after 2nd take offer](./after-2nd-take.offer)
- [xch.events](https://xch.events/transactions/273d11aa58194fd5513363c30e207cbbb95ddf9ab5e05f16194c4682fbd8b5c2)
- [fee transaction](https://spacescan.io/en/coin/0xbf9077fc386c2aa4ef12b9ced11161caa1d327a2cdccbe37d7f3aeaf6244e6f4)

## Clawback
```bash
❯ partial show ./after-2nd-take.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x51e7ffde2100cca0de49a22b6134b9730bffe0a3f8f22aa6121a5f20c76225d9 │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0xdb1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20 │
│ Request Asset Id:            │ XCH                                                                │
│ Offer Amount:                │ 408000 mojos                                                       │
│ Request Amount:              │ 2040000000000 mojos                                                │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1hs0kud8mc4tdy7djugv872mjw804gzfx7g0hfcnt5gfv0zjkhxus4ugkkf     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 500000/2500000000000                                               │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

❯ chia wallet show -f $partial_fp
Wallet height: 6450346
...

Chia Wallet:
   -Total Balance:         0.859999999999 xch (859999999999 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         908.0  (908000 mojo)
   ...
   -Asset ID:              db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
   -Wallet ID:             2

SBX:
   -Total Balance:         80.0  (80000 mojo)
   ...
   -Wallet ID:             3
```

- [clawback spend bundle](./clawback.json)
- [xch.events](https://xch.events/transactions/cb2f22fdfc8e08b568715f4db1520f7d2002c723e7efae5b32bc386d9c673ea4)