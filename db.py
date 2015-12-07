"""A mock database of game solutions and their properties."""

# solution properties
BALL = 0
SWING = 1
SHOOT = 2
TABLE = 3
RUN = 4
FIGHT = 5
THROW = 6
TEAM = 7
SKATE = 8
RIDE = 9
JUMP = 10
SWIM = 11
CATCH = 13
RACKET = 14
KICK = 15

# same order as above
# TODO Enum might work better?
all_properties = ['ball', 'swing', 'shoot', 'table', 'run', 'fight', 'throw', 'team', 'skate', 'ride', 'jump', 'swim',
                  'catch', 'racket', 'kick']

solutions = {
    'tennis':        [BALL, SWING, RACKET, RUN],
    'badminton':     [SWING, RACKET, RUN],
    'basketball':    [BALL, RUN, JUMP, CATCH],
    'baseball':      [BALL, SWING, RUN, CATCH],
    'soccer' :       [BALL, KICK, RUN],
    'hockey':        [SKATE, SHOOT],
    'speed skating': [SKATE],
    'golf':          [BALL, SWING],
    'archery':       [SHOOT],
    'boxing':        [SWING, FIGHT],
    'wrestling':     [FIGHT],
    'cycling':       [RIDE],
    'diving':        [JUMP, SWIM],
    'swimming':      [SWIM],
    'polo':          [BALL, RIDE, SWING],
    'cricket':       [BALL, SWING, RUN, CATCH],
    'shooting':      [SHOOT],
    'triathlon':     [RUN, RIDE, SWIM],
}

all_solutions = solutions.keys()
