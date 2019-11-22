from Agent import Human

def change( human: Human ):
  human.pos_x = 2

human = Human(10)

print(human.pos_x)

change(human)

print(human.pos_x)