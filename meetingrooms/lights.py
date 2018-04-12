def green(pair):
        pair[0].on()
        pair[1].off()

def red(pair):
        pair[0].off()
        pair[1].on()

def on(pair):
        pair[0].on()
        pair[1].on()

def off(pair):
        pair[0].off()
        pair[1].off()

def all_on():
        for room in rooms:
                on(rooms[room])


