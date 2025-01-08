# Offer 0.5 TXCH for 171 TDBX
```bash
❯ chia wallet show -f $partial_fp
...

Chia Wallet:
   -Total Balance:         3.435290549398 txch (3435290549398 mojo)
   ...
   -Type:                  STANDARD_WALLET
   -Wallet ID:             1

TDBX:
   -Total Balance:         0.0  (0 mojo)
   ...
   -Type:                  CAT
   -Asset ID:              d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad
   -Wallet ID:             2

BYC04:
   ...
   -Wallet ID:             3

...
```

## Create
```bash
❯ partial create -f $partial_fp --offer 1:0.5 --request 2:171 -p 0.5XCH-x-171DBX.offer
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                   │ Yes                                                                │
│ MOD_HASH:                │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name: │ 0x0876297fb3ecff07e2300abe81df7d19978c3287c34f91427240a2ed5fca1ba4 │
│ Clawback Puzzle Hash:    │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:          │ XCH                                                                │
│ Request Asset Id:        │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Offer Amount:            │ 0.5 XCH                                                            │
│ Request Amount:          │ 171.0 TDBX                                                         │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:           │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯

The partial offer file is 0.5XCH-x-171DBX.offer
```
- [0.5XCH-x-171DBX.offer](0.5XCH-x-171DBX.offer)

## Show
```bash
❯ partial show ./0.5XCH-x-171DBX.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x0876297fb3ecff07e2300abe81df7d19978c3287c34f91427240a2ed5fca1ba4 │
│ Clawback Puzzle Hash:        │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ XCH                                                                │
│ Request Asset Id:            │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Offer Amount:                │ 500000000000 mojos                                                 │
│ Request Amount:              │ 171000 mojos                                                       │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 500000000000/171000                                                │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯
```
## Take
```bash
❯ chia wallet show -f $partial_taker_fp
Wallet height: 1827928
...

Chia Wallet:
   -Total Balance:         3.072996949997 txch (3072996949997 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         1000.0  (1000000 mojo)
   ...
   -Asset ID:              d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad
   -Wallet ID:             2

BYC04:
   ...
   -Wallet ID:             3

❯ partial take -f $partial_taker_fp -a $(0.1e12) -m (1e6) ./0.5XCH-x-171DBX.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x0876297fb3ecff07e2300abe81df7d19978c3287c34f91427240a2ed5fca1ba4 │
│ Clawback Puzzle Hash:        │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ XCH                                                                │
│ Request Asset Id:            │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Offer Amount:                │ 500000000000 mojos                                                 │
│ Request Amount:              │ 171000 mojos                                                       │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 500000000000/171000                                                │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

 34.2 TDBX -> 0.1 XCH
 Sending 34.2 TDBX
 Paying 0.001 XCH in fees
 Receiving 0.099 XCH
 ...

 ❯ chia wallet show -f $partial_taker_fp
Wallet height: 1827935
...
Chia Wallet:
   -Total Balance:         3.171995949997 txch (3171995949997 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         965.8  (965800 mojo)
   ...
   -Asset ID:              d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad
   -Wallet ID:             2

BYC04:
   ...
   -Wallet ID:             3

❯ chia wallet show -f $partial_fp
Wallet height: 1827947
...

Chia Wallet:
   -Total Balance:         2.935290549398 txch (2935290549398 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         34.2  (34200 mojo)
   ...
   -Asset ID:              d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad
   -Wallet ID:             2

BYC04:
   ...
   -Wallet ID:             3
```
- [spend bundle](1st-take-sb.json)
- [after 1st take offer](after-1st-take.offer)

```bash
❯ partial show ./after-1st-take.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x11f4ae01c28ea7f0db2825fd245d58c0afbb21a60828bca2443761301d23339f │
│ Clawback Puzzle Hash:        │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ XCH                                                                │
│ Request Asset Id:            │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Offer Amount:                │ 400000000000 mojos                                                 │
│ Request Amount:              │ 136800 mojos                                                       │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 500000000000/171000                                                │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯
```
## Clawback
```bash
❯ partial clawback -f $partial_fp -m (1e6) ./after-1st-take.offer
...

❯ chia wallet show -f $partial_fp
Wallet height: 1828030
Sync status: Synced
Balances, fingerprint: 159051227

Chia Wallet:
   -Total Balance:         3.335289549398 txch (3335289549398 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         34.2  (34200 mojo)
   ...
   -Wallet ID:             2

BYC04:
   ...
   -Wallet ID:             3
```
- [clawback spend bundle](./tests/testnet11/0.5TXCH-x-171TDBX/clawback.json)