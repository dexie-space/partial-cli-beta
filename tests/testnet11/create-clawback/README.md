# Create
```bash
❯ partial create -f $partial_fp --offer 1:1.5 --request d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad:450
{
  "partial_info": {
    "fee_puzzle_hash": "bf00456f9fecf7fb57651b0c99ce13bd9d2858e9b190ec373ba158c9a9934e5a",
    "fee_rate": 100,
    "maker_puzzle_hash": "dbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bca",
    "public_key": "8049a7369adf936b3ad73c88fc6abd3d172d1ea1661f7d6597842152c2652966ac6a9b93653124cd93bd9a769a039275",
    "tail_hash": "d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad",
    "rate": 300000,
    "offer_mojos": 1500000000000--offer 1:0.5 --request d82dd03f8a9ad2f84353cd953c4de6b... [History]
  },
  "partial_coin": {
    "parent_coin_info": "0x3603e6c808ae1d4df4a41aa2c73c6f8f4233b4cd714a5e4845fad314e2253460",
    "puzzle_hash": "0xc861cd3857cb1990f515bc5e1a80e50f2d0473beac9cd8529a70cc6a95f2f378",
    "amount": 1500000000000
  },
  "launcher_coin": {
    "parent_coin_info": "0x070cb7455989e25809f7c1cf69389683627759f7c4286b82068fb0c3f37fa40c",
    "puzzle_hash": "0xdbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bca",
    "amount": 285383390000
  },
  "offer": "offer1qqr83wcuu2rykcmqvpsxre7eacddn7fgstelhs0nnytd8x5neg3m7873ephx967lwru88lgjnmdl04n49zkrvcjunxung4vga84etf0nr3n36dykdxattzmfua6j062ngqeeezn58cdupkafcd7cuxmv7zrv2u48nw83htdcy0st9m3pw08c0x5kyd9w0dk44juzsumuattqtegpymleken4kuw442levh3aant6pljmaq44sgxsgah6zl7thxashl30dmj9c7w0u0e5t2mhx57qz0ummdeh9jxth747ld05xc6jrag2ru0lq5n39n66sj0ed88s246yl8z5cdfhuhvkuf7khekupzd92upxd0420nc4lld3scldhm8kpq9g3e532zt0h2src6trgl3dhrns3d98m6m77vl67hq65avvde0y8hlep74l2hu2r0duquutp2qsaxhrw5mkxzxyvw43j9h0kl6p745ld5h0nllajtfvdwa29y2andj9fea68x80mcpzmvcvnkkqs50a8sf7ltc5y4l5n74vnnlxdl24k55vtcv95teu4pcr8w0d40k0yhemc38vchzygnxtew9jj3rkydrx4qwnxekvea88ptyn7h7my3r269cehlr7yl3j6ecthh3rchrlt5t8nfr2jfqz3dejxpq8y26je3qw5njxfavxtzk5lqgct4hefr9dccqdqfvrtp3utvq2jeqe7c3n2x5qzgmg3esgk39sg66g5zx0ggkhgxs849smms2pws522k2rvz9zygznnjccmeqv9gc8r653p0up90el7g8fq6zp75f8mhlxxrplc53hkyw6ufprzp73qzqfszgaj2pzwefm6ngg53m2cv6gjgc6tzyxfagl449j9qz620peyteyfhlxwerfgqg59ynpsn6sjsdzmsc8rfyggp4yegmgvnpxwfptggfdjm0vwzm5r42pd4qtv9zh8c2vrys0gkg8erfar73pgvf63zjqg9sklc8e6gsptvz37nyns6ds2yvzpkdmqskxeldyp3vcqqpms4ugym26gtksqrhy2s5xcysqtxqycftvvp0xlvlz00rtd56dud3hxf4y9m53trr02q0xw0tsd3hdpnkd5hfr4d2s24tk0mlmmde38697aktj0a2as7w60dacn90fa39u79nktjw08l87rlzuhnu3c2gmkqf92qya4qy5h7gqxyyknesjj8p3wgzvkg5gzsqukcusp3r2gu6ejydtn3ks8pqqgrftjgnupttgyshxx0g2jasn7v3hr6v68r7vz9huq9224s59nvsp4xxxkszfyhcfyp8wvetx34sx2u7jsevdzx32cqg0scsf2cyssfz375vuxzdyqs4cqxunqsr25c3m97vztmtfd69n9ez4wck7trr64j24w97rm8dhx9xw7ea2h09445eh3hrjus54a4nhpnvllln0hmls235eax08snmua4vg0zuhrssmw04c2yf82a80dzuz9p9cr23x23f5x6awqm872e4nae8uad46dmflzfmt47km3tkucg60nkk5aykc5sv82g6a84nyek0fc64gwfm09hjevkeesfu4gfxmlgtmcxlxh449rl8vzea8mturakeyhd4hmm0rthmtuam8a5ehevatvyk5gkfne0jqwyqkkj5sstg0c8lw7n2f4hyyerf0fqkz4j2ve3543drtw8qmeqkqvu9atx7npuule6y2uu9h4ld9v0dqdec8jwm5e29gtw6cs670s2vatyuyj3hll74s4t6uzpwksd2c039yhhh0azrt9344vlru4pcawy03ad9x926n6lxras85e7c2quzr40k0cat0r6v508z6rh7avlf7qp0l58z99erech"
}
```

# Show
```bash
❯ partial show  ./launcher.offer
╭──────────────────────────┬────────────────────────────────────────────────────────────────────╮
│ MOD_HASH:                │ 0x8d05845bcd4472d45cec3b5d261e7a08f5cb6eb1562ef9654744ad35ec81c6d1 │
│ Valid:                   │ Yes                                                                │
│ Partial Offer Coin Name: │ 0x6bd6a2762917247ee223bf4fd7d2ded531049129165feac93250f252fb8265b8 │
├──────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Total Offer Amount:      │ 1.5 XCH                                                            │
│ Total Request Amount:    │ 450.0 CATs                                                         │
│ Request Tail Hash:       │ 0xd82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad │
│ Rate (1 XCH):            │ 300.0 CATs                                                         │
│ Fee Rate:                │ 1.0%                                                               │
╰──────────────────────────┴────────────────────────────────────────────────────────────────────╯

❯ partial show  ./launcher.offer --json | jq
{
  "is_valid": true,
  "MOD_HASH": "8d05845bcd4472d45cec3b5d261e7a08f5cb6eb1562ef9654744ad35ec81c6d1",
  "partial_info": {
    "fee_puzzle_hash": "bf00456f9fecf7fb57651b0c99ce13bd9d2858e9b190ec373ba158c9a9934e5a",
    "fee_rate": 100,
    "maker_puzzle_hash": "dbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bca",
    "public_key": "8049a7369adf936b3ad73c88fc6abd3d172d1ea1661f7d6597842152c2652966ac6a9b93653124cd93bd9a769a039275",
    "tail_hash": "d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad",
    "rate": 300000,
    "offer_mojos": 1500000000000
  },
  "partial_coin": {
    "parent_coin_info": "0x3603e6c808ae1d4df4a41aa2c73c6f8f4233b4cd714a5e4845fad314e2253460",
    "puzzle_hash": "0xc861cd3857cb1990f515bc5e1a80e50f2d0473beac9cd8529a70cc6a95f2f378",
    "amount": 1500000000000
  },
  "launcher_coin": {
    "parent_coin_info": "0x070cb7455989e25809f7c1cf69389683627759f7c4286b82068fb0c3f37fa40c",
    "puzzle_hash": "0xdbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bca",
    "amount": 285383390000
  }
}
```

# Clawback
```bash
❯ partial clawback -f $partial_fp -m 1000 ./launcher.offer
{
  "coin_spends": [
    {
      "coin": {
        "parent_coin_info": "0x070cb7455989e25809f7c1cf69389683627759f7c4286b82068fb0c3f37fa40c",
        "puzzle_hash": "0xdbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bca",
        "amount": 285383390000
      },
      "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b0a31ecb83c732a8dc1044aee1038cf07c84c422ceb67ca8d11cc795b5a0775034ff829a8b86c2ad29f4b1bdb32ee11ef5ff018080",
      "solution": "0xff80ffff01ffff3cffa0fedd60bf78dbbba2c642ffe132aeb9b250e41fbddbb0a15ed5ef8bfe8081628e80ffff33ffa0c861cd3857cb1990f515bc5e1a80e50f2d0473beac9cd8529a70cc6a95f2f378ff86015d3ef7980080ffff33ffa05c85145782d02392b18861ed885738792f3b8f37fcea448194395e6c6ee7f065ff8513e13f1f488080ff8080"
    },
    {
      "coin": {
        "parent_coin_info": "0x070cb7455989e25809f7c1cf69389683627759f7c4286b82068fb0c3f37fa40c",
        "puzzle_hash": "0xdbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bca",
        "amount": 300000000000
      },
      "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b0a31ecb83c732a8dc1044aee1038cf07c84c422ceb67ca8d11cc795b5a0775034ff829a8b86c2ad29f4b1bdb32ee11ef5ff018080",
      "solution": "0xff80ffff01ffff3dffa07bcb0775f7f3fe3ea17682d4286b7d62327e45b35e07c1a23d56197d51a1f1678080ff8080"
    },
    {
      "coin": {
        "parent_coin_info": "0xf8e82d15fe2534f983f67bb46432e8313ba1c120d96386f51da7fab816c899a2",
        "puzzle_hash": "0xdbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bca",
        "amount": 999999999000
      },
      "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b0a31ecb83c732a8dc1044aee1038cf07c84c422ceb67ca8d11cc795b5a0775034ff829a8b86c2ad29f4b1bdb32ee11ef5ff018080",
      "solution": "0xff80ffff01ffff3dffa07bcb0775f7f3fe3ea17682d4286b7d62327e45b35e07c1a23d56197d51a1f1678080ff8080"
    },
    {
      "coin": {
        "parent_coin_info": "0x3603e6c808ae1d4df4a41aa2c73c6f8f4233b4cd714a5e4845fad314e2253460",
        "puzzle_hash": "0xc861cd3857cb1990f515bc5e1a80e50f2d0473beac9cd8529a70cc6a95f2f378",
        "amount": 1500000000000
      },
      "puzzle_reveal": "0xff02ffff01ff02ffff01ff04ffff04ffff0149ffff04ff8202ffff808080ffff02ffff03ffff15ff820bffff8080ffff01ff04ffff04ffff0146ffff04ff8205ffff808080ffff04ffff02ff1affff04ff02ffff04ff2fffff04ff8200bfffff04ff8205ffffff04ffff02ff3cffff04ff02ffff04ff82017fffff04ff820bffff8080808080ff80808080808080ffff04ffff02ff16ffff04ff02ffff04ffff11ff820bffffff02ff12ffff04ff02ffff04ff17ffff04ff820bffff808080808080ff80808080ffff04ffff04ffff0133ffff04ff0bffff04ffff02ff12ffff04ff02ffff04ff17ffff04ff820bffff8080808080ff80808080ffff02ffff03ffff15ffff11ff8202ffff820bff80ff8080ffff01ff04ffff02ff2effff04ff02ffff04ff05ffff04ff0bffff04ff17ffff04ff2fffff04ff5fffff04ff8200bfffff04ff82017fffff04ffff11ff8202ffff820bff80ff8080808080808080808080ff8080ffff01ff018080ff018080808080ffff01ff02ff3effff04ff02ffff04ff2fffff04ff5fffff04ff8202ffffff04ff8217ffff8080808080808080ff018080ffff04ffff01ffffffff02ffff03ff05ffff01ff02ff10ffff04ff02ffff04ff0dffff04ffff0bffff0102ffff0bffff0101ffff010480ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0980ffff0bffff0102ff0bffff0bffff0101ff8080808080ff8080808080ffff010b80ff0180ff0bffff0102ffff0bffff0101ffff010280ffff0bffff0102ffff0bffff0102ffff0bffff0101ffff010180ff0580ffff0bffff0102ffff02ff10ffff04ff02ffff04ff07ffff04ffff0bffff0101ffff010180ff8080808080ffff0bffff0101ff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff14ffff04ff02ffff04ff09ff80808080ffff02ff14ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ffff02ffff03ff0bffff01ff02ff2cffff04ff02ffff04ffff02ffff03ff13ffff01ff04ff13ff0580ffff010580ff0180ffff04ff1bff8080808080ffff010580ff0180ff05ffff14ffff12ff05ff0b80ffff018600e8d4a510008080ffffff05ffff14ffff12ff05ff0b80ffff018227108080ff04ffff013fffff04ffff0bffff02ff18ffff04ff02ffff04ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7affff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ffff0bffff0101ff0b80ffff04ffff0bffff0101ffff01a037bef360ee858133b69d595a906dc45d01af50379dad515eb9518abb7c1d2a7a80ff80808080808080ffff02ff14ffff04ff02ffff04ffff04ff17ffff04ffff04ff05ffff04ff2fffff04ffff04ff05ff8080ff80808080ff808080ff8080808080ff808080ffff04ffff0133ffff04ffff01a0cfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7ffff04ff05ff80808080ffff04ffff0133ffff04ffff02ff18ffff04ff02ffff04ff05ffff04ffff0bffff0101ff8202ff80ffff04ffff0bffff0101ff82017f80ffff04ffff0bffff0101ff8200bf80ffff04ffff0bffff0101ff5f80ffff04ffff0bffff0101ff2f80ffff04ffff0bffff0101ff1780ffff04ffff0bffff0101ff0b80ffff04ffff0bffff0101ff0580ff808080808080808080808080ffff04ff8202ffff80808080ff02ff2cffff04ff02ffff04ff80ffff04ffff04ffff04ffff0133ffff04ff05ffff04ffff11ff17ff2f80ff80808080ffff04ffff04ffff0132ffff04ff0bffff04ffff0bff1780ff80808080ffff04ffff02ffff03ffff15ff2fff8080ffff01ff04ffff0134ffff04ff2fff808080ffff01ff018080ff0180ff80808080ff8080808080ff018080ffff04ffff01a08d05845bcd4472d45cec3b5d261e7a08f5cb6eb1562ef9654744ad35ec81c6d1ffff04ffff01a0bf00456f9fecf7fb57651b0c99ce13bd9d2858e9b190ec373ba158c9a9934e5affff04ffff0164ffff04ffff01a0dbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bcaffff04ffff01b08049a7369adf936b3ad73c88fc6abd3d172d1ea1661f7d6597842152c2652966ac6a9b93653124cd93bd9a769a039275ffff04ffff01a0d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80adffff04ffff01830493e0ffff04ffff0186015d3ef79800ff01808080808080808080",
      "solution": "0xffa00000000000000000000000000000000000000000000000000000000000000000ff80ff8203e880"
    }
  ],
  "aggregated_signature": "0x947349e4d85c03f85b16f31d1b57d3cb126031c51ee7d0d5decb3aed6741e2a3c096599975236a739f212dfcb40820fa0193db1eabbb12f16b5a045cda934cd85d65a95310caf1af3475716c35232d9f3abd636df265aebcdb5f978400771c89"
}
```

# Show spent offer
```bash
❯ partial show  ./launcher.offer --json | jq
{
  "is_valid": false,
  "MOD_HASH": "8d05845bcd4472d45cec3b5d261e7a08f5cb6eb1562ef9654744ad35ec81c6d1",
  "partial_info": {
    "fee_puzzle_hash": "bf00456f9fecf7fb57651b0c99ce13bd9d2858e9b190ec373ba158c9a9934e5a",
    "fee_rate": 100,
    "maker_puzzle_hash": "dbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bca",
    "public_key": "8049a7369adf936b3ad73c88fc6abd3d172d1ea1661f7d6597842152c2652966ac6a9b93653124cd93bd9a769a039275",
    "tail_hash": "d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad",
    "rate": 300000,
    "offer_mojos": 1500000000000
  },
  "partial_coin": {
    "parent_coin_info": "0x3603e6c808ae1d4df4a41aa2c73c6f8f4233b4cd714a5e4845fad314e2253460",
    "puzzle_hash": "0xc861cd3857cb1990f515bc5e1a80e50f2d0473beac9cd8529a70cc6a95f2f378",
    "amount": 1500000000000
  },
  "launcher_coin": {
    "parent_coin_info": "0x070cb7455989e25809f7c1cf69389683627759f7c4286b82068fb0c3f37fa40c",
    "puzzle_hash": "0xdbdeae8820ab3201a969a5651202f5d4a59e419ac1331c82daba02b9d7421bca",
    "amount": 285383390000
  }
}
```