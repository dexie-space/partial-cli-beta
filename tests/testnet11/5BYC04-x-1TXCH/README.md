# Offer 5 BYC04 for 1 TXCH
## Create
```bash
❯ chia wallet show -f $partial_fp
Wallet height: 1835297
Sync status: Synced
Balances, fingerprint: 159051227

Chia Wallet:
   -Total Balance:         3.335289549398 txch (3335289549398 mojo)
   ...
   -Wallet ID:             1

TDBX:
   ...
   -Wallet ID:             2

BYC04:
   -Total Balance:         7.987  (7987 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3


❯ partial create -f $partial_fp --offer 4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90:5 --request 1:1
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                   │ Yes                                                                │
│ MOD_HASH:                │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name: │ 0xa5eb21eb36c09b5b94504a68828813f423cc73589ccc6fd7b33552e7c5219ef3 │
│ Clawback Puzzle Hash:    │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:          │ 0x4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90 │
│ Request Asset Id:        │ XCH                                                                │
│ Offer Amount:            │ 5.0 BYC04                                                          │
│ Request Amount:          │ 1.0 XCH                                                            │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:           │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯

The partial offer file is /Users/karlkim/dexie/partial-cli-private/5BYC04-x-1XCH.offer
```
- [5BYC04-x-1XCH.offer](5BYC04-x-1XCH.offer)

## Show
```bash
❯ partial show ./5BYC04-x-1XCH.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0xa5eb21eb36c09b5b94504a68828813f423cc73589ccc6fd7b33552e7c5219ef3 │
│ Clawback Puzzle Hash:        │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0x4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90 │
│ Request Asset Id:            │ XCH                                                                │
│ Offer Amount:                │ 5000 mojos                                                         │
│ Request Amount:              │ 1000000000000 mojos                                                │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 5000/1000000000000                                                 │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯
```

## Take
```bash
❯ chia wallet show -f $partial_taker_fp
Wallet height: 1835451
Sync status: Synced
Balances, fingerprint: 819381847

Chia Wallet:
   -Total Balance:         3.171995949997 txch (3171995949997 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         965.8  (965800 mojo)
   ...
   -Wallet ID:             2

BYC04:
   -Total Balance:         0.0  (0 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3

❯ partial take -f $partial_taker_fp -a (1e3) -m (1e6) ./5BYC04-x-1XCH.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0xa5eb21eb36c09b5b94504a68828813f423cc73589ccc6fd7b33552e7c5219ef3 │
│ Clawback Puzzle Hash:        │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0x4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90 │
│ Request Asset Id:            │ XCH                                                                │
│ Offer Amount:                │ 5000 mojos                                                         │
│ Request Amount:              │ 1000000000000 mojos                                                │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 5000/1000000000000                                                 │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

 0.2 XCH -> 1.0 BYC04
 Sending 0.2 XCH
 Paying 0.01 BYC04 in fees
 Receiving 0.99 BYC04
 ...

 ❯ chia wallet show -f $partial_taker_fp
Wallet height: 1835494
...

Chia Wallet:
   -Total Balance:         2.971994949997 txch (2971994949997 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         965.8  (965800 mojo)
   ...
   -Wallet ID:             2

BYC04:
   -Total Balance:         0.99  (990 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3

❯ chia wallet show -f $partial_fp
Wallet height: 1835504
...

Chia Wallet:
   -Total Balance:         3.535289549398 txch (3535289549398 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         34.2  (34200 mojo)
   ...
   -Wallet ID:             2

BYC04:
   -Total Balance:         2.987  (2987 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3
```

- [spend bundle](1st-take-spend-bundle.json)
- [after 1st take offer](after-1st-take.offer)

```bash
❯ partial show ./after-1st-take.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x7028f41213c15d8e2decd829af87b7eed1ed90f8f127dc6007b8e78c7b4c26cf │
│ Clawback Puzzle Hash:        │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0x4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90 │
│ Request Asset Id:            │ XCH                                                                │
│ Offer Amount:                │ 4000 mojos                                                         │
│ Request Amount:              │ 800000000000 mojos                                                 │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 5000/1000000000000                                                 │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯
```

## Take all BYC04
```bash
❯ partial take -f $partial_taker_fp -a (4e3) -m (1e6) ./after-1st-take.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0x7028f41213c15d8e2decd829af87b7eed1ed90f8f127dc6007b8e78c7b4c26cf │
│ Clawback Puzzle Hash:        │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0x4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90 │
│ Request Asset Id:            │ XCH                                                                │
│ Offer Amount:                │ 4000 mojos                                                         │
│ Request Amount:              │ 800000000000 mojos                                                 │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 5000/1000000000000                                                 │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

 0.8 XCH -> 4.0 BYC04
 Sending 0.8 XCH
 Paying 0.04 BYC04 in fees
 Receiving 3.96 BYC04
 ...

 ❯ chia wallet show -f $partial_taker_fp
Wallet height: 1835523
...

Chia Wallet:
   -Total Balance:         2.171993949997 txch (2171993949997 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         965.8  (965800 mojo)
   ...
   -Wallet ID:             2

BYC04:
   -Total Balance:         4.95  (4950 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3

❯ chia wallet show -f $partial_fp
Wallet height: 1835545
Sync status: Synced
Balances, fingerprint: 159051227

Chia Wallet:
   -Total Balance:         4.335289549398 txch (4335289549398 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         34.2  (34200 mojo)
   ...
   -Wallet ID:             2

BYC04:
   -Total Balance:         2.987  (2987 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3
 ```

- [2nd spend bundle](2nd-take-all-sb.json)