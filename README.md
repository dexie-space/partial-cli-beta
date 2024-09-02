[Partial Offer Coin (PoC)](https://github.com/dexie-space/dexie-governance/issues/12)

# commands
## launch or create a new partial offer
```
❯ partial create --help

 Usage: partial create [OPTIONS]

 create a partial offer requesting CAT token

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --fingerprint  -f  INTEGER  Set the fingerprint to specify which wallet to use [required]      │
│ *  --offer        -o  TEXT     A wallet id to offer and the amount to offer (formatted like       │
│                                wallet_id:amount). Support XCH only                                │
│                                [required]                                                         │
│ *  --request      -r  TEXT     A wallet id of an asset to receive and the amount you wish to      │
│                                receive (formatted like wallet_id:amount). Support CAT only        │
│                                [required]                                                         │
│    --filepath     -p  FILE     The path to write the generated offer file to                      │
│    --help                      Show this message and exit.                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## take the partial offer
```
❯ partial take --help

 Usage: partial take [OPTIONS] PARTIAL_OFFER_FILE

 Take the dexie partial offer by providing the taker offer file or request information.

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --fingerprint    -f  INTEGER   Set the fingerprint to specify which wallet to use [required]   │
│    --offer-file     -o  FILENAME  Taker offer file                                                │
│    --request-mojos  -a  UINT64    Request XCH amount in mojos                                     │
│    --fee            -m  TEXT      The blockchain fee to use when taking the partial offer, in     │
│                                   mojos                                                           │
│                                   [default: 0]                                                    │
│    --help                         Show this message and exit.                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## clawback the partial offer
```
❯ partial clawback --help

 Usage: partial clawback [OPTIONS] OFFER_FILE

 clawback the partial offer coin.

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --fingerprint  -f  INTEGER  Set the fingerprint to specify which wallet to use [required]      │
│    --fee          -m  UINT64   The blockchain fee to use when clawing back the partial offer, in  │
│                                mojos                                                              │
│                                [default: 0]                                                       │
│    --help                      Show this message and exit.                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯

```

# Testnet scenario

1. create a partial offfer, offer 0.5 TXCH for 150 TDBX (300)

```bash
❯ partial create -f $partial_fp --offer 1:0.5 --request d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad:150 | jq
{
  "partial_info": {
    "fee_puzzle_hash": "da3c6fd192afdb0e3318b0b44ddb102566fea251e74e8135be2317f4e50208a4",
    "fee_rate": 100,
    "maker_puzzle_hash": "3e8641ffd4808f666d7efa2539d0071d2e646115d153a8bde352a4e34586d348",
    "public_key": "8049a7369adf936b3ad73c88fc6abd3d172d1ea1661f7d6597842152c2652966ac6a9b93653124cd93bd9a769a039275",
    "tail_hash": "d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad",
    "cat_offer_mod_hash": "97e06ce07905686dbce24559b9691fdcbadf400da9cc7675c35d8beb87301974",
    "rate": 300000,
    "offer_mojos": 500000000000
  },
  "partial_coin": {
    "parent_coin_info": "0xb7f0e809bf950d20c29bcf7545bc6dcbfac49c68e78190fcf415f6943d76e0d5",
    "puzzle_hash": "0x7d69896b660c221b931dc5db6626e8647443fdc0365c72ad3de0964bfb3cbe43",
    "amount": 500000000000
  },
  "launcher_coin": {
    "parent_coin_info": "0xafc3b2d43f72791d6fb8cf8ac1d0cc462319b2fc40e9cbc07f99e7051d1092a9",
    "puzzle_hash": "0x3e8641ffd4808f666d7efa2539d0071d2e646115d153a8bde352a4e34586d348",
    "amount": 1000000000000
  },
  "offer": "offer1qqr83wcuu2ryhhvetd5fg3c5clts0z29d93nr2x5skcxy293arwx003kk82k66e0k3ywcka4e0x8wekguepxflfzum3vv96r9j6sktdy5e3t4pwc923vd9yzyqg6m46j4ajyh2d7dzp5fywk2g5ds7he82am2znaa9a7wctqpmnlel3nu7wgrq2fysfdxrsuru4mmx8tffmpewhsl6ccke6lt5u8lmx7fvmm7w76xu6r202elhgeue0ae03a9e5zd08llwfghpvf2hqzhtnd96kauwf56gun4l6yl08xrym54wa2zw8aa20l7ul7uzncw36902thutjl6vcw5a8wml9qhz38auw5lcuh26cxa0rduhg6zkm9alnvcl6skn6aa9ldp7x87ga47h2trw5gg45qw934c0pu2ra484lvkyr6wzsmemx63kec7nr0pu9hyaaw4r7dlhke6ka88lkrnccar03xy4wdmn7w6nmxu7malm8ulhhwtpgnh7md8uvnmwt4p53lne8s64ul740rgtnwefhx6adn2t8he8pu08zathvq9p7ll2zcj0daw7r47rxmkr286tced299dyspr37mcphvekkv82wchv469hlxvej0efvmlmhvaeht8xtxhklrnatud59rgrv9qvwppmwqyp9jj4sxr8rqqrzxss97rtpxr3duntxzjsd5k2yk3evcuzzjn2jea2advpen4v57sugl9pnkm4488l6k5ftqnp5aqwnfqujzpzgdv7f5p5qzrzvptrqsf3suxzn45xdsjsfu6tr9tsy6qny4jht8tx4kdjvxnd2avk3yytxsj29ypqct4qc9fqay59fzu9x6qqzjcztq4wc3pkzfzq7fpzs3e3y5spp8sygd47c9cerh9zsfpvs6qp3u6re3qrvgu3ju2jr8mv0zwjc3qpzfm5j7jguv22988mxy7r9vxqzg85w6fdvk5dr486z3ueevc5mrgk3pp4jkp29rfjrhx03la5wlpzqufz95g6y3psgp0l4uy66ggu0wwuns9mxqc7pkxzyppmp9qzkfg09yzxttjjjqspaj22rgwfdq4q70e7sljktgaaw7eng78vtf700mmazljl7kzt649mww3248za7njml9jdena0vkrmulr0dxd9pmmatm8ul43l7ynh5gwr9mlfm00qhxrhea0a5fc9v6tfz6ld6m56n9w8d5qjm703n5aa57n09qlrp7twu8mlh8axn686jl7cttu7rtynwrpwvchec2hxfhh30v87a7tlmpwnxc7nfst97fj3"
}
```

2. display the partial offer information
```bash
❯ partial show ./launcher-ceb5eb165f8004daf94c107900b7e97c02b887f78f67fb683643b77b86107e1a.offer
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ MOD_HASH:                │ 0x5a3875e000ab384ac01cdf8c272509f02845ba0a87fe1b8d267ba7cd7e2c807b │
│ Valid:                   │ Yes                                                                │
│ Partial Offer Coin Name: │ 0xdf5c0291ae78b67ee7d1d290883c834a2d7a58ce2e6cf6b407e0d1ea0774b9b8 │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Total Offer Amount:      │ 0.5 XCH                                                            │
│ Total Request Amount:    │ 150.0 CATs                                                         │
│ Request Tail Hash:       │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Rate (1 XCH):            │ 300.0 CATs                                                         │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯
```

3. take 0.2 TXCH from the partial offer.
```bash
❯ partial take -f $partial_taker_fp -a $(0.2e12) -m 1000 ./launcher-ceb5eb165f8004daf94c107900b7e97c02b887f78f67fb683643b77b86107e1a.offer
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ MOD_HASH:                │ 0x5a3875e000ab384ac01cdf8c272509f02845ba0a87fe1b8d267ba7cd7e2c807b │
│ Valid:                   │ Yes                                                                │
│ Partial Offer Coin Name: │ 0xdf5c0291ae78b67ee7d1d290883c834a2d7a58ce2e6cf6b407e0d1ea0774b9b8 │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Total Offer Amount:      │ 0.5 XCH                                                            │
│ Total Request Amount:    │ 150.0 CATs                                                         │
│ Request Tail Hash:       │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Rate (1 XCH):            │ 300.0 CATs                                                         │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯

 60.0 CATs -> 0.2 XCH
 Sending 60.0 CATs
 Paying 0.002 XCH in fees
 Receiving 0.198 XCH

 Would you like to take this offer? [y/n]: y
{
  "spend_bundle": {
    "coin_spends": [
      {
        "coin": {
          "parent_coin_info": "0xafc3b2d43f72791d6fb8cf8ac1d0cc462319b2fc40e9cbc07f99e7051d1092a9",
          "puzzle_hash": "0x3e8641ffd4808f666d7efa2539d0071d2e646115d153a8bde352a4e34586d348",
          "amount": 1000000000000
        },
        "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b0b0a5d47cd344ae08bb22c69d8ca0422a2be7ae14265c9626b25b2f748f89da9f9be5cf0fdb7afe3df941f8b3e1436264ff018080",
        "solution": "0xff80ffff01ffff3dffa0bb8820e27911b2fec68f76cd082678994a9e9ec9c47b2ac117f254ebc78e7bc880ffff3cffa00715177eef97117e98e975f5fbda23d3f06d33bdc5982e333286bd7e229e10cc80ffff33ffa07d69896b660c221b931dc5db6626e8647443fdc0365c72ad3de0964bfb3cbe43ff85746a528800ffff8d64657869655f7061727469616cffc20b7b226665655f70757a7a6c655f68617368223a202264613363366664313932616664623065333331386230623434646462313032353636666561323531653734653831333562653233313766346535303230386134222c20226665655f72617465223a203130302c20226d616b65725f70757a7a6c655f68617368223a202233653836343166666434383038663636366437656661323533396430303731643265363436313135643135336138626465333532613465333435383664333438222c20227075626c69635f6b6579223a2022383034396137333639616466393336623361643733633838666336616264336431373264316561313636316637643635393738343231353263323635323936366163366139623933363533313234636439336264396137363961303339323735222c20227461696c5f68617368223a202264383264643033663861396164326638343335336364393533633464653662323164626161663764653362613366346464643961626533316563626138306164222c20226361745f6f666665725f6d6f645f68617368223a202239376530366365303739303536383664626365323435353962393639316664636261646634303064613963633736373563333564386265623837333031393734222c202272617465223a203330303030302c20226f666665725f6d6f6a6f73223a203530303030303030303030307d8080ffff33ffa03e8641ffd4808f666d7efa2539d0071d2e646115d153a8bde352a4e34586d348ff85746a5288008080ff8080"
      },
      {
        "coin": {
          "parent_coin_info": "0xb7f0e809bf950d20c29bcf7545bc6dcbfac49c68e78190fcf415f6943d76e0d5",
          "puzzle_hash": "0x7d69896b660c221b931dc5db6626e8647443fdc0365c72ad3de0964bfb3cbe43",
          "amount": 500000000000
        },
        "puzzle_reveal": "0xff02ffff01ff02ffff01ff04ffff04ffff013cffff04ff2fff808080ffff04ffff04ffff0149ffff04ff8202ffff808080ffff02ffff03ffff15ff820bffff8080ffff01ff04ffff04ffff0146ffff04ff8205ffff808080ffff04ffff02ff1affff04ff02ffff04ff2fffff04ff8200bfffff04ff8205ffffff04ffff02ff3cffff04ff02ffff04ff82017fffff04ff820bffff8080808080ff80808080808080ffff04ffff02ff16ffff04ff02ffff04ffff11ff820bffffff02ff12ffff04ff02ffff04ff17ffff04ff820bffff808080808080ff80808080ffff04ffff04ffff0133ffff04ff0bffff04ffff02ff12ffff04ff02ffff04ff17ffff04ff820bffff8080808080ff80808080ffff02ffff03ffff15ffff11ff8202ffff820bff80ff8080ffff01ff04ffff02ff2effff04ff02ffff04ff05ffff04ff0bffff04ff17ffff04ff2fffff04ff5fffff04ff8200bfffff04ff82017fffff04ffff11ff8202ffff820bff80ff8080808080808080808080ff8080ffff01ff018080ff018080808080ffff01ff02ff3effff04ff02ffff04ff2fffff04ff5fffff04ff8202ffffff04ff8217ffff8080808080808080ff01808080ffff04ffff01ffffffff02ffff03ff05ffff01ff02ff10ffff04ff02ffff04ff0dffff04ffff0bffff0102ffff0bffff0101ffff010480ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0980ffff0bffff0102ff0bffff0bffff0101ff8080808080ff8080808080ffff010b80ff0180ff0bffff0102ffff0bffff0101ffff010280ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0580ffff0bffff0102ffff02ff10ffff04ff02ffff04ff07ffff04ffff0bffff0101ffff010180ff8080808080ffff0bffff0101ff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff14ffff04ff02ffff04ff09ff80808080ffff02ff14ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ffff02ffff03ff0bffff01ff02ff2cffff04ff02ffff04ffff02ffff03ff13ffff01ff04ff13ff0580ffff010580ff0180ffff04ff1bff8080808080ffff010580ff0180ff05ffff14ffff12ff05ff0b80ffff018600e8d4a510008080ffffff05ffff14ffff12ff05ff0b80ffff018227108080ff04ffff013fffff04ffff0bffff02ff18ffff04ff02ffff04ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7affff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ffff0bffff0101ff0b80ffff04ffff0bffff0101ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7a80ff80808080808080ffff02ff14ffff04ff02ffff04ffff04ff17ffff04ffff04ff05ffff04ff2fffff04ffff04ff05ff8080ff80808080ff808080ff8080808080ff808080ffff04ffff0133ffff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ff05ff80808080ffff04ffff0133ffff04ffff02ff18ffff04ff02ffff04ff05ffff04ffff0bffff0101ff8202ff80ffff04ffff0bffff0101ff82017f80ffff04ffff0bffff0101ff8200bf80ffff04ffff0bffff0101ff5f80ffff04ffff0bffff0101ff2f80ffff04ffff0bffff0101ff1780ffff04ffff0bffff0101ff0b80ffff04ffff0bffff0101ff0580ff808080808080808080808080ffff04ff8202ffff80808080ff02ff2cffff04ff02ffff04ff80ffff04ffff04ffff04ffff0133ffff04ff05ffff04ffff11ff17ff2f80ff80808080ffff04ffff04ffff0132ffff04ff0bffff04ffff0bff1780ff80808080ffff04ffff02ffff03ffff15ff2fff8080ffff01ff04ffff0134ffff04ff2fff808080ffff01ff018080ff0180ff80808080ff8080808080ff018080ffff04ffff01a05a3875e000ab384ac01cdf8c272509f02845ba0a87fe1b8d267ba7cd7e2c807bffff04ffff01a0da3c6fd192afdb0e3318b0b44ddb102566fea251e74e8135be2317f4e50208a4ffff04ffff0164ffff04ffff01a03e8641ffd4808f666d7efa2539d0071d2e646115d153a8bde352a4e34586d348ffff04ffff01b08049a7369adf936b3ad73c88fc6abd3d172d1ea1661f7d6597842152c2652966ac6a9b93653124cd93bd9a769a039275ffff04ffff01a0d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80adffff04ffff01830493e0ffff04ffff0185746a528800ff01808080808080808080",
        "solution": "0xffa0df5c0291ae78b67ee7d1d290883c834a2d7a58ce2e6cf6b407e0d1ea0774b9b8ff852e90edd00080"
      },
      {
        "coin": {
          "parent_coin_info": "0xdf5c0291ae78b67ee7d1d290883c834a2d7a58ce2e6cf6b407e0d1ea0774b9b8",
          "puzzle_hash": "0xcfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7",
          "amount": 198000000000
        },
        "puzzle_reveal": "0xff02ffff01ff02ff0affff04ff02ffff04ff03ff80808080ffff04ffff01ffff333effff02ffff03ff05ffff01ff04ffff04ff0cffff04ffff02ff1effff04ff02ffff04ff09ff80808080ff808080ffff02ff16ffff04ff02ffff04ff19ffff04ffff02ff0affff04ff02ffff04ff0dff80808080ff808080808080ff8080ff0180ffff02ffff03ff05ffff01ff02ffff03ffff15ff29ff8080ffff01ff04ffff04ff08ff0980ffff02ff16ffff04ff02ffff04ff0dffff04ff0bff808080808080ffff01ff088080ff0180ffff010b80ff0180ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff1effff04ff02ffff04ff09ff80808080ffff02ff1effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080",
        "solution": "0xffffa01691709fd482c92d6353e1973c50c5cd4c336e63d19633ecdd69c22bc994d661ffffa0cf856df461f4e7b9d2ee82099b23e303e746f4c59f94afcc25d92ab3f737edb1ff852e19b83c00ff80808080"
      },
      {
        "coin": {
          "parent_coin_info": "0x68172f26267ff9990a4f2b786d601de7ce09aa5cba2702344ca43b8f0bc2a223",
          "puzzle_hash": "0x0c7ae0f3a5d6dbe7ec3ef9abbbc21dfd9c659081730417e347d0bf3fb2afd8ec",
          "amount": 1234000
        },
        "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ff5effff04ff02ffff04ffff04ff05ffff04ffff0bff34ff0580ffff04ff0bff80808080ffff04ffff02ff17ff2f80ffff04ff5fffff04ffff02ff2effff04ff02ffff04ff17ff80808080ffff04ffff02ff2affff04ff02ffff04ff82027fffff04ff82057fffff04ff820b7fff808080808080ffff04ff81bfffff04ff82017fffff04ff8202ffffff04ff8205ffffff04ff820bffff80808080808080808080808080ffff04ffff01ffffffff3d46ff02ff333cffff0401ff01ff81cb02ffffff20ff02ffff03ff05ffff01ff02ff32ffff04ff02ffff04ff0dffff04ffff0bff7cffff0bff34ff2480ffff0bff7cffff0bff7cffff0bff34ff2c80ff0980ffff0bff7cff0bffff0bff34ff8080808080ff8080808080ffff010b80ff0180ffff02ffff03ffff22ffff09ffff0dff0580ff2280ffff09ffff0dff0b80ff2280ffff15ff17ffff0181ff8080ffff01ff0bff05ff0bff1780ffff01ff088080ff0180ffff02ffff03ff0bffff01ff02ffff03ffff09ffff02ff2effff04ff02ffff04ff13ff80808080ff820b9f80ffff01ff02ff56ffff04ff02ffff04ffff02ff13ffff04ff5fffff04ff17ffff04ff2fffff04ff81bfffff04ff82017fffff04ff1bff8080808080808080ffff04ff82017fff8080808080ffff01ff088080ff0180ffff01ff02ffff03ff17ffff01ff02ffff03ffff20ff81bf80ffff0182017fffff01ff088080ff0180ffff01ff088080ff018080ff0180ff04ffff04ff05ff2780ffff04ffff10ff0bff5780ff778080ffffff02ffff03ff05ffff01ff02ffff03ffff09ffff02ffff03ffff09ff11ff5880ffff0159ff8080ff0180ffff01818f80ffff01ff02ff26ffff04ff02ffff04ff0dffff04ff0bffff04ffff04ff81b9ff82017980ff808080808080ffff01ff02ff7affff04ff02ffff04ffff02ffff03ffff09ff11ff5880ffff01ff04ff58ffff04ffff02ff76ffff04ff02ffff04ff13ffff04ff29ffff04ffff0bff34ff5b80ffff04ff2bff80808080808080ff398080ffff01ff02ffff03ffff09ff11ff7880ffff01ff02ffff03ffff20ffff02ffff03ffff09ffff0121ffff0dff298080ffff01ff02ffff03ffff09ffff0cff29ff80ff3480ff5c80ffff01ff0101ff8080ff0180ff8080ff018080ffff0109ffff01ff088080ff0180ffff010980ff018080ff0180ffff04ffff02ffff03ffff09ff11ff5880ffff0159ff8080ff0180ffff04ffff02ff26ffff04ff02ffff04ff0dffff04ff0bffff04ff17ff808080808080ff80808080808080ff0180ffff01ff04ff80ffff04ff80ff17808080ff0180ffff02ffff03ff05ffff01ff04ff09ffff02ff56ffff04ff02ffff04ff0dffff04ff0bff808080808080ffff010b80ff0180ff0bff7cffff0bff34ff2880ffff0bff7cffff0bff7cffff0bff34ff2c80ff0580ffff0bff7cffff02ff32ffff04ff02ffff04ff07ffff04ffff0bff34ff3480ff8080808080ffff0bff34ff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff2effff04ff02ffff04ff09ff80808080ffff02ff2effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ffff04ffff04ff30ffff04ff5fff808080ffff02ff7effff04ff02ffff04ffff04ffff04ff2fff0580ffff04ff5fff82017f8080ffff04ffff02ff26ffff04ff02ffff04ff0bffff04ff05ffff01ff808080808080ffff04ff17ffff04ff81bfffff04ff82017fffff04ffff02ff2affff04ff02ffff04ff8204ffffff04ffff02ff76ffff04ff02ffff04ff09ffff04ff820affffff04ffff0bff34ff2d80ffff04ff15ff80808080808080ffff04ff8216ffff808080808080ffff04ff8205ffffff04ff820bffff808080808080808080808080ff02ff5affff04ff02ffff04ff5fffff04ff3bffff04ffff02ffff03ff17ffff01ff09ff2dffff02ff2affff04ff02ffff04ff27ffff04ffff02ff76ffff04ff02ffff04ff29ffff04ff57ffff04ffff0bff34ff81b980ffff04ff59ff80808080808080ffff04ff81b7ff80808080808080ff8080ff0180ffff04ff17ffff04ff05ffff04ff8202ffffff04ffff04ffff04ff78ffff04ffff0eff5cffff02ff2effff04ff02ffff04ffff04ff2fffff04ff82017fff808080ff8080808080ff808080ffff04ffff04ff20ffff04ffff0bff81bfff5cffff02ff2effff04ff02ffff04ffff04ff15ffff04ffff10ff82017fffff11ff8202dfff2b80ff8202ff80ff808080ff8080808080ff808080ff138080ff80808080808080808080ff018080ffff04ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7affff04ffff01a0d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80adffff04ffff01ff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b09231efa63d2e70b666a6099aaf0cc7b7f6f7e40d765811554b75b2eacd38627c6859a2310b2f832a5acb3b7cec31bca1ff018080ff0180808080",
        "solution": "0xffff80ffff01ffff3fffa06e908f7d33f86b99935ce855a941a232d10df34a387a933aaec289cfe6f3e51180ffff3cffa0dd50152ee1cd11e436874dc721203f969e0706c7f181bfeb8fe3ca2e3757837e80ffff33ffa0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ff8300ea60ffffa0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e78080ffff33ffa0cf856df461f4e7b9d2ee82099b23e303e746f4c59f94afcc25d92ab3f737edb1ff8311e9f0ffffa0cf856df461f4e7b9d2ee82099b23e303e746f4c59f94afcc25d92ab3f737edb1808080ff8080ffffa02af91b0ccd7a6e5279944064201e4ff34d5481830e925cae9860c9e9ba1231b1ffa0ed8bcc3f1c51c7428b48316c1a92aa2d061dc14f1661088cf687dbfdd58883ebff8338f9f080ffa0ef41f16be118b42ace17f12483ddc30ccc7335bd187d6f78645d40719cfb09acffffa068172f26267ff9990a4f2b786d601de7ce09aa5cba2702344ca43b8f0bc2a223ffa00c7ae0f3a5d6dbe7ec3ef9abbbc21dfd9c659081730417e347d0bf3fb2afd8ecff8312d45080ffffa068172f26267ff9990a4f2b786d601de7ce09aa5cba2702344ca43b8f0bc2a223ffa0cf856df461f4e7b9d2ee82099b23e303e746f4c59f94afcc25d92ab3f737edb1ff8312d45080ff80ff8080"
      },
      {
        "coin": {
          "parent_coin_info": "0xba7d5ae23e9afbb9d7ead5bd634fc7efdedaae047a637f90611c6e35d6ff4d17",
          "puzzle_hash": "0xcf856df461f4e7b9d2ee82099b23e303e746f4c59f94afcc25d92ab3f737edb1",
          "amount": 595383391082
        },
        "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b09231efa63d2e70b666a6099aaf0cc7b7f6f7e40d765811554b75b2eacd38627c6859a2310b2f832a5acb3b7cec31bca1ff018080",
        "solution": "0xff80ffff01ffff3dffa0bfdc4901511704111e7b69a91bc1354c37ee2d32d099802ac6979efe05917b7680ffff3cffa010fde46aefafb3edef98c20be0bfdfbc6d7c8127ce1aea9693e239842942834e80ffff33ffa0cf856df461f4e7b9d2ee82099b23e303e746f4c59f94afcc25d92ab3f737edb1ff86008a9f9d8f8280ffff34ff8203e88080ff8080"
      },
      {
        "coin": {
          "parent_coin_info": "0xef41f16be118b42ace17f12483ddc30ccc7335bd187d6f78645d40719cfb09ac",
          "puzzle_hash": "0x97e06ce07905686dbce24559b9691fdcbadf400da9cc7675c35d8beb87301974",
          "amount": 60000
        },
        "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ff5effff04ff02ffff04ffff04ff05ffff04ffff0bff34ff0580ffff04ff0bff80808080ffff04ffff02ff17ff2f80ffff04ff5fffff04ffff02ff2effff04ff02ffff04ff17ff80808080ffff04ffff02ff2affff04ff02ffff04ff82027fffff04ff82057fffff04ff820b7fff808080808080ffff04ff81bfffff04ff82017fffff04ff8202ffffff04ff8205ffffff04ff820bffff80808080808080808080808080ffff04ffff01ffffffff3d46ff02ff333cffff0401ff01ff81cb02ffffff20ff02ffff03ff05ffff01ff02ff32ffff04ff02ffff04ff0dffff04ffff0bff7cffff0bff34ff2480ffff0bff7cffff0bff7cffff0bff34ff2c80ff0980ffff0bff7cff0bffff0bff34ff8080808080ff8080808080ffff010b80ff0180ffff02ffff03ffff22ffff09ffff0dff0580ff2280ffff09ffff0dff0b80ff2280ffff15ff17ffff0181ff8080ffff01ff0bff05ff0bff1780ffff01ff088080ff0180ffff02ffff03ff0bffff01ff02ffff03ffff09ffff02ff2effff04ff02ffff04ff13ff80808080ff820b9f80ffff01ff02ff56ffff04ff02ffff04ffff02ff13ffff04ff5fffff04ff17ffff04ff2fffff04ff81bfffff04ff82017fffff04ff1bff8080808080808080ffff04ff82017fff8080808080ffff01ff088080ff0180ffff01ff02ffff03ff17ffff01ff02ffff03ffff20ff81bf80ffff0182017fffff01ff088080ff0180ffff01ff088080ff018080ff0180ff04ffff04ff05ff2780ffff04ffff10ff0bff5780ff778080ffffff02ffff03ff05ffff01ff02ffff03ffff09ffff02ffff03ffff09ff11ff5880ffff0159ff8080ff0180ffff01818f80ffff01ff02ff26ffff04ff02ffff04ff0dffff04ff0bffff04ffff04ff81b9ff82017980ff808080808080ffff01ff02ff7affff04ff02ffff04ffff02ffff03ffff09ff11ff5880ffff01ff04ff58ffff04ffff02ff76ffff04ff02ffff04ff13ffff04ff29ffff04ffff0bff34ff5b80ffff04ff2bff80808080808080ff398080ffff01ff02ffff03ffff09ff11ff7880ffff01ff02ffff03ffff20ffff02ffff03ffff09ffff0121ffff0dff298080ffff01ff02ffff03ffff09ffff0cff29ff80ff3480ff5c80ffff01ff0101ff8080ff0180ff8080ff018080ffff0109ffff01ff088080ff0180ffff010980ff018080ff0180ffff04ffff02ffff03ffff09ff11ff5880ffff0159ff8080ff0180ffff04ffff02ff26ffff04ff02ffff04ff0dffff04ff0bffff04ff17ff808080808080ff80808080808080ff0180ffff01ff04ff80ffff04ff80ff17808080ff0180ffff02ffff03ff05ffff01ff04ff09ffff02ff56ffff04ff02ffff04ff0dffff04ff0bff808080808080ffff010b80ff0180ff0bff7cffff0bff34ff2880ffff0bff7cffff0bff7cffff0bff34ff2c80ff0580ffff0bff7cffff02ff32ffff04ff02ffff04ff07ffff04ffff0bff34ff3480ff8080808080ffff0bff34ff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff2effff04ff02ffff04ff09ff80808080ffff02ff2effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ffff04ffff04ff30ffff04ff5fff808080ffff02ff7effff04ff02ffff04ffff04ffff04ff2fff0580ffff04ff5fff82017f8080ffff04ffff02ff26ffff04ff02ffff04ff0bffff04ff05ffff01ff808080808080ffff04ff17ffff04ff81bfffff04ff82017fffff04ffff02ff2affff04ff02ffff04ff8204ffffff04ffff02ff76ffff04ff02ffff04ff09ffff04ff820affffff04ffff0bff34ff2d80ffff04ff15ff80808080808080ffff04ff8216ffff808080808080ffff04ff8205ffffff04ff820bffff808080808080808080808080ff02ff5affff04ff02ffff04ff5fffff04ff3bffff04ffff02ffff03ff17ffff01ff09ff2dffff02ff2affff04ff02ffff04ff27ffff04ffff02ff76ffff04ff02ffff04ff29ffff04ff57ffff04ffff0bff34ff81b980ffff04ff59ff80808080808080ffff04ff81b7ff80808080808080ff8080ff0180ffff04ff17ffff04ff05ffff04ff8202ffffff04ffff04ffff04ff78ffff04ffff0eff5cffff02ff2effff04ff02ffff04ffff04ff2fffff04ff82017fff808080ff8080808080ff808080ffff04ffff04ff20ffff04ffff0bff81bfff5cffff02ff2effff04ff02ffff04ffff04ff15ffff04ffff10ff82017fffff11ff8202dfff2b80ff8202ff80ff808080ff8080808080ff808080ff138080ff80808080808080808080ff018080ffff04ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7affff04ffff01a0d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80adffff04ffff01ff02ffff01ff02ff0affff04ff02ffff04ff03ff80808080ffff04ffff01ffff333effff02ffff03ff05ffff01ff04ffff04ff0cffff04ffff02ff1effff04ff02ffff04ff09ff80808080ff808080ffff02ff16ffff04ff02ffff04ff19ffff04ffff02ff0affff04ff02ffff04ff0dff80808080ff808080808080ff8080ff0180ffff02ffff03ff05ffff01ff02ffff03ffff15ff29ff8080ffff01ff04ffff04ff08ff0980ffff02ff16ffff04ff02ffff04ff0dffff04ff0bff808080808080ffff01ff088080ff0180ffff010b80ff0180ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff1effff04ff02ffff04ff09ff80808080ffff02ff1effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ff0180808080",
        "solution": "0xffffffa0df5c0291ae78b67ee7d1d290883c834a2d7a58ce2e6cf6b407e0d1ea0774b9b8ffffa03e8641ffd4808f666d7efa2539d0071d2e646115d153a8bde352a4e34586d348ff8300ea60ffffa03e8641ffd4808f666d7efa2539d0071d2e646115d153a8bde352a4e34586d34880808080ffffa068172f26267ff9990a4f2b786d601de7ce09aa5cba2702344ca43b8f0bc2a223ffa0cf856df461f4e7b9d2ee82099b23e303e746f4c59f94afcc25d92ab3f737edb1ff8312d45080ffa05b7dcf449018859ddd2934ed76bc66a61df393053ee63ba8ef9165ae8b16aaa8ffffa0ef41f16be118b42ace17f12483ddc30ccc7335bd187d6f78645d40719cfb09acffa097e06ce07905686dbce24559b9691fdcbadf400da9cc7675c35d8beb87301974ff8300ea6080ffffa0ef41f16be118b42ace17f12483ddc30ccc7335bd187d6f78645d40719cfb09acffa0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ff8300ea6080ff80ff8080"
      }
    ],
    "aggregated_signature": "0xb172eea572d2fec1c625a4b10358bce07829d9ea604a5d0682066417c1fc8719be491834f0393bb17841aca1ddc5140a02c327933a0520ba237494d7138515e722bcfaa766142c7d7ab9bf588718d4c1cf046a4f7da90bdf9c16d2e287bd399b"
  },
  "next_offer": "offer1qqr83wcuu2rykcmqvpstc87rx3c4m3dkhtn3wt6dazcxnakj4k9r3fuh7dksh7ur3whasjmkaevweuw48fgv5gzy7heszegp60hvdlmttad53kka7lgf7l03ark5nke7qrxhp0vek2psrhjwsk6uuxtdyzgclz8tl7xfavrysw2v63dp4yd5nfcm9n5n0s8nyf39cryjnsv0vgm9p7sggrfzudqjkl6cjeq3n56qpek4pzhzqetn5snsx9cafhyxfqezqececw9sy0r6uqcspugm8rvlup6fxus0ezp6hn7plgarzk87c3tgmxpxyr3z49pueprkhcdxqdvvr44x33fruhtzvu2y2ypdvq7tzx5wj4gqx4guyysmyszl6emyd9qpzs5jvxzr2l6q5twrqudynpq25d6sxsewzvujz5scnmpkw6udhg825qmzqku290tcscxfx53y30kxne44qxja82ytgpqkzmlq78gdv3z7jd62c0xcyzxp0gy2ey9wvgdu8zetfvz33sqdyq6zjcpl5uqaccyz7nuzqlfcpxz2mrqtenmh6nnc6ldx30rddejdfpxuywcce6crenn6urvvmvva3ddmget2kz42an70u7m0vd7pdhdnuhl24v8nknmlvy3t60ve083dajur3elel5lc49ulywzjxacrf2sp9dqp9xpjzpeq93qu8y3c52fcfgclqn8kz3p6ju26j0phsmrqzgngtzgncqdwxzgt3r849pwgdlwgm3uxfr37xfrmcq2h9zc69exfq6jy9tspyk2upzcjhzd4ngter0wqjs3fdjxpppgdhrwc74yyg99pvl2y08px3qj56npy5qayrgya98sysakfg30fqwrd29j7qajwaaag4de8a5rsmhzatlj0hft667hemyafmpn24ze9kdhezun6m07dvuktzcvtaaksr4d5079s98lmxkdwu5cklleffztrp9z9jzj5k4wehcll9vxl66dewkl4gtf0kr974ffy3f0qch437acapyk84ekew0fqegmrg7pwx7dh2lmjkm2htxuw8avhkmw9whj3dfkf67nyum63psaff25ekcnxhahy23petvun7l8z4x798j53g6h6phwshajakvh06uqw8caat3hhmyndjh0tdv07lvhhh5akh8lpndws66epe2d9jf3lszc95g04zy3jysswxrgpvqqq4qsqy0s544rjj"
}
```

> `next_offer` is the next partial offer (e.g., `001.offer`)

check the taker wallet. `0xc4015e42fbf728ce0c9ae2fc361d541202ec39b072825fd4f0bbd1935983c84d` is the coin we get when taking the partial offer.
```bash
❯ chia wallet coins list -f $partial_taker_fp -i 1
There are a total of 2 coins in wallet 1.
2 confirmed coins.
0 unconfirmed additions.
0 unconfirmed removals.
Confirmed coins:
Coin ID: 0xc4015e42fbf728ce0c9ae2fc361d541202ec39b072825fd4f0bbd1935983c84d
	Address: txch1e7zkmarp7nnmn5hwsgyekglrq0n5dax9n722lnp9my4t8aehakcsuzcmfz Amount: 0.198000000000  (198000000000 mojo), Confirmed in block: 1276530

Coin ID: 0xc14f9e9c13999f1982b60c1ad0e23401abdb65e559d8c2c9744a78ba641a8e91
	Address: txch1e7zkmarp7nnmn5hwsgyekglrq0n5dax9n722lnp9my4t8aehakcsuzcmfz Amount: 0.595383390082  (595383390082 mojo), Confirmed in block: 1276530
```

4. display the next partial offer (i.e., `001.offer`). The partial offer should now have 0.3 TXCH (`0.5-0.2`).
```bash
❯ partial show ./001.offer
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ MOD_HASH:                │ 0x5a3875e000ab384ac01cdf8c272509f02845ba0a87fe1b8d267ba7cd7e2c807b │
│ Valid:                   │ Yes                                                                │
│ Partial Offer Coin Name: │ 0x204774b9f34613844f2da4d48dd513f64f282b928bf25592f3e724726e240ac7 │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Total Offer Amount:      │ 0.3 XCH                                                            │
│ Total Request Amount:    │ 90.0 CATs                                                          │
│ Request Tail Hash:       │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Rate (1 XCH):            │ 300.0 CATs                                                         │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯

```

5. The remaining 0.3 TXCH (minus 1000 mojos) is returned to the maker wallet.
```bash
❯ partial clawback -f $partial_fp -m 1000 001.offer
{
  "coin_spends": [
    {
      "coin": {
        "parent_coin_info": "0xdf5c0291ae78b67ee7d1d290883c834a2d7a58ce2e6cf6b407e0d1ea0774b9b8",
        "puzzle_hash": "0xa348f53b511a305425f3c02310358b81ffadeb38193edf482f9bd1c5db92b6f0",
        "amount": 300000000000
      },
      "puzzle_reveal": "0xff02ffff01ff02ffff01ff04ffff04ffff013cffff04ff2fff808080ffff04ffff04ffff0149ffff04ff8202ffff808080ffff02ffff03ffff15ff820bffff8080ffff01ff04ffff04ffff0146ffff04ff8205ffff808080ffff04ffff02ff1affff04ff02ffff04ff2fffff04ff8200bfffff04ff8205ffffff04ffff02ff3cffff04ff02ffff04ff82017fffff04ff820bffff8080808080ff80808080808080ffff04ffff02ff16ffff04ff02ffff04ffff11ff820bffffff02ff12ffff04ff02ffff04ff17ffff04ff820bffff808080808080ff80808080ffff04ffff04ffff0133ffff04ff0bffff04ffff02ff12ffff04ff02ffff04ff17ffff04ff820bffff8080808080ff80808080ffff02ffff03ffff15ffff11ff8202ffff820bff80ff8080ffff01ff04ffff02ff2effff04ff02ffff04ff05ffff04ff0bffff04ff17ffff04ff2fffff04ff5fffff04ff8200bfffff04ff82017fffff04ffff11ff8202ffff820bff80ff8080808080808080808080ff8080ffff01ff018080ff018080808080ffff01ff02ff3effff04ff02ffff04ff2fffff04ff5fffff04ff8202ffffff04ff8217ffff8080808080808080ff01808080ffff04ffff01ffffffff02ffff03ff05ffff01ff02ff10ffff04ff02ffff04ff0dffff04ffff0bffff0102ffff0bffff0101ffff010480ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0980ffff0bffff0102ff0bffff0bffff0101ff8080808080ff8080808080ffff010b80ff0180ff0bffff0102ffff0bffff0101ffff010280ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0580ffff0bffff0102ffff02ff10ffff04ff02ffff04ff07ffff04ffff0bffff0101ffff010180ff8080808080ffff0bffff0101ff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff14ffff04ff02ffff04ff09ff80808080ffff02ff14ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ffff02ffff03ff0bffff01ff02ff2cffff04ff02ffff04ffff02ffff03ff13ffff01ff04ff13ff0580ffff010580ff0180ffff04ff1bff8080808080ffff010580ff0180ff05ffff14ffff12ff05ff0b80ffff018600e8d4a510008080ffffff05ffff14ffff12ff05ff0b80ffff018227108080ff04ffff013fffff04ffff0bffff02ff18ffff04ff02ffff04ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7affff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ffff0bffff0101ff0b80ffff04ffff0bffff0101ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7a80ff80808080808080ffff02ff14ffff04ff02ffff04ffff04ff17ffff04ffff04ff05ffff04ff2fffff04ffff04ff05ff8080ff80808080ff808080ff8080808080ff808080ffff04ffff0133ffff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ff05ff80808080ffff04ffff0133ffff04ffff02ff18ffff04ff02ffff04ff05ffff04ffff0bffff0101ff8202ff80ffff04ffff0bffff0101ff82017f80ffff04ffff0bffff0101ff8200bf80ffff04ffff0bffff0101ff5f80ffff04ffff0bffff0101ff2f80ffff04ffff0bffff0101ff1780ffff04ffff0bffff0101ff0b80ffff04ffff0bffff0101ff0580ff808080808080808080808080ffff04ff8202ffff80808080ff02ff2cffff04ff02ffff04ff80ffff04ffff04ffff04ffff0133ffff04ff05ffff04ffff11ff17ff2f80ff80808080ffff04ffff04ffff0132ffff04ff0bffff04ffff0bff1780ff80808080ffff04ffff02ffff03ffff15ff2fff8080ffff01ff04ffff0134ffff04ff2fff808080ffff01ff018080ff0180ff80808080ff8080808080ff018080ffff04ffff01a05a3875e000ab384ac01cdf8c272509f02845ba0a87fe1b8d267ba7cd7e2c807bffff04ffff01a0da3c6fd192afdb0e3318b0b44ddb102566fea251e74e8135be2317f4e50208a4ffff04ffff0164ffff04ffff01a03e8641ffd4808f666d7efa2539d0071d2e646115d153a8bde352a4e34586d348ffff04ffff01b08049a7369adf936b3ad73c88fc6abd3d172d1ea1661f7d6597842152c2652966ac6a9b93653124cd93bd9a769a039275ffff04ffff01a0d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80adffff04ffff01830493e0ffff04ffff018545d964b800ff01808080808080808080",
      "solution": "0xffa00000000000000000000000000000000000000000000000000000000000000000ff80ff8203e880"
    }
  ],
  "aggregated_signature": "0xa00d9e33e703605ec01e631afad2cfc1a841ee8eb5597f5c66dda2e8abede11ac706214cd87c4590f719e67426bd2b350ec2cb0cc98547504928838fa35c15ad04a99fc140f10d4caf0e2496ec70ff264b132265eb27098b260a24ca9013c437"
}

❯ chia wallet coins list -f $partial_fp -i 1
There are a total of 3 coins in wallet 1.
3 confirmed coins.
0 unconfirmed additions.
0 unconfirmed removals.
Confirmed coins:
...
Coin ID: 0xcdfc3d6b5cd78d474ab674babc40df99307477e761913023055d4ee69f817e06
	Address: txch186ryrl75sz8kvmt7lgjnn5q8r5hxgcg469f6300r22jwx3vx6dyq5fs6pm Amount: 0.299999999000  (299999999000 mojo), Confirmed in block: 1276617

...
```



