[Partial Offer Coin (PoC)]

# Overview

A dexie partial offer coin is a coin with a puzzle offering one asset (XCH only for now) for another CAT at a fixed exchange rate. A maker can use partial cli to create an offer. The offer can be taken using partial cli and an optional standard Chia offer. The offer can also be clawed back by the maker at any time.

# Concepts
- A file containing partial offer information is a non standard bech32 offer file with partial coin spend.
- The partial offer coin is a coin on the blockchain.
- When the partial offer is taken partially, the new partial offer coin with the new amount is created.
- The standard settlement (offer) puzzle is utilized to exchange the assets.
- The first partial offer is created by using `partial create` command. When the first offer is created, no new coin is created. The first partial offer coin is created and spent when the offer is taken.
- The partial offer can be taken by using `partial take` command.
- The total amount on the partial offer can be clawed back to the maker by using `partial clawback` command.


# Partial CLI commands
```bash
❯ partial --help

 Usage: partial [OPTIONS] COMMAND [ARGS]...

 Manage dexie partial offers

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────╮
│ clawback   clawback the partial offer coin.                                                       │
│ config     display the cli config                                                                 │
│ create     create a partial offer requesting CAT token                                            │
│ get        get a serialized curried puzzle of the partial offer coin                              │
│ show       display the dexie partial offer information.                                           │
│ take       Take the dexie partial offer by providing the taker offer file or request information. │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯

```
