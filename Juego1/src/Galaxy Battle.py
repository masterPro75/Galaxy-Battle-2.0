import pygame, sys
from pygame.locals import *
from random import randint

ancho = 900
alto = 480
listaEnemigo = []

class Jugador(pygame.sprite.Sprite):
        "Clase de personajes"
        def __init__(self):
            self.imagen_nave = pygame.image.load("Imagenes\Nave.png")
            self.imagen_explosion = pygame.image.load("Imagenes\explosion.png")
            self.rect = self.imagen_nave.get_rect()
            self.rect.centerx = ancho/2
            self.rect.centery = alto - 60
            self.Vida = True
            self.velocidad = 5
            self.listaDisparo = []

            self.sonidoDisparo = pygame.mixer.Sound("Sonidos\jugador_disparo.wav")
            self.sonidoExplosion = pygame.mixer.Sound("Sonidos\destruccionJugador.wav")

        def dibujar(self, superficie):
            superficie.blit(self.imagen_nave, self.rect)

        def dibujarExplosion(self, superficie):
            superficie.blit(self.imagen_explosion, self.rect)
        
        def mover(self, izq, der):
                if izq:
                        self.moverIzquierda()
                elif der:
                        self.moverDerecha()
           
        def moverIzquierda(self):
                self.rect.left -= self.velocidad
                self.movimiento()
                self.direccion = 'O'

        def moverDerecha(self):
                self.rect.right += self.velocidad
                self.movimiento()
                self.direccion = 'E'

        def movimiento(self):
                if self.Vida == True:
                        if self.rect.left < 0:
                                self.rect.left = 0
                        elif self.rect.right > ancho:
                                self.rect.right = ancho

        def disparo(self, x , y):
                miProyectil = Proyectil(x, y, "Imagenes\disparo_laser.png" , True)
                self.listaDisparo.append(miProyectil)
                self.sonidoDisparo.play()

        def destruccion(self):
                self.sonidoExplosion.play()
                self.imagen_nave = self.imagen_explosion
                detenerTodo()
                self.Vida = False
                self.velocidad = 0
                
class Proyectil(pygame.sprite.Sprite):
        "Clase de disparo"
        def __init__(self, posx ,posy, ruta, personaje):
                pygame.sprite.Sprite.__init__(self)
                
                self.imagenProyectil = pygame.image.load(ruta)
                self.rect = self.imagenProyectil.get_rect()
                self.velocidadDisparo = 10

                self.rect.top = posy
                self.rect.left = posx
                
                self.disparoPersonaje = personaje
                

        def trayectoria(self):
                if self.disparoPersonaje == True:
                        self.rect.top = self.rect.top - self.velocidadDisparo
                else:
                        self.rect.top = self.rect.top + self.velocidadDisparo 
                

        def dibujar(self , superficie):
                superficie.blit(self.imagenProyectil, self.rect)
                

class Invasor(pygame.sprite.Sprite):
        "Clase de enemigos"
        def __init__(self,posx,posy,distancia,imagen1):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_enemigo = pygame.image.load(imagen1)
                
                
                self.listaImagenes= [self.imagen_enemigo]
                self.posImagen = 0

                self.imagenInvasor = self.listaImagenes[self.posImagen]
                self.rect = self.imagen_enemigo.get_rect()
                
                self.velocidad = 3
                self.listaDisparo = []
                self.rect.top = posy
                self.rect.left= posx
                
                self.rangoDisparo = 1
                self.tiempoCambio = 1

                self.conquista = False

                self.derecha = True
                self.contador = 0
                self.Maxdescenso = self.rect.top + 40

                self.limiteDerecha=posx+ distancia
                self.limiteIzquierda=posx-distancia

                self.sonidoDisparoEnemigo = pygame.mixer.Sound("Sonidos\enemigo_disparo.wav")

        def dibujar(self, superficie):
                superficie.blit(self.imagen_enemigo, self.rect)

        def comportamiento(self, tiempo):
                if self.conquista== False:
                        self.movimientos()
                        self.ataque()
                        if self.tiempoCambio == tiempo:
                                self.posImagen +=1
                                self.tiempoCambio +=1

        def movimientos(self):
                if self.contador < 3:
                        self.movimientoLateral()
                else:
                        self.descenso()

        def descenso(self):
                if self.Maxdescenso == self.rect.top:
                        self.contador = 0
                        self.Maxdescenso = self.rect.top +40
                else:
                        self.rect.top += 1

        def movimientoLateral(self):
                if self.derecha==True:
                        self.rect.left = self.rect.left + self.velocidad
                        if self.rect.left > self.limiteDerecha:
                                self.derecha = False
                                self.contador += 1
                else:
                        self.rect.left = self.rect.left - self.velocidad
                        if self.rect.left < self.limiteIzquierda:
                                self.derecha = True
        
        def ataque(self):
                if (randint(0,100)<self.rangoDisparo):
                        self.disparo()

        def disparo(self):
                x,y = self.rect.center
                miProyectil = Proyectil(x, y ,"Imagenes\disparo.png", False)
                self.listaDisparo.append(miProyectil)
                self.sonidoDisparoEnemigo.play()


"Main"

def detenerTodo():
        for enemigo in listaEnemigo:
                for disparo in enemigo.listaDisparo:
                        enemigo.listaDisparo.remove(disparo)

                enemigo.conquista= True

def pausa():
        pausado = True
        while pausado:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_c:
                                        pausado = False
                                elif event.key == pygame.K_q:
                                        pygame.quit()
                                        quit()
                Fuente = pygame.font.SysFont("Comic Sans MS",30)
                TextPause = Fuente.render("Paused",-100,(120,100,40))
                TextPause2= Fuente.render("Press C key to continue or Q key to quit game",25,(120,100,40))
                ventana.blit(TextPause,(400,200))
                ventana.blit(TextPause2,(100,400))
                pygame.display.update()
                reloj.tick(5)

##def gameLoop():
##        gameExit = False
##        gameOver = False
## 
##        while not gameExit:
##                while not gameOver == True:
##                        pygame.display.update()
##                        for event in pygame.event.get():
##                                if event.type == pygame.KEYDOWN:
##                                        if event.key == pygame.K_c:
##                                                gameLoop()
##                                        if event.key == pygame.K_q:
##                                                gameExit=True
##                                                gameOver=False
##                                                
##                        #Fuente = pygame.font.SysFont("Comic Sans MS",30)
##                        #imagen_fondo = pygame.image.load("Imagenes\Fondo2.jpg")
##                        #ventana.blit(imagen_fondo, (0, 0))
##                        #TextMenu = Fuente.render("Menu principal",0,(120,100,40))
                        

        
def puntos(score):
        FuenteScore = pygame.font.SysFont("Comic Sans MS",30)
        textScore = FuenteScore.render("Score: "+str(score), True, (120,100,40))
        ventana.blit(textScore,(0,0))
        #superficie.blit(textScore, [0,0]

def salud_nave(salud):
        FuenteSalud = pygame.font.SysFont("Comic Sans MS",30)
        textSalud = FuenteSalud.render("Health: "+str(salud)+"%", True, (120,100,40))
        ventana.blit(textSalud,(0,30))

def game_intro():
        intro = True
        while intro:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                intro = False
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_c:
                                        
                                        gameLoop()
                                if event.key == pygame.K_q:
                                        pygame.quit()
                                        sys.exit()
                                if event.key == pygame.K_h:
                                        imagenFondo = pygame.image.load("Imagenes\Fondo2.jpg")
                                        ventana.blit(imagenFondo, (0, 0))
                                        mostrando = True
                                        while mostrando:
                                                FuenteHighScore = pygame.font.SysFont("Comic Sans MS",30)
                                                textHS = FuenteHighScore.render("High Scores",-210,(66,203,244))
                                                text1 = FuenteHighScore.render(" 1... 1000",-210,(66,203,244))
                                                text2 = FuenteHighScore.render(" 2... 950",-210,(66,203,244))
                                                text3 = FuenteHighScore.render(" 3... 900",-210,(66,203,244))
                                                text4 = FuenteHighScore.render(" 4... 850",-210,(66,203,244))
                                                text5 = FuenteHighScore.render(" 5... 800",-210,(66,203,244))
                                                text6 = FuenteHighScore.render(" 6... 750",-210,(66,203,244))
                                                text7 = FuenteHighScore.render(" 7... 700",-210,(66,203,244))
                                                text8 = FuenteHighScore.render(" 8... 650",-210,(66,203,244))
                                                text9 = FuenteHighScore.render(" 9... 600",-210,(66,203,244))
                                                text10 =FuenteHighScore.render("10... 550",-210,(66,203,244))
                                                textBack=FuenteHighScore.render("Press B key to back to main menu",-210,(244,203,66))
                                                ventana.blit(textHS,(100,0))
                                                ventana.blit(text1,(150,100))
                                                ventana.blit(text2,(150,150))
                                                ventana.blit(text3,(150,200))
                                                ventana.blit(text4,(150,250))
                                                ventana.blit(text5,(150,300))
                                                ventana.blit(text6,(450,100))
                                                ventana.blit(text7,(450,150))
                                                ventana.blit(text8,(450,200))
                                                ventana.blit(text9,(450,250))
                                                ventana.blit(text10,(450,300))
                                                ventana.blit(textBack,(100,400))
                                                pygame.display.update()
                                                reloj.tick(60)
                                                for evento in pygame.event.get():
                                                        if evento.type == pygame.QUIT:
                                                                pygame.quit()
                                                                sys.exit()
                                                        if evento.type == pygame.KEYDOWN:
                                                                if evento.key == K_b:
                                                                        mostrando=False
                                        
                imagenFondo = pygame.image.load("Imagenes\Fondo2.jpg")
                ventana.blit(imagenFondo, (0, 0))
                FuenteIntro = pygame.font.SysFont("Comic Sans MS",30)
                FuenteGrande= pygame.font.SysFont("Comic Sans MS",60)
                FuenteMediana=pygame.font.SysFont("Comic Sans MS",45)
                textIntro = FuenteGrande.render("Welcome to Galaxy Battle",-200,(244,122,66))
                textIntro2 =FuenteMediana.render("CONTROLS: ",-130,(244,223,66))
                textIntro3 =FuenteIntro.render("Use LEFT-RIGHT ARROWS keys to move the ship",-170,(66,203,244))
                textIntro4 =FuenteIntro.render("Press SPACEBAR key to shoot enemies",-210,(66,203,244))
                textIntro5 =FuenteIntro.render("Press C to play or Q to quit",-210,(244,233,66))
                textIntro6 =FuenteIntro.render("Press H key to view high score",-210,(244,233,66))
                ventana.blit(textIntro,(100,0))
                ventana.blit(textIntro2,(150,100))
                ventana.blit(textIntro3,(150,200))
                ventana.blit(textIntro4,(150,250))
                ventana.blit(textIntro5,(200,350))
                ventana.blit(textIntro6,(200,400))
                pygame.display.update()
                reloj.tick(15)

def cargarEnemigos():
        posx = 100
        for x in range(1,5):
                enemigo = Invasor(posx,120,80,"Imagenes\Naveenemiga1.png")
                listaEnemigo.append(enemigo)
                posx = posx + 200

        posx = 100
        for x in range(1,5):
                enemigo = Invasor(posx,0,80,"Imagenes\spaceship_sprite.png")
                listaEnemigo.append(enemigo)
                posx = posx + 200

        posx = 100
        for x in range(1,5):
                enemigo = Invasor(posx,-120,80,"Imagenes\Naveenemiga1.png")
                listaEnemigo.append(enemigo)
                posx = posx + 200

def mostrar_gameOver():
        FuenteSistema = pygame.font.SysFont("Comic Sans MS",30)
        Texto = FuenteSistema.render("Game Over",0,(120,100,40))
        Texto2 = FuenteSistema.render("Press R key to restart game again",0,(120,100,40))
        ventana.blit(Texto,(100,0))
        ventana.blit(Texto2,(100,200))
        pygame.display.update()
        reloj.tick(60)

def vaciar_lista_enemigo():
        for enemigo in listaEnemigo[:]:
                listaEnemigo.remove(enemigo)
pygame.init()
pygame.mixer.music.load("Sonidos\musica.wav")
pygame.mixer.music.play(3)

def gameLoop():
        
        imagenFondo = pygame.image.load("Imagenes\Fondo.jpg")
        ventana.blit(imagenFondo, (0, 0))
        
        FuenteSistema = pygame.font.SysFont("Comic Sans MS",30)
        Texto = FuenteSistema.render("Game Over",0,(120,100,40))
        Texto2 = FuenteSistema.render("Press R key to play again or Q to exit",0,(120,100,40))

        jugador = Jugador()
        vaciar_lista_enemigo()
        cargarEnemigos()
        score = 0
        contadorNaves=12
        salud=100
        enJuego = True
        derechaApretada = False
        izquierdaApretada = False
        
        
        while enJuego:
            ventana.blit(imagenFondo,(0,0))
            #jugador.dibujar()
            reloj.tick(60)    
            tiempo = pygame.time.get_ticks()/1000
              
            for evento in pygame.event.get():
                        if evento.type == QUIT: #agregar la salida al menu y guardado de score
                                pygame.quit()
                                sys.exit()
                        if enJuego== True:        
                                if evento.type == pygame.KEYDOWN:
                                        if evento.key == K_LEFT:
                                                izquierdaApretada = True
                                                jugador.moverIzquierda()
                                        elif evento.key == K_RIGHT:
                                                derechaApretada = True
                                                jugador.moverDerecha()
                                        elif evento.key == K_SPACE:
                                                x,y = jugador.rect.center
                                                jugador.disparo(x,y)
                                        elif evento.key == pygame.K_p:
                                                pausa()
                                        

                                if evento.type == pygame.KEYUP:
                                        if evento.key == K_LEFT:
                                                izquierdaApretada = False
                                        elif evento.key == K_RIGHT:
                                                derechaApretada = False

                        

            jugador.mover(izquierdaApretada, derechaApretada)
            

            if len(jugador.listaDisparo) > 0:
                for x in jugador.listaDisparo:
                        x.dibujar(ventana)
                        x.trayectoria()
                        enemigoGolpeado = False
                        if not x.rect.top > 0:
                                jugador.listaDisparo.remove(x)
                        else:
                                for enemigo in listaEnemigo:
                                        if x.rect.colliderect(enemigo.rect) and not enemigoGolpeado:
                                                listaEnemigo.remove(enemigo)
                                                jugador.listaDisparo.remove(x)
                                                contadorNaves=contadorNaves - 1
                                                if contadorNaves == 0:
                                                        contadorNaves=12
                                                        cargarEnemigos()
                                                        salud=salud+20
                                                enemigoGolpeado = True
                                                score = score + 10
            puntos(score)
            salud_nave(salud)

            if len(listaEnemigo)>0:
                    for enemigo in listaEnemigo:
                            enemigo.comportamiento(tiempo)
                            enemigo.dibujar(ventana)

                            if enemigo.rect.colliderect(jugador.rect):
                                    jugador.destruccion()    
                                    enJuego=False
                                    detenerTodo()

                                
                            if len(enemigo.listaDisparo) > 0:
                                for x in enemigo.listaDisparo:
                                        x.dibujar(ventana)
                                        x.trayectoria()
                                        if x.rect.colliderect(jugador.rect):
                                                salud=salud - 20
                                                enemigo.listaDisparo.remove(x)
                                                if salud <= 0:
                                                        enJuego=False
                                                        jugador.destruccion()
                                                        detenerTodo()
                                                
                                                                
                                        if not x.rect.top > -5:
                                                enemigo.listaDisparo.remove(x)
                                        else:
                                                for disparo in jugador.listaDisparo:
                                                        if x.rect.colliderect(disparo.rect):
                                                                jugador.listaDisparo.remove(disparo)
                                                                #enemigo.listaDisparo.remove(x)
            

                    
                    
            jugador.dibujar(ventana)
            pygame.display.update()
            
        
        
        enJuego=True
        while enJuego:
            #pygame.mixer.music.fadeout(3000)
            ventana.blit(Texto,(300,300))
            ventana.blit(Texto2,(200,400))
            pygame.display.update()
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                    pygame.quit()
                                    sys.exit()
                            if event.key == pygame.K_r:
                                    enJuego=False
        return
pygame.init()
reloj = pygame.time.Clock()
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Galaxy Battle 2.0")
game_intro()
pygame.quit()
quit()
