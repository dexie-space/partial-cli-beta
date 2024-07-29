[Partial Offer Coin (PoC)](https://github.com/dexie-space/dexie-governance/issues/12)

## create genesis partial offer
```
❯ partial create -f $partial_fp --offer 1:1 --request 657bdae0165c622f635374e539ef7e4632750ecc87541071478c21a7ba67096c:128.680 -pk a07f3f0f388f33cb4e2b5494e7be564a7f8cbedeabc453be0c3ed75e36ddf407b8667bf9b84d7045e1c0c16462ad822d
offer1qqr83wcuu2ryhhvemd94gugscu6ukhw2eq529p6qt9av5zl8nn0h2rfvk5eq6zethfqtfltwsa6a2h9uzzh2seg5j99cy9payj6urwny2yvs3zdp49v9yyny95296ty4dqx38g5gd6ef69v3l6rwvmvxn88lq80xv9l0echzut3phdh0f76x0h04xny0fg3nkm7ggrgan8e8as0dt8ll4c03whfj0ku79cxmnh0hgg0h5h7ffufu26u7un88feevdvcyu9g0e7txaxu7qgtzxynwf789hwznllmnlm3ewpn6quwnptdqy3nk5mknmla3da0krgaldlkvd5y7h6jwc9u878dkldnwk0hxwau3wl4h3luqusmekvhxftncp44r8uc2tk7sulk8qv8dur95w4u6hc20fp9w54wr6es00d69w50uy4hmr9gg52qua4edkkacx66hyc6j0wxm9ul4edftkf3mqve0mrf7d7wnlspldn6xfl8c70362pvww2r85k4d9edd78uu49xtek4der4v2jragdxxxznfsukwkpp9cj5x593v5s9636zcfpjjn3p9mc6yqxpj9fqtvf9vcg2kgguszu9y5uatcddu43ztsjj4dkxvsdrzqffnxqd9ycqgysm9wqzf65q34cggdryc23cz290rqg3vp9fxszfqg2vq5562z33cckv8p5mfwk25fq6ga9ppxw5xmpsfyx5x3366ce39v593yvpztse2t6gcp9kpsfsxpqg2syrs92fj3zypgxg2dp9qq3vn4zqwpy2cdn5g5ktksn3vvtqy544d9jtxa5zvfskmls3544ve24mc924xyc0dr74e7ha80305a6ln83lmscln5rth6f6hekxgunj7lparmwhujuha9ykvwfep08gggs00eanhf4wpc7nh6ey8cmcl0yfu4f4apqkvawr9rle5awslcu0nmhjltyvxc0dsx9h5kdr9eyeahydw6kyltrnns7ddraal5rmc60q2hq70p
```

## get
```
❯ partial get -ph d00aa66868bba6e5bdda64eae25116cd42eeb8410b7e328551c7fd6b46ece933 -pk a07f3f0f388f33cb4e2b5494e7be564a7f8cbedeabc453be0c3ed75e36ddf407b8667bf9b84d7045e1c0c16462ad822d -t 657bdae0165c622f635374e539ef7e4632750ecc87541071478c21a7ba67096c -r 128.680 -a 1000000000000  -h
b0db8f7952a418110c8b0368a59ec6134fe84bc2b043a4ba9c6afc8bf834c0fd
```

## show
```
❯ partial show ./test.offer                                                    
{
  "maker_puzzle_hash": "d00aa66868bba6e5bdda64eae25116cd42eeb8410b7e328551c7fd6b46ece933",
  "public_key": "a07f3f0f388f33cb4e2b5494e7be564a7f8cbedeabc453be0c3ed75e36ddf407b8667bf9b84d7045e1c0c16462ad822d",
  "tail_hash": "657bdae0165c622f635374e539ef7e4632750ecc87541071478c21a7ba67096c",
  "rate": 128.68,
  "offer_mojos": 1000000000000
}
```

## take
> TBA