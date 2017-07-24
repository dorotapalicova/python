from random import randint


class Monster:
    def __init__(self, name, strength, health):
        self.name = name
        self.strength = strength
        self.health = health

    # print on standard output name, strength and health of monster
    def actual_monster(self):
        print(self.name, "se silou", self.strength, "a", self.health, "zivotmi.")

    # lower health of monster when attacked
    def deal_damage(self, attack_strength):
        self.health -= attack_strength


class Room:
    def __init__(self, name, next_rooms, monster):
        self.name = name
        self.next_rooms = next_rooms
        self.monster = monster

    def add_door(self, door_to):
        self.next_rooms.append(door_to)

    # print on standard output room and monster
    def actual_room(self):
        print("Nachadzas sa v mistnosti", self.name, ". Je tu:")
        self.monster.actual_monster()

    # print on standard number of neighbor rooms
    def actual_neighbors_rooms(self):
        print("Je tu", len(self.next_rooms), "dveri.")


class Hero:
    def __init__(self, name, strength, health, position):
        self.name = name
        self.strength = strength
        self.health = health
        self.position = position

    # print on standard output name, strength and health of hero
    def actual_hero(self):
        print("Volas sa", self.name, ". Tva sila je", self.strength, "a mas ", self.health, "zivotu.")

    # hero goes to one of neighbor rooms
    def go_to_next_room(self):
        where = int(input("Zvolte cislo dveri do ktorych chcete ist ")) - 1
        while where < 0 or where > len(self.position.next_rooms) - 1:
            where = int(input("Zvolte cislo dveri do ktorych chcete ist ")) - 1
        self.position = self.position.next_rooms[where]
        return self.position

    # hero and monster throw dice, throw is add to their strength, one with lower score gets damage based on difference of scores
    def hit_monster(self,
                    monster):
        throw_hero = randint(1, 6)
        throw_monster = randint(1, 6)
        throw_hero += self.strength
        throw_monster += monster.strength
        attack_strength = abs(throw_monster - throw_hero)

        if throw_monster < throw_hero:
            print("Trafil si priseru a ubral jej", attack_strength, "zivotov")
            monster.deal_damage(attack_strength)
            if monster.health <= 0:
                print("Prisera porazena.")
            else:
                print("Prisera ma", monster.health, "zivotov")

        elif throw_monster > throw_hero:
            print("Trafila ta prisera a ubrala ti", attack_strength, "zivotov")
            self.take_damage(attack_strength)
            if self.health > 0:
                print("Mas", self.health, "zivotov")
            else:
                print(self.name, "bohuzial si prehal.")

        elif throw_monster == throw_hero:
            return (self.hit_monster(monster))

    # hero fight with monster while both of them are alive
    def fight_monster(self, monster):
        while self.health > 0 and monster.health > 0:
            self.hit_monster(monster)

    # hero takes damage based on attack_strength
    def take_damage(self, attack_strength):
        self.health -= attack_strength

    # hero goes through rooms and fight monsters while he is alive or while he is not in exit
    def find_exit(self):
        if self.health >= 0 and self.position.name != "Vychod":
            self.actual_hero()
            self.position.actual_room()

            if (self.position.monster.name != "Nic"):
                todo = input("Chces bojovat s priserou? Ak ano zmackni b ")
                if (todo == 'b'):
                    self.fight_monster(self.position.monster)
                    if self.health <= 0:
                        print (self.name, "bohuzial si prehal.")
                        return

            self.position.actual_neighbors_rooms()
            self.go_to_next_room()
            print("")
            print(5 * "-----")
            return (self.find_exit())

        elif self.position.name == "Vychod":
            print (self.name, "dostal si sa k vychodu. Vyhral si.")
            return


def game():
    mummy = Monster("Desiva mumie", 3, 15)
    cockroach = Monster("Hnusny svab", 1, 7)
    spider = Monster("Jedenactinohy pavouk", 2, 20)
    medusa = Monster("Meduza s hady misto vlasu", 5, 22)
    zombie = Monster("Zapachajici zombie", 4, 11)
    teacher = Monster("Nespravedlivy cvicici", 5, 16)
    exam = Monster("Prilis tezky zapocet", 3, 30)
    nothing = Monster("Nic", 0, 0)
    rat = Monster("Chlupata krysa", 1, 24)
    harpy = Monster("Zakerna harpye", 2, 13)
    centaur = Monster("Sileny kentaur", 3, 18)
    lizard = Monster("Jesterka bez ocasku", 1, 8)

    kitchen = Room("Moderni kuchyne", [], mummy)
    living_room = Room("Zabydleny obyvaci pokoj", [], cockroach)
    bathroom = Room("Kachlickova koupelna", [], centaur)
    hall = Room("Prostorna hala", [], harpy)
    toilet = Room("Smradlavy zachod", [], exam)
    loft = Room("Prastara puda", [], rat)
    cellar = Room("Zavsiveny sklep", [], teacher)
    corridor = Room("Studena chodba", [], spider)
    bedroom = Room("Utulna loznice", [], zombie)
    exit = Room("Vychod", [], nothing)
    closet = Room("Kumbalek pro sluzku", [], medusa)
    staircase = Room("Vrzajici schodiste", [], lizard)

    rooms = [kitchen, living_room, bathroom, hall, toilet, loft, cellar, corridor, bedroom, exit, closet, staircase]

    for room in rooms:
        for i in range(4):
            chance = rooms[randint(0, len(rooms) - 1)]
            if room != chance:
                if not chance in room.next_rooms:
                    chance.add_door(room)
                    room.add_door(chance)

    name = input("Ako sa volas? ")
    player = Hero(name, 4, 50, rooms[randint(0, len(rooms) - 1)])
    player.find_exit()


game()
