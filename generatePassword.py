from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import secrets
import pyperclip
import time

app=Tk()
app.title("Gerador de senhas")
app.geometry("600x400")

############# Funções #############

def gerarSenha():    
    size=int(sb_size_pass.get())
    #size=int(sc_escala.get())
    senhaAleatoria = secrets.token_urlsafe(size)
    et_senhaSugerida.delete(0,END)
    senhaAleatoriaB = senhaAleatoria[0:size]
    #print("Tamanho da senha:"+ str(len(senhaAleatoriaB)))
    et_senhaSugerida.insert(END, senhaAleatoriaB)
    if size <= 5:
        qualidadeSenha="Péssima"
    elif size >=6 and size <=10 :
        qualidadeSenha="Ruim"
    elif size >=11 and size <=15 :
        qualidadeSenha="Boa"
    else:
        qualidadeSenha="Ótima"


    lb_qualityPassB["text"]=qualidadeSenha

def copiarSenha():
    senhaGerada=et_senhaSugerida.get()
    pyperclip.copy(str(senhaGerada))
    #print("Senha Gerada.:"+ str(senhaGerada))
    print(pyperclip.copy(et_senhaSugerida.get()))
    for x in range(6):
        print(x)
        time.sleep(2)
    senhaComparar=pyperclip.paste()
    if senhaGerada == str(senhaComparar):
        pyperclip.copy("Limpando area de transferencia")

def mostrarSenha():
    if et_senhaSugerida["show"]=="":
        et_senhaSugerida["show"]="*"
        btn_view["text"]="View"
    else:
        et_senhaSugerida["show"]=""
        btn_view["text"]="Hide"

def sb_size_pass_function(event):
    gerarSenha()
    sc_escala.set(sb_size_pass.get())

def sc_escala_function(event):
    sb_size_pass.delete(0,END)
    sb_size_pass.insert(END,sc_escala.get())
    gerarSenha()


############# Frame 1 #############
fr_generate1=Frame(app)
fr_generate1.place(x=5,y=5,width=590,height=50)

et_senhaSugerida=Entry(fr_generate1,show="*",width=50)
et_senhaSugerida.grid(column=0,row=1,pady=5)

btn_view=Button(fr_generate1,text="View",command=mostrarSenha)
btn_view.grid(column=2,row=1,pady=5)

btn_regerar=Button(fr_generate1,text="Gerar",command=gerarSenha)
btn_regerar.grid(column=3,row=1,pady=5)

btn_copy=Button(fr_generate1,text="Copy",command=copiarSenha)
btn_copy.grid(column=4,row=1,pady=5)

############# Frame 2 #############

fr_generate2=Frame(app)
fr_generate2.place(x=5,y=60,width=590,height=60)

varBarra=DoubleVar()
varBarra.set(40)

pb_qualityPass=ttk.Progressbar(fr_generate2,variable=varBarra,maximum=100)
pb_qualityPass.grid(column=0,row=2,pady=5)

lb_qualityPass=Label(fr_generate2,text="Password Quality: ")
lb_qualityPass.grid(column=0,row=3,pady=5)

lb_qualityPassB=Label(fr_generate2,text="xxx")
lb_qualityPassB.grid(column=1,row=3,pady=5)

############# Frame 3 #############

fr_generate3=Frame(app)
fr_generate3.place(x=5,y=115,width=590,height=220)

nb_pass=ttk.Notebook(fr_generate3)
nb_pass.place(x=0,y=0,width=590,height=220)
#nb_pass.place(x=50,y=50,width=200,height=250)

tb1_pass=Frame(nb_pass)

nb_pass.add(tb1_pass,text="Password")

fr_generate3_a=Frame(fr_generate3)
fr_generate3_a.place(x=5,y=35)

lb_length=Label(fr_generate3_a,text="Tamanho:")
lb_length.grid(column=0,row=0)

sc_escala=Scale(fr_generate3_a,from_=1,to=30,orient=HORIZONTAL)
sc_escala.set(6)
sc_escala.grid(column=1,row=0,pady=1)
sc_escala.bind('<B1-Motion>', sc_escala_function)

sb_size_pass=Spinbox(fr_generate3_a,from_=1, to=30)
sb_size_pass.delete(0,END)
sb_size_pass.insert(END,6)
sb_size_pass.grid(column=2,row=0,pady=1)

sb_size_pass.bind('<Button-1>', sb_size_pass_function)


############# Frame 4 #############

fr_generate4=Frame(app,relief="solid")
fr_generate4.place(x=5,y=350,width=590,height=40)

btn_generate_close=Button(fr_generate4,text="Sair",command=app.quit)
btn_generate_close.grid(column=0,row=0,pady=5)

btn_apply_password=Button(fr_generate4,text="Aplicar senha",command=app.quit)
btn_apply_password.grid(column=1,row=0,pady=5)

app.mainloop()