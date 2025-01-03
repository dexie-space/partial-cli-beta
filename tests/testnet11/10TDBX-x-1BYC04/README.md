# Offer 10 TDBX for 1 BYC04
## Create
```bash
❯ chia wallet show -f $partial_fp
Wallet height: 1840772
...

Chia Wallet:
   -Total Balance:         4.335289549398 txch (4335289549398 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         34.2  (34200 mojo)
   ...
   -Asset ID:              d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad
   -Wallet ID:             2

BYC04:
   -Total Balance:         2.987  (2987 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3

❯ partial create -f $partial_fp --offer 2:10 --request 3:1 -p 10TDBX-x-1BYC04.offer
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                   │ Yes                                                                │
│ MOD_HASH:                │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name: │ 0xff07ecc74df7922d01e5013f4e08ee8cfa9e8d7c568618141491a6253baf364d │
│ Clawback Puzzle Hash:    │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:          │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Request Asset Id:        │ 0x4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90 │
│ Offer Amount:            │ 10.0 TDBX                                                          │
│ Request Amount:          │ 1.0 BYC04                                                          │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:           │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯

The partial offer file is 10TDBX-x-1BYC04.offer
```
- [10TDBX-x-1BYC04.offer](10TDBX-x-1BYC04.offer)

## Show
```bash
❯ partial show ./10TDBX-x-1BYC04.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0xff07ecc74df7922d01e5013f4e08ee8cfa9e8d7c568618141491a6253baf364d │
│ Clawback Puzzle Hash:        │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Request Asset Id:            │ 0x4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90 │
│ Offer Amount:                │ 10000 mojos                                                        │
│ Request Amount:              │ 1000 mojos                                                         │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 10000/1000                                                         │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯
```

## Take
```bash
❯ chia wallet show -f $partial_taker_fp
Wallet height: 1840784
...

Chia Wallet:
   -Total Balance:         2.171993949997 txch (2171993949997 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         965.8  (965800 mojo)
   ...
   -Asset ID:              d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad
   -Wallet ID:             2

BYC04:
   -Total Balance:         4.95  (4950 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3

❯ partial take -f $partial_taker_fp -a (6.42e3) -m (1e6) ./10TDBX-x-1BYC04.offer
╭──────────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ Valid:                       │ Yes                                                                │
│ MOD_HASH:                    │ 0x85cd51da98e194894a7b7cd32b6a3d51c57b79fb2f990294c61ca8a7a96f1486 │
│ Partial Offer Coin Name:     │ 0xff07ecc74df7922d01e5013f4e08ee8cfa9e8d7c568618141491a6253baf364d │
│ Clawback Puzzle Hash:        │ 0xfa88ad7547a42d0d81f3781245586ddc4893f8e7124056927c565d797c49a66b │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Offer Asset Id:              │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Request Asset Id:            │ 0x4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90 │
│ Offer Amount:                │ 10000 mojos                                                        │
│ Request Amount:              │ 1000 mojos                                                         │
├──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Fee Recipient:               │ txch1mg7xl5vj4ldsuvcckz6ymkcsy4n0agj3ua8gzdd7yvtlfegzpzjqh9qcuz    │
│ Fee Rate:                    │ 1.0%                                                               │
│ Initial Offer/Request Mojos: │ 10000/1000                                                         │
╰──────────────────────────────┴────────────────────────────────────────────────────────────────────╯

 0.642 BYC04 -> 6.42 TDBX
 Sending 0.642 BYC04
 Paying 0.064 TDBX in fees
 Receiving 6.356 TDBX
...

❯ chia wallet show -f $partial_taker_fp
Wallet height: 1840802
Sync status: Synced
Balances, fingerprint: 819381847

Chia Wallet:
   -Total Balance:         2.171992949997 txch (2171992949997 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         972.156  (972156 mojo)
   ...
   -Asset ID:              d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad
   -Wallet ID:             2

BYC04:
   -Total Balance:         4.308  (4308 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3

❯ chia wallet show -f $partial_fp
Wallet height: 1840808
...

Chia Wallet:
   -Total Balance:         4.335289549398 txch (4335289549398 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         24.2  (24200 mojo)
   ...
   -Asset ID:              d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad
   -Wallet ID:             2

BYC04:
   -Total Balance:         3.629  (3629 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3
```

- [spend bundle](./1st-take-sb.json)
- [after 1st take offer](./after-1st-take.offer)

## Clawback
```bash
❯ partial clawback -f $partial_fp -m (1e6) ./after-1st-take.offer
...

❯ chia wallet show -f $partial_fp
Wallet height: 1841726
Sync status: Synced
Balances, fingerprint: 159051227

Chia Wallet:
   -Total Balance:         4.335288549398 txch (4335288549398 mojo)
   ...
   -Wallet ID:             1

TDBX:
   -Total Balance:         27.78  (27780 mojo)
   ...
   -Asset ID:              d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad
   -Wallet ID:             2

BYC04:
   -Total Balance:         3.629  (3629 mojo)
   ...
   -Asset ID:              4eadfa450c19fa51df65eb7fbf5b61077ec80ec799a7652bb187b705bff19a90
   -Wallet ID:             3
```

