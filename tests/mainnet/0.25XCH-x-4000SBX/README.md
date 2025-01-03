# Offer 0.25 XCH for 4000 SBX
```bash
❯ chia wallet show -f $partial_fp
Wallet height: 6441065
...

Chia Wallet:
   -Total Balance:         0.4982931 xch (498293100000 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         500.003  (500003 mojo)
   ...
   -Wallet ID:             2

SBX:
   -Total Balance:         0.0  (0 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3
```

## Create
```bash
❯ partial create -f $partial_fp --offer 1:0.25 --request 3:4000 -p 0.25XCH-x-4000SBX.offer
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                   │ Yes                                                                │
│ MOD_HASH:                │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name: │ 0x71403e46cc37278e0548f6fdaf7365e63e938a0ee34ee9f250fda4f985aafd4c │
│ Clawback Puzzle Hash:    │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:          │ XCH                                                                │
│ Request Asset Id:        │ 0xa628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913 │
│ Offer Amount:            │ 0.25 XCH                                                           │
│ Request Amount:          │ 4000.0 SBX                                                         │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:           │ xch1huqy2mulanmlk4m9rvxfnnsnhkwjsk8fkxgwcdem59vvn2vnfedqhlgarh     │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯

The partial offer file is 0.25XCH-x-4000SBX.offer
```
- [0.25XCH-x-4000SBX.offer](0.25XCH-x-4000SBX.offer)

### Show
```bash
❯ partial show ./0.25XCH-x-4000SBX.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x71403e46cc37278e0548f6fdaf7365e63e938a0ee34ee9f250fda4f985aafd4c │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ XCH                                                                │
│ Request Asset Id:            │ 0xa628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913 │
│ Offer Amount:                │ 250000000000 mojos                                                 │
│ Request Amount:              │ 4000000 mojos                                                      │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1huqy2mulanmlk4m9rvxfnnsnhkwjsk8fkxgwcdem59vvn2vnfedqhlgarh     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 250000000000/4000000                                               │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯
```
## Take
```bash
❯ chia wallet show -f $partial_taker_fp
Wallet height: 6441087
...

Chia Wallet:
   -Total Balance:         0.475 xch (475000000000 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         499.997  (499997 mojo)
   ...
   -Wallet ID:             2

SBX:
   -Total Balance:         303.467  (303467 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3

❯ partial take -f $partial_taker_fp -a (0.005e12) -m (1) ./0.25XCH-x-4000SBX.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x71403e46cc37278e0548f6fdaf7365e63e938a0ee34ee9f250fda4f985aafd4c │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ XCH                                                                │
│ Request Asset Id:            │ 0xa628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913 │
│ Offer Amount:                │ 250000000000 mojos                                                 │
│ Request Amount:              │ 4000000 mojos                                                      │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1huqy2mulanmlk4m9rvxfnnsnhkwjsk8fkxgwcdem59vvn2vnfedqhlgarh     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 250000000000/4000000                                               │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

 80 SBX -> 0.005 XCH
 Sending 80 SBX
 Paying 0.00005 XCH in fees
 Receiving 0.00495 XCH
 ...

 ❯ chia wallet show -f $partial_taker_fp
Wallet height: 6441214
...

Chia Wallet:
   -Total Balance:         0.479949999999 xch (479949999999 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         499.997  (499997 mojo)
   ...
   -Wallet ID:             2

SBX:
   -Total Balance:         223.467  (223467 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3

❯ chia wallet show -f $partial_fp
Wallet height: 6441216
...

Chia Wallet:
   -Total Balance:         0.2482931 xch (248293100000 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         500.003  (500003 mojo)
   ...
   -Wallet ID:             2

SBX:
   -Total Balance:         80.0  (80000 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3
```

- [spend bundle](1st-take-sb.json)
- [after 1st take offer](after-1st-take.offer)
- [xch.events](https://xch.events/transactions/eabb871ef4e11df9b47f9e7855294fcc2d4c4a0842c887d21590fa5a18d4ed86)

## Clawback
```bash
❯ partial show ./after-1st-take.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x6ce418ef8fb9860d94a3f3b6c5dfab79f723e139d171cce4d1a468e71f3086be │
│ Clawback Puzzle Hash:        │ 0x47e04fc9e399fe1a5af83fa82e61df7993ed79d0cf7c03809ac0f8b47ef7da0f │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ XCH                                                                │
│ Request Asset Id:            │ 0xa628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913 │
│ Offer Amount:                │ 245000000000 mojos                                                 │
│ Request Amount:              │ 3920000 mojos                                                      │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ xch1huqy2mulanmlk4m9rvxfnnsnhkwjsk8fkxgwcdem59vvn2vnfedqhlgarh     │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 250000000000/4000000                                               │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

❯ partial clawback -f $partial_fp -m (1) ./after-1st-take.offer
...
❯ chia wallet show -f $partial_fp
Wallet height: 6441247
...

Chia Wallet:
   -Total Balance:         0.493293099999 xch (493293099999 mojo)
   ...
   -Wallet ID:             1

DBX:
   -Total Balance:         500.003  (500003 mojo)
   ...
   -Wallet ID:             2

SBX:
   -Total Balance:         80.0  (80000 mojo)
   ...
   -Asset ID:              a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913
   -Wallet ID:             3
```
- [clawback.json](clawback.json)
- [xch.events](https://xch.events/transactions/c0c57cb092c60e29f18d3eba3468d2cd54704774dbb103ca3a176be51fe45b9f)
