import pygame, character, time, background, spells

class Enemy(character.Character):
    """
    paths = [walkleft, attackleft, die]
    speed = (x, y) >0
    direction = (+-1, +-1) o (0,0)
    """

    def __init__(self, pos, lista_im, speed, direction):

        character.Character.__init__(self, lista_im)
        self.speed = speed
        self.direction = direction
        self.pos = pos
        self.rect.move_ip(pos)
        self.before = 'left'
        self.index = 0
        self.time_before = time.time()
        

class Ward(Enemy):
    """
    """

    def __init__(self, pos, lista_im, speed, direction): #stats
        Enemy.__init__(self, pos, lista_im, speed, direction)
        self.health = 25
        self.healthMax = 25
        self.attack = 2
        self.barpos = (self.pos[0], self.pos[1]-3)

        self.healthbar = pygame.Surface((30, 3))
        self.healthbar.fill((0,0,0))
        self.healthbar.set_alpha(75)
        self.healthRect = self.healthbar.get_rect()
        self.healthRect.move_ip(self.barpos)

        self.hpbar = pygame.Surface((30, 3))
        self.hpbar.fill((255,0,0))
        self.hpbar.set_alpha(240)
        self.hpRect = self.hpbar.get_rect()
        self.hpRect.move_ip(self.barpos)


        animtime = 0.25
        s1 = pygame.image.load('images/heal1.gif')
        s2 = pygame.image.load('images/heal2.gif')
        s3 = pygame.image.load('images/heal3.gif')
        s4 = pygame.image.load('images/heal4.gif')
        l_sprites = [s1, s2, s3, s4]
        self.healing = spells.Heal(l_sprites, animtime)




    def update(self, tower):
        self.healing.heal(self, 10)
        antic = self.rect.copy()
        self.rect.move_ip(self.speed[0]*self.direction[0], self.speed[1] * self.direction[1])
        self.healthRect.move_ip(self.speed[0]*self.direction[0], self.speed[1] * self.direction[1])
        self.hpRect.move_ip(self.speed[0]*self.direction[0], self.speed[1] * self.direction[1])

        l = pygame.sprite.spritecollide(self, tower, dokill = False)
        atacar = False
        for var in l:
            if type(var) == background.Tower:
                self.collision(antic, var.rect)
                torre = var
                atacar = True
        #actualizar choques --> atacar
        #vida (muerte)
        
        if self.speed[0] > 0 and self.direction[0] < 0:
            if self.before != 'left':
                self.image = self.walkleft[0]
                self.before = 'left'
            else:
                if time.time() - self.time_before >= 0.18:
                    self.time_before = time.time()
                    if self.index+1 == len(self.walkleft):
                        self.image = self.walkleft[0]
                        self.index = 0
                    else:
                        self.image = self.walkleft[self.index+1]
                        self.index += 1
        elif self.speed[0] > 0 and self.direction[0] > 0:
            if self.before != 'right':
                self.image = self.walkright[0]
                self.before = 'right'
            else:
                if time.time() - self.time_before >= 0.18:
                    self.time_before = time.time()
                    if self.index+1 == len(self.walkright):
                        self.image = self.walkright[0]
                        self.index = 0
                    else:
                        self.image = self.walkright[self.index+1]
                        self.index += 1
        elif self.before == 'collision':
            self.index = 0
            self.image = self.attackleft[self.index]
            self.before = 'attackleft'
        elif self.before == 'attackleft' and atacar:
            if time.time() - self.time_before >= 0.3:
                self.time_before = time.time()
                self.index += 1
                if self.index == len(self.attackleft):
                    self.index = 0
                    self.image = self.attackleft[self.index]
                else:
                    self.image = self.attackleft[self.index]
                    if self.index == 1:
                        torre.takeDamage(self.attack)
                        if torre.health <= 0:
                            self.direction = (-1, 0)
        elif self.before == 'dying0':
            self.index = 0
            self.image = self.die[self.index]
            self.before = 'dying1'
            self.time_before = time.time()
        elif self.before == 'dying1':
            if time.time() - self.time_before >= 0.4 and self.index < 1:
                self.index = 1
                self.image = self.die[self.index]
                self.time_before = time.time()
            elif time.time() - self.time_before >= 4 and self.index == 1:
                self.kill()
        else:
            self.direction = (-1,0)

    def collision(self, enemic, fondo):
        """
        IMPORTANTE: Se procesa el choque ANTES del movimiento, por tanto, aun no se tocan, pero se supone que lo haran con el proximo update.
        """
        if enemic.left >= fondo.right:
            self.direction = (0, 0)
            self.before = 'collision'
    def takeDamage(self, n):
        health_antes = self.health
        self.health-=n
        if health_antes<=0:
            pass
        elif self.health <= 0 and 'dying' not in self.before:
            self.death()
        else:
            pos = (self.rect.left, self.rect.top - 3)
            self.hpbar = pygame.Surface((int(30*self.health/self.healthMax), 3))
            self.hpbar.fill((255,0,0))
            self.hpbar.set_alpha(240)
            self.hpRect = self.hpbar.get_rect()
            self.hpRect.move_ip(pos)

            
    def death(self):
        self.before = 'dying0'
        self.direction = (0,0)
        

class Orc(Enemy):
    """
    """

    def __init__(self, pos, lista_im, speed, direction): #stats
        Enemy.__init__(self, pos, lista_im, speed, direction)
        self.health = 40
        self.healthMax = 40
        self.attack = 4
        self.barpos = (self.rect.centerx - 20, self.pos[1]-4)

        self.healthbar = pygame.Surface((30, 3))
        self.healthbar.fill((0,0,0))
        self.healthbar.set_alpha(75)
        self.healthRect = self.healthbar.get_rect()
        self.healthRect.move_ip(self.barpos)

        self.hpbar = pygame.Surface((30, 3))
        self.hpbar.fill((255,0,0))
        self.hpbar.set_alpha(240)
        self.hpRect = self.hpbar.get_rect()
        self.hpRect.move_ip(self.barpos)




    def update(self, tower):
        antic = self.rect.copy()
        self.rect.move_ip(self.speed[0]*self.direction[0], self.speed[1] * self.direction[1])
        self.healthRect.move_ip(self.speed[0]*self.direction[0], self.speed[1] * self.direction[1])
        self.hpRect.move_ip(self.speed[0]*self.direction[0], self.speed[1] * self.direction[1])

        l = pygame.sprite.spritecollide(self, tower, dokill = False)
        atacar = False
        for var in l:
            if type(var) == background.Tower:
                self.collision(antic, var.rect)
                torre = var
                atacar = True
        #actualizar choques --> atacar
        #vida (muerte)
        
        if self.speed[0] > 0 and self.direction[0] < 0:
            if self.before != 'left':
                self.image = self.walkleft[0]
                self.before = 'left'
            else:
                if time.time() - self.time_before >= 0.12:
                    self.time_before = time.time()
                    if self.index+1 == len(self.walkleft):
                        self.image = self.walkleft[0]
                        self.index = 0
                    else:
                        self.image = self.walkleft[self.index+1]
                        self.index += 1
        elif self.speed[0] > 0 and self.direction[0] > 0:
            if self.before != 'right':
                self.image = self.walkright[0]
                self.before = 'right'
            else:
                if time.time() - self.time_before >= 0.12:
                    self.time_before = time.time()
                    if self.index+1 == len(self.walkright):
                        self.image = self.walkright[0]
                        self.index = 0
                    else:
                        self.image = self.walkright[self.index+1]
                        self.index += 1
        elif self.before == 'collision':
            self.index = 0
            self.image = self.attackleft[self.index]
            self.before = 'attackleft'
        elif self.before == 'attackleft' and atacar:
            if time.time() - self.time_before >= 0.3:
                self.time_before = time.time()
                self.index += 1
                if self.index == len(self.attackleft):
                    self.index = 0
                    self.image = self.attackleft[self.index]
                else:
                    self.image = self.attackleft[self.index]
                    if self.index == 1:
                            torre.takeDamage(self.attack)
                            if torre.health <= 0:
                                self.direction = (-1, 0)

        elif self.before == 'dying0':
            self.index = 0
            self.image = self.die[self.index]
            self.before = 'dying1'
            self.time_before = time.time()
        elif self.before == 'dying1':
            if time.time() - self.time_before >= 0.2 and self.index < 2:
                self.index += 1
                self.image = self.die[self.index]
                self.time_before = time.time()
            elif time.time() - self.time_before >= 4 and self.index == 3:
                self.kill()
        else:
            self.direction = (-1,0)

    def collision(self, enemic, fondo):
        """
        IMPORTANTE: Se procesa el choque ANTES del movimiento, por tanto, aun no se tocan, pero se supone que lo haran con el proximo update.
        """
        if enemic.left >= fondo.right:
            self.direction = (0, 0)
            self.before = 'collision'
    def takeDamage(self, n):
        health_antes = self.health
        self.health-=n
        print(health_antes, self.health)
        if health_antes<=0:
            pass
        elif self.health <= 0 and 'dying' not in self.before:
            self.death()
        else:
            print(self.health)
            pos = (self.rect.centerx - 20, self.rect.top - 4)
            #pos = self.barpos
            self.hpbar = pygame.Surface((int(30*self.health/self.healthMax), 3))
            self.hpbar.fill((255,0,0))
            self.hpbar.set_alpha(240)
            self.hpRect = self.hpbar.get_rect()
            self.hpRect.move_ip(pos)


    def death(self):
        self.before = 'dying0'
        self.direction = (0,0)

class OrcBerserker(Orc):

    def __init__(self, pos, lista_im, speed, direction):
        Orc.__init__(self, pos, lista_im, speed, direction)
        self.attack = 7
        self.health = 45
        self.healthMax = 45

class BlueOrc(Orc):
    def __init__(self, pos, lista_im, speed, direction):
        Orc.__init__(self, pos, lista_im, speed, direction)
        self.attack = 5
        self.health = 55
        self.healthMax = 55


def creaGrup(l):
    grup = pygame.RenderPlain()
    for var in l:
        grup.add(var)
    return grup
