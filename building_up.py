import random
from secrets import choice
from turtle import resizemode
from tkinter import *
import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
from random import choice


pygame.mixer.pre_init(44100,-16,2,4096)
pygame.init()

clock = pygame.time.Clock()
fps = 60

ekran_genislik = 800
ekran_yukseklik = 800

ekran = pygame.display.set_mode((ekran_genislik,ekran_yukseklik))
pygame.display.set_caption('Building Up!')

font = pygame.font.SysFont('Impact', 70)
font_skor = pygame.font.SysFont('Impact', 20)

doseme_boyutu = 40
game_over = 0
ana_menu = True
level = 1
skor = 0

siyah = (31,29,26)
# resimler
ana_menu_resim = pygame.image.load('resimler/ana_menu_resim.png')
arkaplan_resim = pygame.image.load('resimler/arkaplan.png')
arkaplan_darkresim = pygame.image.load('resimler/arkaplan_dark.png')
arkaplan_lightresim = pygame.image.load('resimler/arkaplan_light.png')
arkaplan_yesilresim = pygame.image.load('resimler/arkaplan_yesil.png')
tamamlama_resim = pygame.image.load('resimler/tamamlama.png')
bitiris_resim = pygame.image.load('resimler/bitiris.png')
bastan_basla_resim = pygame.image.load('resimler/bastan_basla_resim.png')
basla_resim = pygame.image.load('resimler/baslama_resim.png')
cikis_resim = pygame.image.load('resimler/cikis_resim.png')
sonraki_resim = pygame.image.load('resimler/sonraki.png')

# ses ve müzik

ara_ekran_calma = True
secme_fx_calma = True
intro_calma = True
bitis_calma = True
Level1_calma = True
Level2_calma = True
Level3_calma = True
Level4_calma = True
Level5_calma = True

disket_fx1 = pygame.mixer.Sound('sesler/altinsesi1.wav')
disket_fx1.set_volume(0.5)
ziplama_fx = pygame.mixer.Sound('sesler/ziplama.wav')
ziplama_fx.set_volume(0.5)
olme_fx = pygame.mixer.Sound('sesler/olmesesi.wav')
olme_fx.set_volume(0.5)
secme_fx = pygame.mixer.Sound('sesler/secmesesi.wav')
secme_fx.set_volume(0.5)
giris_ekrani_m = pygame.mixer.Sound('sesler/intro.wav')
giris_ekrani_m.set_volume(0.5)
ara_ekran_m = pygame.mixer.Sound('sesler/kazanmasesi.wav')
ara_ekran_m.set_volume(0.5)
bitis_ekrani_m = pygame.mixer.Sound('sesler/bitissesi.wav')
bitis_ekrani_m.set_volume(0.5)

# Level Müzikleri
L_1_0_M = pygame.mixer.Sound('sesler/L1-0.wav')
L_1_1_M = pygame.mixer.Sound('sesler/L1-1.wav')
L_1_1_M.set_volume(1.5)
L_1_2_M = pygame.mixer.Sound('sesler/L1-2.wav')
L_1_3_M = pygame.mixer.Sound('sesler/L1-3.wav')

L_2_0_M = pygame.mixer.Sound('sesler/L2-0.wav')
L_2_1_M = pygame.mixer.Sound('sesler/L2-1.wav')
L_2_2_M = pygame.mixer.Sound('sesler/L2-2.wav')
L_2_3_M = pygame.mixer.Sound('sesler/L2-3.wav')

L_3_0_M = pygame.mixer.Sound('sesler/L3-0.wav')
L_3_1_M = pygame.mixer.Sound('sesler/L3-1.wav')
L_3_2_M = pygame.mixer.Sound('sesler/L3-2.wav')
L_3_3_M = pygame.mixer.Sound('sesler/L3-3.wav')

L_4_0_M = pygame.mixer.Sound('sesler/L4-0.wav')
L_4_1_M = pygame.mixer.Sound('sesler/L4-1.wav')
L_4_2_M = pygame.mixer.Sound('sesler/L4-2.wav')
L_4_3_M = pygame.mixer.Sound('sesler/L4-3.wav')

L_5_0_M = pygame.mixer.Sound('sesler/L5-0.wav')
L_5_1_M = pygame.mixer.Sound('sesler/L5-1.wav')
L_5_2_M = pygame.mixer.Sound('sesler/L5-2.wav')
L_5_3_M = pygame.mixer.Sound('sesler/L5-3.wav')


def yazi_yaz(yazi,font,yazi_rengi,x,y):
    yazi = font.render(yazi,True,yazi_rengi)
    ekran.blit(yazi,(x,y))

def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(ekran, (255, 255, 255), (0, line * doseme_boyutu), (ekran_genislik, line * doseme_boyutu))
        pygame.draw.line(ekran, (255, 255, 255), (line * doseme_boyutu, 0), (line * doseme_boyutu, ekran_yukseklik))

def reset_level(Level):
    oyuncu.reset(80, ekran_yukseklik - 80)
    dusman_grup.empty()
    diken_grup.empty()
    cikis_grup.empty()
    disket_grup.empty()
    gitar_grup.empty()
    bateri_grup.empty()
    klavye_grup.empty()
    # dünya datasını yükleme
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        dunya_data = pickle.load(pickle_in)
    dunya = Dunya(dunya_data)

    return dunya


class Buton():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tiklandi = False
    
    def olustur(self):
        aksiyon = False

        pozisyon = pygame.mouse.get_pos()

        if self.rect.collidepoint(pozisyon):
            if pygame.mouse.get_pressed()[0] == 1 and self.tiklandi == False:
                aksiyon = True
                self.tiklandi = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.tiklandi = False

        ekran.blit(self.image,self.rect)

        return aksiyon


class Oyuncu():

    def __init__(self, x, y):
        self.reset(x,y)
    
    def update(self, game_over):
        dx = 0
        dy = 0
        yurume_sayac = 5.2

        if game_over == 0:
        
            tus = pygame.key.get_pressed()

        
            if tus[pygame.K_w] and self.ziplama == False and self.havada == False:
                ziplama_fx.play()
                self.hiz_y = -15
                self.ziplama = True
                
                
            if tus[pygame.K_w] == False:
                self.ziplama = False
                self.sayac += 1
                self.yon = 2
                
                
            if tus[pygame.K_a]:
                dx -= 5
                self.sayac += 1
                self.yon = -1
                
            if tus[pygame.K_d]:
                dx += 5
                self.sayac += 1
                self.yon = 1
            if tus[pygame.K_a] == False and tus[pygame.K_d] == False:
                self.sayac = 0
                self.index = 0
                idle_resim = pygame.image.load('resimler/oyuncu_idle.png')
                idle = pygame.transform.smoothscale(idle_resim,(32,40))
                self.resim = idle

            # animasyonlar
            if self.sayac > yurume_sayac:
                    self.sayac = 0
                    self.index += 1
                    if self.index >= len(self.resimler_sag):
                        self.index = 0
                    if self.yon == 1:
                        self.resim = self.resimler_sag[self.index]
                    if self.yon == -1:
                        self.resim = self.resimler_sol[self.index]
                
            
            


            self.hiz_y +=  1
            if self.hiz_y > 10:
                self.hiz_y = 10
            dy += self.hiz_y

            # çakışma
            self.havada = True
            for doseme in dunya.doseme_listesi:
                if doseme[1].colliderect(self.rect.x + dx, self.rect.y, self.genislik, self.yukseklik):

                    dx = 0

                if doseme[1].colliderect(self.rect.x, self.rect.y + dy, self.genislik, self.yukseklik):
                    if self.hiz_y < 0:
                        dy = doseme[1].bottom - self.rect.top 
                        self.hiz_y = 0
                    elif self.hiz_y >= 0:
                        dy = doseme[1].top - self.rect.bottom
                        self.havada = False
                    
            if pygame.sprite.spritecollide(self, dusman_grup, False):
                olme_fx.play()
                game_over = -1
            
            if pygame.sprite.spritecollide(self, diken_grup, False):
                olme_fx.play()
                game_over = -1
            
            if pygame.sprite.spritecollide(self, cikis_grup, False):
                game_over = 1
                
            
            
            
            
                    

                


            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.resim = self.olum_resim
            yazi_yaz('KAYBETTİN!', font,siyah, (ekran_genislik// 2) - 150, (ekran_yukseklik// 2) -200)
            if self.rect.y > -50:
                self.rect.y -= 7

            


        ekran.blit(self.resim,self.rect)
        return game_over

    def reset(self,x,y):

        self.resimler_sag = []
        self.resimler_sol = []
        self.index = 0
        self.sayac = 0
        
        for num in range(1,5):
            resim_sag = pygame.image.load(f'resimler/oyuncu{num}.png')
            if num == 1:
                resim_sag = pygame.transform.smoothscale(resim_sag, (32,40))
            if num == 2:
                resim_sag = pygame.transform.smoothscale(resim_sag, (32.8,38.2))
            if num == 3:
                resim_sag = pygame.transform.smoothscale(resim_sag, (32.8,37.3))
            if num == 4:
                resim_sag = pygame.transform.smoothscale(resim_sag, (42.6,32))
            self.resimler_sag.append(resim_sag)
            self.resimler_sol.append(pygame.transform.flip(resim_sag, True, False))
        self.olum_resim = pygame.image.load('resimler/oyuncu_oldu.png')
        self.resim = self.resimler_sag[self.index]
        self.rect = self.resim.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.genislik = self.resim.get_width()
        self.yukseklik = self.resim.get_height()
        self.hiz_y = 0
        self.ziplama = False
        self.yon = 0
        self.havada = True

class Dunya():
    def __init__(self,data):

        self.doseme_listesi = []

        toprak = pygame.image.load('resimler/toprak.png')
        yer_orta = pygame.image.load('resimler/yer_orta.png')
        yer_sol = pygame.image.load('resimler/yer_sol.png')
        yer_sag = pygame.image.load('resimler/yer_sag.png')
        yer_tek = pygame.image.load('resimler/yer_tek.png')
        

        satir_sayaci = 0
        for satir in data:
            sutun_sayaci = 0
            for doseme in satir:
                if doseme == 1:
                    resim = pygame.transform.smoothscale(toprak,(doseme_boyutu,doseme_boyutu))
                    resim_rect = resim.get_rect()
                    resim_rect.x = sutun_sayaci * doseme_boyutu
                    resim_rect.y = satir_sayaci * doseme_boyutu
                    doseme = (resim, resim_rect)
                    self.doseme_listesi.append(doseme)
                if doseme == 2:
                    resim = pygame.transform.smoothscale(yer_orta,(doseme_boyutu,doseme_boyutu))
                    resim_rect = resim.get_rect()
                    resim_rect.x = sutun_sayaci * doseme_boyutu
                    resim_rect.y = satir_sayaci * doseme_boyutu
                    doseme = (resim, resim_rect)
                    self.doseme_listesi.append(doseme)
                if doseme == 3:
                    resim = pygame.transform.smoothscale(yer_sol,(doseme_boyutu,doseme_boyutu))
                    resim_rect = resim.get_rect()
                    resim_rect.x = sutun_sayaci * doseme_boyutu
                    resim_rect.y = satir_sayaci * doseme_boyutu
                    doseme = (resim, resim_rect)
                    self.doseme_listesi.append(doseme)
                if doseme == 4:
                    resim = pygame.transform.scale(yer_sag,(doseme_boyutu,doseme_boyutu))
                    resim_rect = resim.get_rect()
                    resim_rect.x = sutun_sayaci * doseme_boyutu
                    resim_rect.y = satir_sayaci * doseme_boyutu
                    doseme = (resim, resim_rect)
                    self.doseme_listesi.append(doseme)
                if doseme == 5:
                    resim = pygame.transform.smoothscale(yer_tek,(doseme_boyutu,doseme_boyutu))
                    resim_rect = resim.get_rect()
                    resim_rect.x = sutun_sayaci * doseme_boyutu
                    resim_rect.y = satir_sayaci * doseme_boyutu
                    doseme = (resim, resim_rect)
                    self.doseme_listesi.append(doseme)
                if doseme == 6:
                    dusman = Dusman(sutun_sayaci * doseme_boyutu, satir_sayaci * doseme_boyutu)
                    dusman_grup.add(dusman)
                if doseme == 7:
                    diken = Diken(sutun_sayaci * doseme_boyutu, satir_sayaci * doseme_boyutu + (doseme_boyutu// 2))
                    diken_grup.add(diken)
                if doseme == 8:
                    cikis = Cikis_Kapisi(sutun_sayaci * doseme_boyutu + 8, satir_sayaci * doseme_boyutu - (doseme_boyutu//2) -4)
                    cikis_grup.add(cikis)
                if doseme == 9:
                    disket = Disket(sutun_sayaci * doseme_boyutu + (doseme_boyutu //2) - 12, satir_sayaci * doseme_boyutu + (doseme_boyutu //2) - 12)
                    disket_grup.add(disket)
                if doseme == 10:
                    klavye = Klavye(sutun_sayaci * doseme_boyutu, satir_sayaci * doseme_boyutu)
                    klavye_grup.add(klavye)
                if doseme == 11:
                    gitar = Gitar(sutun_sayaci * doseme_boyutu, satir_sayaci * doseme_boyutu)
                    gitar_grup.add(gitar)
                if doseme == 12:
                    bateri = Bateri(sutun_sayaci * doseme_boyutu, satir_sayaci * doseme_boyutu)
                    bateri_grup.add(bateri)
                sutun_sayaci += 1
            satir_sayaci += 1
        
    def olustur(self):
        for doseme in self.doseme_listesi:
            ekran.blit(doseme[0],doseme[1])

class Dusman(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.dusman_list = []
        self.dusman_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/dusman_0.png'),(42,40)))
        self.dusman_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/dusman_1.png'),(42,40)))
        self.dusman_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/dusman_2.png'),(42,40)))
        self.dusman_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/dusman_3.png'),(42,40)))
        self.dusman_anlik = 0
        self.image = self.dusman_list[self.dusman_anlik]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.yon = 1
        self.hareket_sayaci = 0
    
    def update(self):
        self.dusman_anlik += 0.1
        if self.dusman_anlik >= len(self.dusman_list):
            self.dusman_anlik = 0
        self.image = self.dusman_list[int(self.dusman_anlik)]
        self.rect.x += self.yon
        self.hareket_sayaci += 1
        if abs(self.hareket_sayaci) > 50:
            self.image = pygame.transform.flip(self.dusman_list[int(self.dusman_anlik)],True,True)
            self.yon *= -1
            self.hareket_sayaci *= -1

class Diken(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.diken_list = []
        self.diken_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/diken_0.png'),(doseme_boyutu, doseme_boyutu // 2)))
        self.diken_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/diken_1.png'),(doseme_boyutu, doseme_boyutu // 2)))
        self.diken_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/diken_2.png'),(doseme_boyutu, doseme_boyutu // 2)))
        self.diken_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/diken_3.png'),(doseme_boyutu, doseme_boyutu // 2)))
        self.diken_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/diken_4.png'),(doseme_boyutu, doseme_boyutu // 2)))
        self.diken_anlik = 0
        self.image = self.diken_list[self.diken_anlik]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.diken_anlik += 0.2

        if self.diken_anlik >= len(self.diken_list):
            self.diken_anlik = 0
        
        self.image = self.diken_list[int(self.diken_anlik)]

class Disket(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.disket_list = []
        self.disket_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/disket_0.png'),(25 , 25)))
        self.disket_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/disket_1.png'),(25 , 25)))
        self.disket_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/disket_2.png'),(25 , 25)))
        self.disket_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/disket_3.png'),(25 , 25)))
        self.disket_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/disket_4.png'),(25 , 25)))
        self.disket_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/disket_5.png'),(25 , 25)))
        
        
        self.disket_anlik = 0
        self.image = self.disket_list[self.disket_anlik]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.disket_anlik += 0.2

        if self.disket_anlik >= len(self.disket_list):
            self.disket_anlik = 0
        
        self.image = self.disket_list[int(self.disket_anlik)]

class Klavye(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.klavye_list = []
        self.klavye_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/klavye_0.png'),(doseme_boyutu, doseme_boyutu)))
        self.klavye_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/klavye_1.png'),(doseme_boyutu, doseme_boyutu)))
        self.klavye_anlik = 0
        self.image = self.klavye_list[self.klavye_anlik]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.klavye_anlik += 0.2

        if self.klavye_anlik >= len(self.klavye_list):
            self.klavye_anlik = 0
        
        self.image = self.klavye_list[int(self.klavye_anlik)]

class Gitar(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.gitar_list = []
        self.gitar_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/gitar_0.png'),(doseme_boyutu, doseme_boyutu)))
        self.gitar_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/gitar_1.png'),(doseme_boyutu, doseme_boyutu)))

        self.gitar_anlik = 0
        self.image = self.gitar_list[self.gitar_anlik]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.gitar_anlik += 0.2

        if self.gitar_anlik >= len(self.gitar_list):
            self.gitar_anlik = 0
        
        self.image = self.gitar_list[int(self.gitar_anlik)]
    
class Bateri(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.bateri_list = []
        self.bateri_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/bateri_0.png'),(doseme_boyutu, doseme_boyutu)))
        self.bateri_list.append(pygame.transform.smoothscale(pygame.image.load('resimler/bateri_1.png'),(doseme_boyutu, doseme_boyutu)))
  
        self.bateri_anlik = 0
        self.image = self.bateri_list[self.bateri_anlik]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.bateri_anlik += 0.2

        if self.bateri_anlik >= len(self.bateri_list):
            self.bateri_anlik = 0
        
        self.image = self.bateri_list[int(self.bateri_anlik)]

class Cikis_Kapisi(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        resim = pygame.image.load('resimler/cikis_kapisi.png')
        self.image = pygame.transform.smoothscale(resim, (int(doseme_boyutu * 1.6) , int(doseme_boyutu * 1.6)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



oyuncu = Oyuncu(80, ekran_yukseklik - 80)
dusman_grup = pygame.sprite.Group()
diken_grup = pygame.sprite.Group()
cikis_grup = pygame.sprite.Group()
disket_grup = pygame.sprite.Group()
klavye_grup = pygame.sprite.Group()
gitar_grup = pygame.sprite.Group()
bateri_grup = pygame.sprite.Group()

skor_simgesi = Disket(doseme_boyutu//2 + 22,doseme_boyutu//2 + 22)
disket_grup.add(skor_simgesi)

if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    dunya_data = pickle.load(pickle_in)
dunya = Dunya(dunya_data)



bastan_basla_buton = Buton(ekran_genislik // 2 - 90, ekran_yukseklik // 2 - 100, bastan_basla_resim)
baslama_buton = Buton(ekran_genislik // 2 -250, ekran_yukseklik // 2 + 100, basla_resim)
cikis_buton = Buton(ekran_genislik // 2 + 50, ekran_yukseklik // 2 + 100, cikis_resim)
bastan_basla2_buton = Buton(ekran_genislik // 2 - 70, ekran_yukseklik // 2 - 120, bastan_basla_resim)
sonraki_buton = Buton(ekran_genislik // 2 - 80, ekran_yukseklik // 2 - 180, sonraki_resim)
cikis2_buton = Buton(ekran_genislik // 2 - 70, ekran_yukseklik // 2 - 60, cikis_resim)

calisma = True

while calisma:

    clock.tick(fps)
    
    if ana_menu == True:
        ekran.blit(ana_menu_resim,(0,0))
        if intro_calma:
            pygame.mixer.music.load('sesler/intro.wav')
            pygame.mixer.music.play(0)
            intro_calma = False
        if cikis_buton.olustur():
            calisma = False
        if baslama_buton.olustur():
            pygame.mixer.music.stop()
            ana_menu = False
    else:
        if secme_fx_calma:
            secme_fx_calma = False
            secme_fx.play()
        if level == 1:
            ekran.blit(arkaplan_resim,(0,0))
        if level == 2:
            ekran.blit(arkaplan_yesilresim,(0,0))
        if level == 3:
            ekran.blit(arkaplan_darkresim,(0,0))
        if level == 4:
            ekran.blit(arkaplan_lightresim,(0,0))
        if level == 5:
            ekran.blit(arkaplan_resim,(0,0))
        dunya.olustur()

        if game_over == 0:
                bitis_ekrani_m.stop()
                if level == 1 and Level1_calma:
                    Level1_calma = False
                    oyuncu = Oyuncu(80, ekran_yukseklik - 80)
                    L_1_0_M.play(-1)
                    L_1_0_M.set_volume(0.3)

                    dusman_grup.update()
                if level == 2 and Level2_calma:
                    ekran.blit(arkaplan_yesilresim,(0,0))
                    Level2_calma = False
                    oyuncu = Oyuncu(160, ekran_yukseklik - 400)
                    L_2_0_M.play(-1)
                    
                    
                    dusman_grup.update()

                if level == 3 and Level3_calma:
                    ekran.blit(arkaplan_darkresim,(0,0))
                    Level3_calma = False
                    oyuncu = Oyuncu(80, ekran_yukseklik - 700)
                    L_3_0_M.play(-1)

                    dusman_grup.update()
                
                if level == 4 and Level4_calma:
                    ekran.blit(arkaplan_lightresim,(0,0))
                    Level4_calma = False
                    oyuncu = Oyuncu(365, ekran_yukseklik - 300)
                    L_4_0_M.play(-1)

                    dusman_grup.update()

                if level == 5 and Level5_calma:
                    Level5_calma = False
                    oyuncu = Oyuncu(80, ekran_yukseklik - 80)
                    L_5_0_M.play(-1)

                    dusman_grup.update()
                
                if pygame.sprite.spritecollide(oyuncu,disket_grup, True):
                    disket_fx1.play()
                    skor += 1
                yazi_yaz('x ' + str(skor), font_skor, siyah, doseme_boyutu + 30, 42)

                # GİTAR

                if pygame.sprite.spritecollide(oyuncu,gitar_grup, True):
                    if level == 1:
                        L_1_0_M.stop()
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.load('sesler/L1-0.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_1_1_M.play(-1)
                    if level == 2:
                        L_2_0_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L2-0.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_2_1_M.play(-1)
                        L_2_1_M.set_volume(0.5)
                    if level == 3:
                        L_3_0_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L3-0.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_3_1_M.play(-1)
                    if level == 4:
                        L_4_0_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L4-0.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_4_1_M.play(-1)
                    if level == 5:
                        L_5_0_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L5-0.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_5_1_M.play(-1)

                # DAVUL        

                if pygame.sprite.spritecollide(oyuncu,bateri_grup, True):
                    if level == 1:
                        L_1_1_M.stop()
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.load('sesler/L1-1.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_1_2_M.play(-1)
                    if level == 2:
                        L_2_1_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L2-1.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_2_2_M.play(-1)
                        L_2_2_M.set_volume(0.5)
                    if level == 3:
                        L_3_1_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L3-1.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_3_2_M.play(-1)
                    if level == 4:
                        L_4_1_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L4-1.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_4_2_M.play(-1)
                    if level == 5:
                        L_5_1_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L5-1.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_5_2_M.play(-1)

                # KLAVYE

                if pygame.sprite.spritecollide(oyuncu,klavye_grup, True):
                    if level == 1:
                        L_1_2_M.stop()
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.load('sesler/L1-2.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_1_3_M.play(-1)
                    if level == 2:
                        L_2_2_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L2-2.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_2_3_M.play(-1)
                        L_2_3_M.set_volume(0.5)
                    if level == 3:
                        L_3_2_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L3-2.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_3_3_M.play(-1)
                    if level == 4:
                        L_4_2_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L4-2.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_4_3_M.play(-1)
                    if level == 5:
                        L_5_2_M.stop()
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.load('sesler/L5-2.wav')
                        pygame.mixer.music.play(1) 
                        pygame.mixer.music.fadeout(2500)
                        L_5_3_M.play(-1)

               
             
             

        
        dusman_grup.draw(ekran)
        dusman_grup.update()
        diken_grup.draw(ekran)
        diken_grup.update()
        disket_grup.draw(ekran)
        disket_grup.update()
        klavye_grup.draw(ekran)
        klavye_grup.update()
        gitar_grup.draw(ekran)
        gitar_grup.update()
        bateri_grup.draw(ekran)
        bateri_grup.update()
        cikis_grup.draw(ekran)
        game_over = oyuncu.update(game_over)

        if game_over == -1:
            if bastan_basla_buton.olustur():        
                secme_fx_calma = True
                secme_fx.play()
                dunya_data = []
                dunya = reset_level(level)
                game_over = 0
                skor = 0
                Level1_calma = True
                Level2_calma = True
                Level3_calma = True
                Level4_calma = True
                Level5_calma = True
                pygame.mixer.stop()
                
        if game_over == 1 and level != 5:
            ekran.blit(tamamlama_resim,(0,0))
            if ara_ekran_calma:
                L_1_0_M.stop()
                L_2_0_M.stop()
                L_3_0_M.stop()
                L_4_0_M.stop()
                L_5_0_M.stop()
                L_1_1_M.stop()
                L_1_2_M.stop()
                L_1_3_M.stop()
                L_2_1_M.stop()
                L_2_2_M.stop()
                L_2_3_M.stop()
                L_3_1_M.stop()
                L_3_2_M.stop()
                L_3_3_M.stop()
                L_4_1_M.stop()
                L_4_2_M.stop()
                L_4_3_M.stop()
                L_5_1_M.stop()
                L_5_2_M.stop()
                L_5_3_M.stop()
                
                pygame.mixer.music.load('sesler/kazanmasesi.wav')
                pygame.mixer.music.play(0)
                ara_ekran_calma = False
                
                
            if sonraki_buton.olustur():
                secme_fx_calma = True
                secme_fx.play()
                level += 1
                if level < 6:
                    dunya_data = []
                    dunya = reset_level(level)
                    game_over = 0
                    ara_ekran_calma = True
                elif level == 5:
                    game_over = 1
            if bastan_basla2_buton.olustur():
                dunya_data = []
                dunya = reset_level(level)
                game_over = 0
                secme_fx_calma = True
                secme_fx.play()
                Level1_calma = True
                Level2_calma = True
                Level3_calma = True
                Level4_calma = True
                Level5_calma = True
            if cikis2_buton.olustur():
                calisma = False
        if game_over == 1 and level == 5:

            ekran.blit(bitiris_resim,(0,0))
            if bitis_calma:
                L_5_0_M.stop()
                L_5_1_M.stop()
                L_5_2_M.stop()
                L_5_3_M.stop()
                bitis_calma = False
                pygame.mixer.music.load('sesler/bitissesi.wav')
                pygame.mixer.music.play()


            if bastan_basla2_buton.olustur():
                dunya_data = []
                level = 1
                dunya = reset_level(level)
                game_over = 0
                skor = 0
                Level1_calma = True
                Level2_calma = True
                Level3_calma = True
                Level4_calma = True
                Level5_calma = True
                pygame.mixer.music.stop()
            if cikis2_buton.olustur():
                calisma = False
            


    

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            calisma = False

    pygame.display.update()

pygame.quit()