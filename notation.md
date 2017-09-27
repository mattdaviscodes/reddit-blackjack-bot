# Blackjack Notation
Storing blackjack hands in any state while keeping a record of all previous
states demands a specialized notation. The goal of this document is to create a
standardized way to record how any game of blackjack with an arbitrary number
of players proceeded.

## Legend

### Card Values
| Key 	| Description         	|
|-----	|---------------------	|
| s   	| Spades              	|
| c   	| Clubs               	|
| h   	| Hearts              	|
| d   	| Diamonds            	|
| t   	| Ten                 	|
| j   	| Jack                	|
| q   	| Queen               	|
| k   	| King                	|
| a   	| Ace                 	|
| 2-9 	| Integer card values 	|

Examples:
- `3h` - Three of Hearts
- `td` - Ten of Diamonds
- `jc` - Jack of Clubs
- `as` - Ace of Spades

### Actions and Results
| Key 	| Description  	|
|-----	|--------------	|
| ^   	| Hit          	|
| _   	| Stay (Stand) 	|
| !   	| Double Down  	|
| /   	| Split        	|
| #   	| Bust         	|
| ?     | Hidden card   |
| %     | Reveal card   |
| w   	| Win          	|
| l   	| Loss         	|
| p   	| Push         	|

> Note: The Hidden Card icon may soon be deprecated

### Meta
| Key 	| Description           	|
|-----	|-----------------------	|
| &#124;| Entry Delimiter       	|
| .   	| Intra-Entry Delimiter 	|
| {}  	| Setup Block           	|
| []  	| Outcome Block         	|
| //  	| Split Details Block   	|

## Format

### Hand Level
A hand of blackjack is represented in this notation by three distinct blocks of
characters. Each game begins with a **setup block**, enclosed in curly braces `{}`, which lists the details of the game. Number of players, number of decks, any other variable rules like dealer action on soft 17.

The main block of the game is recorded via a series of **event blocks**, which are delimited by the pipe character `|`. These list each player and dealer action, as well as the direct result of those actions.

The results of the hand are listed at the very end in an **outcome block**, enclosed in square brackets `[]`. This is a comma separated list of each players outcome -- win, loss, or push. It may be further subdivided if any of the players split their hand(s).

### Event Level
Each event in the **event block** is divided into five discrete data points, separated by periods `.`. These are:
- Actor ID
    - 0 for dealer
    - Any positive integer for a player
- Hand ID
    - Any positive integer
    - Usually a 1, but can be greater if player splits hand(s)
- Action
    - Hit, Double Down, etc
    - Things that happen before another card is dealt
- Card
- Modifier
    - Stay, Bust
    - Thing that happen after card is dealt

Action, Card, and Modifier may be omitted depending on situation. For example,
when a hand is first being dealt, the players are taking no actions, but they
receive cards. Or a player may choose to stay with their first two cards, so
we would record an empty Action and Card block for that event, with Stay in
the Modifier section.

### Examples
Example below with comments for clarity. Usually these will be stored with as little whitespace as possible.

```
// BEGIN SETUP
{3.52}     // Setup: 3 players, 52 cards

// BEGIN DEAL
1.1..as.
2.1..6s.
3.1..ac.
0.1...?
1.1..ad.
2.1..5d.
3.1..kd._   // Player 3 dealt blackjack, stays
0.1..ah.    // Dealer shows ace up. Insurance offering is not recorded here as it is outside the main flow of the game (it's a side bet)

// BEGIN PLAY
// If dealer has blackjack, the next lines would be:
//      d.%.kc.$
//      [l,l,p]

1.1./..     // Player 1 splits aces
/1.as/2.ad/
1.1.^.5c.   // Player hits first hand, receives 5c, soft 16 total
1.1.^.3c._  // Player hits hand 1 again, stays
1.2.^.2d.
1.2.^.4c.
1.2.^.5h.
1.2.^.8d._  // Player takes a ton of cards, stays with 20
2.1.!.qs._  // Player 2 doubles down, gets 21, stays  
0.1.%.4h.   // Dealer reveals hole card
0.1.^.6d._  // Dealer hits, gets 21, stays

// OUTCOME
[l/l,p,w]
```

The same game recorded to standard -- no whitespace, no comments -- looks like this:

```
{3.52}|1.1..as.|2.1..6s.|3.1..ac.|0.1...?|1.1..ad.|2.1..5d.|3.1..kd._|0.1..ah.|1.1./..|/1.as/2.ad/|1.1.^.5c.|1.1.^.3c._|1.2.^.2d.|1.2.^.4c.|1.2.^.5h.|1.2.^.8d._|2.1.!.qs._|0.1.%.4h.|0.1.^.6d._|[l/l,p,w]
```
