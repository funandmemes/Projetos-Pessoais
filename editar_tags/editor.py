#!/usr/bin/env python3
'''
Editor de tags de arquivos mp3 ou m4a

Para abrir:
python3

Bibliotecas externas necessárias:
> pillow
> mutagen
> eyed3

Para instalar as bibliotecas:
> pip install pillow
> pip install mutagen
> pip install eyed3

Ou instale todas de uma vez:
> pip install pillow mutagen eyed3
'''
__author__='funandmemes'
__version__='0.1.1'

import os
from tkinter import *
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import APIC, ID3, ID3NoHeaderError, PictureType
from mutagen.oggvorbis import OggVorbis
from mutagen.oggopus import OggOpus
import tempfile
from base64 import b64encode
import eyed3
from tinytag import TinyTag
import base64
from mutagen.flac import Picture, FLAC

tags = {
    'titulo_m4a': '\xa9nam',
    'artista_m4a': '\xa9ART',
    'album_m4a': '\xa9alb',
    'titulo_mp3': 'title',
    'artista_mp3': 'artist',
    'album_mp3': 'album',
    'titulo_ogg': 'title',
    'artista_ogg': 'artist',
    'album_ogg': 'album',
    'titulo_flac': 'title',
    'artista_flac': 'artist',
    'album_flac': 'album',
}
class main:
    def __init__(self, master):
        self.master = master
        Label(self.master, text='').grid(row=0)
        self.but = Button(self.master, text='SELECIONAR MÚSICA',
        command=self.abrir_mus).grid(row=1, columnspan=2)
        self.musica_info = Label(self.master, text='', foreground='red')
        self.musica_info.grid(row=2, columnspan=2)
        self.titulo = Label(self.master, text='Faixa: ').grid(row=3, column=0,
        sticky='e')
        self.titulo_dig = Entry(self.master)
        self.titulo_dig.grid(row=3, column=1)
        self.artista = Label(self.master, text='Artista: ').grid(row=4,
        column=0, sticky='e')
        self.artista_dig = Entry(self.master)
        self.artista_dig.grid(row=4, column=1)
        self.album = Label(self.master, text='Album: ').grid(row=5, column=0,
        sticky='e')
        self.album_dig = Entry(self.master)
        self.album_dig.grid(row=5, column=1)
        Label(self.master, text='').grid(row=6)
        self.capa = Button(self.master, text='SELECIONAR CAPA',
        command=self.abrir_capa)
        self.capa.grid(row=7, columnspan=2)
        self.capa_info = Label(self.master, text='', foreground='red')
        self.capa_info.grid(row=8, columnspan=2)
        self.salvar_but = Button(self.master, text='SALVAR',
        command=self.salvar_tags)
        self.salvar_but.grid(row=9, columnspan=2)
        Label(self.master, text='').grid(row=10)
        
    def abrir_mus(self):
        self.musica = askopenfile(mode='r', filetypes=[('Músicas',
        '*.m4a *.mp3 *.opus *.ogg *.flac')])
        if self.musica is not None:     
            print('Música carregada')
            nome_musica = os.path.basename(self.musica.name)
            if len(nome_musica) > 30:
                nome_musica = nome_musica[:30] + '...'
            self.musica_info.config(text=f"'{nome_musica}'")

    def iniciar_corte(self, event):
        if self.corte_atual:
            self.canvas.delete(self.corte_atual)
        inicio_x = self.canvas.canvasx(event.x)
        inicio_y = self.canvas.canvasy(event.y)
        self.corte_atual = self.canvas.create_rectangle(inicio_x, inicio_y, inicio_x, inicio_y, outline='red')
        
    def corte(self, event):
        atual_x = self.canvas.canvasx(event.x)
        atual_y = self.canvas.canvasy(event.y)
        inicio_x, inicio_y, _, _ = self.canvas.coords(self.corte_atual)
        lado = min(abs(atual_x - inicio_x), abs(atual_y - inicio_y))
        atual_x = inicio_x + lado
        atual_y = inicio_y + lado
        self.canvas.coords(self.corte_atual, inicio_x, inicio_y,
        atual_x, atual_y)

    def corte_pronto(self, event):
        quadrado = self.canvas.coords(self.corte_atual)
        quadrado = [int(coord) for coord in quadrado]
        self.corte_imagem = self.capa_foto.crop(quadrado)
        self.pronto_salvar = True
        print('Corte pronto para salvar')

    def salvar_corte(self):
        self.corte_imagem.thumbnail((300,300))
        with tempfile.NamedTemporaryFile(suffix='.png', delete = True) as temp:
            self.corte_imagem.save(temp.name)
            print('Imagem cortada')
            with open(temp.name, 'rb') as self.capa_arquivo:
                self.capa_final = self.capa_arquivo.read()
        self.segunda.destroy()
        nome_capa = os.path.basename(self.capa.name)
        if len(nome_capa) > 30:
            nome_capa = nome_capa[:30] + '...'
        self.capa_info.config(text=f"'{nome_capa}'")

    def abrir_capa(self):
        self.capa = askopenfile(mode='r', filetypes=[('Imagens', '*.jpg *.png')])
        self.segunda = Toplevel(root)
        self.segunda.title('Recortar a capa')
        self.canvas = Canvas(self.segunda, width=400, height=400)
        self.canvas.pack()
        self.capa_foto = Image.open(self.capa.name)
        self.capa_foto.thumbnail((400, 400))  
        self.imagem = ImageTk.PhotoImage(self.capa_foto)
        self.canvas.create_image(0, 0, anchor=NW, image=self.imagem)
        self.corte_atual = None
        self.canvas.bind('<Button-1>', self.iniciar_corte)
        self.canvas.bind('<B1-Motion>', self.corte)
        self.canvas.bind('<ButtonRelease-1>', self.corte_pronto)
        self.salvar = Button(self.segunda, text='SALVAR CORTE',
        command=self.salvar_corte)
        self.salvar.pack()
        
        if self.capa is not None:
            return

    def salvar_tags(self):
        formato = self.musica.name.split('.')[-1]
        titulo = self.titulo_dig.get()
        titulo_tag = 'titulo_' + formato
        artista = self.artista_dig.get()
        artista_tag = 'artista_' + formato
        album = self.album_dig.get()
        album_tag = 'album_' + formato
        if formato == 'm4a':
            audio = MP4(self.musica.name)
            audio.delete()
            try:
                capa_audio = [MP4Cover(self.capa_final)]
                audio['covr'] = capa_audio
            except Exception as e:
                print(f'[ERROR] Unable to change cover: {e}')
        if formato == 'mp3':
            mp3 = MP3(self.musica.name, ID3=ID3)
            mp3.delete()
            mp3.save()
            audio = eyed3.load(self.musica.name)
            audio.initTag()
            audio.tag.save()
            audio = EasyID3(self.musica.name)
            mp3 = MP3(self.musica.name, ID3=ID3)
            try:
                mp3.tags.add(APIC(encoding=3, mime='image/jpeg', type=3,
                desc='Cover', data=self.capa_final))
                mp3.save()
                audio = EasyID3(self.musica.name)
            except Exception as e:
                print(f'[ERROR] Unable to change cover: {e}')
        if formato == 'ogg':
            audio = OggVorbis(self.musica.name)
            audio.delete()
            try:
                picture = Picture()
                picture.data = self.capa_final
                picture.type = 17
                picture.mime = u'image/jpeg'
                picture.width = 300
                picture.height = 300
                picture.depth = 24
                
                picture_data = picture.write()
                encoded_data = base64.b64encode(picture_data)
                vcomment_value = encoded_data.decode('ascii')
                audio["metadata_block_picture"] = [vcomment_value]
                audio.save()
            except Exception as e:
                print(f'[ERROR] Unable to change cover: {e}')
        if formato == 'flac':
            audio = FLAC(self.musica.name)
            audio.delete()
            try:
                picture = Picture()
                picture.data = self.capa_final
                picture.type = 17
                picture.mime = u'image/jpeg'
                picture.width = 300
                picture.height = 300
                picture.depth = 2

                picture_data = picture.write()
                encoded_data = base64.b64encode(picture_data)
                vcomment_value = encoded_data.decode('ascii')
                audio["metadata_block_picture"] = [vcomment_value]
                audio.save()
            except Exception as e:
                print(f'[ERROR] Unable to change cover: {e}')
        if len(titulo) > 0:
            audio[tags[titulo_tag]] = titulo
        if len(artista) > 0:
            audio[tags[artista_tag]] = artista
        if len(album) > 0:
            audio[tags[album_tag]] = album
        audio.save()
        print('sussesso')
root = Tk()
root.title('Editor de tags')
app = main(root)
root.mainloop()
