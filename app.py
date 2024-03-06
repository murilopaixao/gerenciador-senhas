from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import os
from hashlib import md5, sha256
import Banco
import secrets
import pyperclip
import time

app=ctk.CTk()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app.title("Gerenciador de senhas")
app.geometry("1130x710")
app.minsize(650, 450)
#app.resizable(TRUE, TRUE)

pastaApp=os.path.dirname(__file__)


def monstrarMsg(tipoMsg,titleMsg,msg):
    if(tipoMsg=="1"):
        messagebox.showinfo(title=titleMsg,message=msg)
    elif(tipoMsg=="2"):
        messagebox.showwarning(title=titleMsg,message=msg)
    elif(tipoMsg=="3"):
        messagebox.showerror(title=titleMsg,message=msg)

def semComando():
    print("")

def clearTreeview():
    tv.delete(*tv.get_children())
    
    #for child in fr_cad.winfo_children():
     #   child.destroy()

def popularTreeview():
    tv.delete(*tv.get_children())
    entradas=Banco.selectAll()
    for x in entradas:
        tv.insert("","end",values=(x["id"],x["titulo"],x["username"],x["password"],x["url"],x["tags"],x["notes"]))

def popularTreeviewGrupo():
    tv_grupo.delete(*tv_grupo.get_children())
    tv_grupo.insert("","0","Raiz", text="Murilo")
    entradas=Banco.selectAllGrupo()
    for x in entradas:
        tv_grupo.insert(x["cod_Pai"],"end",x["Cod"],text=x["Departamento"])
        #print(x)

def itemSelectTreeview(event):
    try:
        itemSelect=tv.selection()[0]
        valores=tv.item(itemSelect,"values")
        pesquisa = Banco.selectOne(valores[0])
        #print(valores[1])
        lb_caminho.configure(text=valores[1])
        lb_content_username.configure(text=valores[2])
        lb_content_password.configure(text=valores[3])
        lb_content_url.configure(text=valores[4])        
        lb_content_tags.configure(text=valores[5])
        lb_content_notes.configure(text=valores[6])
    except:
        messagebox.showinfo(title="ERRO", message="Selecione o item!!!")

def deletar():
    try:
        itemSelect=tv.selection()[0]
        valores=tv.item(itemSelect,"values")
        tv.delete(itemSelect)
        Banco.deleteOne(valores[1])

    except:
        messagebox.showinfo(title="ERRO", message="Selecione o item")


def novaEntrada():
    limparCampos()
    btn_gravar.configure(text="Gravar")
    btn_gravar.configure(command=gravarDados)
    inicio_frame.pack_forget()
    fr_cad.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)
    #exec(open(pastaApp+"/novaEntrada.py").read())

def alterarCadastro():
    et_password.configure(show="*")
    
    if lb_id.cget("text") != "":
        Banco.alterar(lb_id.cget("text"),et_title.get(),et_username.get(),criptBasic("encode",et_password.get()),et_url.get(),et_tags.get(),et_notes.get("1.0",END))
    popularTreeview()
    fr_cad.pack_forget()    
    inicio_frame.pack(fill=ctk.BOTH, expand=True)
    limparCampos()

def editarCadastro():
    limparCampos()
    try:
        itemSelect=tv.selection()[0]
        valores=tv.item(itemSelect,"values")
        lb_id.configure(text=valores[0])

        et_title.insert(END, valores[1])
        et_username.insert(END, valores[2])
        et_password.insert(END, criptBasic("decode",valores[3]))
        et_url.insert(END, valores[4])
        et_tags.insert(END, valores[5])
        et_notes.insert(END, valores[6])
        btn_gravar.configure(text="Alterar")
        btn_gravar.configure(command=alterarCadastro)
        inicio_frame.pack_forget()
        fr_cad.pack(anchor=N,fill=BOTH, expand=True, side=LEFT)

    except:
        messagebox.showinfo(title="ERRO", message="Selecione o item!!!")

def criptografarSenha(passIni):
    texto = passIni.encode("utf-8")
    #hashmd5 = md5(texto).hexdigest()
    hash256 = sha256(texto).hexdigest()
    return hash256

def criptBasic(tipo,word):
    senhaCripto = ""
    if tipo == "encode":
        for i in word:
            senhaCripto = senhaCripto + chr ( ord(i) + 5)        
    else:
        for i in word:
            senhaCripto = senhaCripto + chr ( ord(i) - 5)
    return senhaCripto

def generatePassword():
    fr_cad.pack_forget()
    fr_gerador_senhas.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

def changeWindow(windowClose,windowOpen):
    windowClose.pack_forget()
    windowOpen.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

def applyPass():
    print("")
    et_password.delete(0,END)
    et_password.insert(END, et_senhaSugerida.get())
    et_senhaSugerida.delete(0,END)
    changeWindow(fr_gerador_senhas,fr_cad)


def login(rotina):
    if rotina == "inicio":
        global passIni 
        passIni = Banco.configInicio()        
        return len(passIni)
    
    if rotina == "senhaInicial":
        if len(et_login.get()) == 0:
            messagebox.showinfo(title="Login", message="Informe a senha")
        elif et_login.get()==et_loginConfirm.get():
            passwordInicial = criptografarSenha(et_login.get())
            Banco.configSenhaInicial(passwordInicial)
            inicio_login_frame.forget()
            inicio_frame.pack(fill=ctk.BOTH, expand=True)
        else:            
            messagebox.showinfo(title="Login", message="Algo parece não estar correto")
    
    if rotina == "verificarSenha":
        if passIni["senhaInicial"] == criptografarSenha(et_login.get()):
            inicio_login_frame.forget()
            inicio_frame.pack(fill=ctk.BOTH, expand=True)
        else:
            messagebox.showinfo(title="Login", message="Algo parece não estar correto")


def popup_menu(e):
    print(e.x_root, e.y_root)
    menupop.tk_popup(x=e.x_root, y=e.y_root)


# Menu 
#Entrada - Ferramentas - Help
#print(ord("A")+5)
#print(chr(ord("A")+5))
barraDeMenus=Menu(app)
menuContatos=Menu(barraDeMenus,tearoff=0)
menuContatos.add_command(label="Nova entrada",command=novaEntrada)
menuContatos.add_command(label="Pesquisar",command=semComando)
menuContatos.add_command(label="Criar Base de dados",command=semComando)
menuContatos.add_separator()
menuContatos.add_command(label="Sair",command=app.quit)
barraDeMenus.add_cascade(label="Entrada",menu=menuContatos)

menuFerramentas=Menu(barraDeMenus,tearoff=0)
menuFerramentas.add_command(label="Pesquisar",command=semComando)
barraDeMenus.add_cascade(label="Ferramentas",menu=menuFerramentas)

menuHelp=Menu(barraDeMenus,tearoff=0)
menuHelp.add_command(label="Sobre",command=semComando)
barraDeMenus.add_cascade(label="Help",menu=menuHelp)

app.config(menu=barraDeMenus)

#Menu popup
menupop = Menu(app,tearoff=0)
menupop.add_command(label="Copiar usuário")
menupop.add_command(label="Copiar senha")
menupop.add_separator()
menupop.add_command(label="Excluir")
menupop.add_separator()
menupop.add_command(label="Novo")

############# Fim menu #############

############# Login #############

inicio_login_frame = ctk.CTkFrame(app, width=200, height=300)
inicio_login_frame.pack(pady=100)

lb_login=ctk.CTkLabel(inicio_login_frame,text="LOGIN")
lb_login.pack(pady=15)

lb_pass1=ctk.CTkLabel(inicio_login_frame,text="Informe a senha")
lb_pass1.pack(pady=15)

et_login=ctk.CTkEntry(inicio_login_frame,width=500,height=30)
et_login.pack(padx=15)

checkPass = login("inicio")

if checkPass == 0 :
    lb_pass2=ctk.CTkLabel(inicio_login_frame,text="Confirme a senha")
    lb_pass2.pack(pady=15)
    et_loginConfirm=ctk.CTkEntry(inicio_login_frame,width=500,height=30)
    et_loginConfirm.pack(padx=15)
    btn_login=ctk.CTkButton(inicio_login_frame,text="Cadastrar senha",command=lambda:login("senhaInicial"))
else:
    btn_login=ctk.CTkButton(inicio_login_frame,text="Login",command=lambda:login("verificarSenha"))

btn_login.pack(pady=15)
et_login.focus()

############# Fim Login #############


############# Main #############
inicio_frame = ctk.CTkFrame(app)
#inicio_frame.pack(fill=ctk.BOTH, expand=True)

left_frame = ctk.CTkFrame(inicio_frame)
left_frame.pack(side=LEFT, fill=ctk.BOTH, expand=True, padx=5, pady=10)


tv_grupo=ttk.Treeview(left_frame)
tv_grupo.grid(column=0,row=0,padx=5,pady=5)

popularTreeviewGrupo()

right_frame = ctk.CTkFrame(inicio_frame)
right_frame.pack(side=RIGHT, fill=ctk.BOTH, expand=True, padx=10, pady=10)

right_frame_tv = ctk.CTkFrame(right_frame,width=750,height=250)
right_frame_tv.grid(column=0,row=0, pady=5)

tv=ttk.Treeview(right_frame_tv,columns=("id","titulo","username","password","url","tags","notes"), show="headings")

tv.column("id",minwidth=0,width=50)
tv.column("titulo",minwidth=0,width=150)
tv.column("username",minwidth=0,width=100)
tv.column("password",minwidth=0,width=100)
tv.column("url",minwidth=0,width=150)
tv.column("tags",minwidth=0,width=100)
tv.column("notes",minwidth=0,width=50)

tv.heading("id",text="ID")
tv.heading("titulo",text="Titulo")
tv.heading("username",text="Username")
tv.heading("password",text="Password")
tv.heading("url",text="URL")
tv.heading("tags",text="Tags")
tv.heading("notes",text="Notes")

#tv.grid(column=1,row=0,pady=5)
tv.place(x=10,y=5)
barra = ttk.Scrollbar(right_frame_tv, orient="vertical", command=tv.yview)
barra.place(x=710,y=5,height=225)
tv.configure(yscrollcommand=barra.set)
tv.bind("<ButtonRelease-1>", itemSelectTreeview)
tv.bind("<Button-3>", popup_menu)
#barra.place(x=695,y=5,height=220)


popularTreeview()

#Selecionando item no treeview
tv.focus_set()
children = tv.get_children()
if children:
    tv.focus(children[0])
    tv.selection_set(children[0])
#itemSelect=tv.selection()[0]

right_frame_btn=ctk.CTkFrame(right_frame)
right_frame_btn.grid(column=0,row=1,padx=15,pady=5)

btn_alterar=ctk.CTkButton(right_frame_btn,text="Alterar",command=editarCadastro)
btn_alterar.grid(column=1,row=0,padx=5,pady=5)

#btn_gerador=ctk.CTkButton(right_frame_btn,text="Gerador",command=generatePassword)
#btn_gerador.grid(column=2,row=0,padx=5,pady=5)

btn_delete=ctk.CTkButton(right_frame_btn,text="Deletar",command=deletar)
btn_delete.grid(column=3,row=0,pady=5)

btn_entrada=ctk.CTkButton(right_frame_btn,text="Adicionar",command=novaEntrada)
btn_entrada.grid(column=4,row=0,padx=5,pady=5)

btn_sair=ctk.CTkButton(right_frame_btn,text="Sair",command=app.quit)
btn_sair.grid(column=5,row=0,padx=5,pady=5)

right_frame_detalhes=ctk.CTkFrame(right_frame)
right_frame_detalhes.grid(column=0,row=2,pady=5)


lb_caminho=ctk.CTkLabel(right_frame_detalhes,text="Caminho")
lb_caminho.grid(column=1,row=3,pady=5)

tabview = ctk.CTkTabview(master=right_frame_detalhes, width=740)
tabview.grid(column=1,row=4,padx=5,pady=5)


tabview.add("Detalhes")  # add tab at the end
tabview.add("Outros")  # add tab at the end
tabview.set("Detalhes")  # set currently visible tab

lb_username=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Username")
lb_password=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Password")
lb_tags=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Tags")
lb_notes=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Notes")
lb_url=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Url")
lb_expiration=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Expiration")

lb_content_username=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Username")
lb_content_password=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Password")
lb_content_tags=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Tags")
lb_content_notes=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Notes")
lb_content_url=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Url")
lb_content_expiration=ctk.CTkLabel(master=tabview.tab("Detalhes"),text="Never")

lb_username.grid(column=0,row=0,padx=10,stick='e')
lb_content_username.grid(column=1,row=0,pady=5)

lb_password.grid(column=0,row=1,padx=10,stick='e')
lb_content_password.grid(column=1,row=1,pady=5)

lb_tags.grid(column=0,row=2,padx=10,stick='e')
lb_content_tags.grid(column=1,row=2,pady=5)

lb_notes.grid(column=0,row=3,padx=10,stick='e')
lb_content_notes.grid(column=1,row=3,pady=5)

lb_url.grid(column=2,row=0,padx=75,stick='e')
lb_content_url.grid(column=3,row=0,padx=0,pady=5)

lb_expiration.grid(column=2,row=1,padx=75,stick='e')
lb_content_expiration.grid(column=3,row=1,pady=5)

lb_total_entradas=ctk.CTkLabel(right_frame,width=100,height=15,text="0 Entrada(s)")
lb_total_entradas.place(x=900,y=680)

############# Fim Main #############

############# Cadastro #############
def limparCampos():
    et_title.delete(0,END)
    et_username.delete(0,END)
    et_password.delete(0,END)
    et_url.delete(0,END)
    et_tags.delete(0,END)
    et_notes.delete(1.0,END)
    et_password.configure(show="*")
    btn_mostraSenha.configure(text="View")
    et_title.focus()

def gravarDados():
    print("------------------------------------------")
    print("Titulo: ", et_title.get() )
    print("------------------------------------------")

    if et_title.get() != "":
        Banco.insertOne(et_title.get(),et_username.get(),criptBasic("encode",et_password.get()),et_url.get(),et_tags.get(),et_notes.get("1.0",END))
    
    limparCampos()
    popularTreeview()
    fr_cad.pack_forget()    
    inicio_frame.pack(fill=ctk.BOTH, expand=True)

def cancelNovaEntrada():
    limparCampos()
    fr_cad.pack_forget()    
    inicio_frame.pack(fill=ctk.BOTH, expand=True)

def mostrarSenha():
    if et_password.cget("show")=="":
        et_password.configure(show="*")
        btn_mostraSenha.configure(text="View")
    else:
        et_password.configure(show="")
        btn_mostraSenha.configure(text="Hide")
    
fr_cad=ctk.CTkFrame(app)

lb_title=ctk.CTkLabel(fr_cad,text="Titulo:",width=80,anchor=E)
lb_username=ctk.CTkLabel(fr_cad,text="Username:",width=80,anchor=E)
lb_password=ctk.CTkLabel(fr_cad,text="Password:",width=80,anchor=E)
lb_url=ctk.CTkLabel(fr_cad,text="URL:",width=80,anchor=E)
lb_tags=ctk.CTkLabel(fr_cad,text="Tags:",width=80,anchor=E)
lb_notes=ctk.CTkLabel(fr_cad,text="Notes:",width=80,anchor=E)
lb_id=ctk.CTkLabel(fr_cad,text="ID:",anchor=E)
et_title=ctk.CTkEntry(fr_cad,width=500,height=30)
et_username=ctk.CTkEntry(fr_cad,width=500,height=30)
et_password=ctk.CTkEntry(fr_cad,show="*",width=400,height=30)
et_url=ctk.CTkEntry(fr_cad,width=500,height=30)
et_tags=ctk.CTkEntry(fr_cad,width=500,height=30)
et_notes=ctk.CTkTextbox(fr_cad,width=500,height=80)

btn_gs=ctk.CTkButton(fr_cad,text="#",width=45,height=30 ,command=generatePassword)
btn_mostraSenha=ctk.CTkButton(fr_cad,text="View",width=45,height=30,command=mostrarSenha)
btn_limpar=ctk.CTkButton(fr_cad,text="Limpar",width=80,command=limparCampos)
btn_cancel=ctk.CTkButton(fr_cad,text="Cancel",width=80,command=cancelNovaEntrada)
btn_gravar=ctk.CTkButton(fr_cad,text="Gravar",width=80,command=gravarDados)

lb_title.place(x=10,y=30)
et_title.place(x=100,y=30)

lb_username.place(x=10,y=65)
et_username.place(x=100,y=65)

lb_password.place(x=10,y=100)
et_password.place(x=100,y=100)
btn_gs.place(x=505,y=100)
btn_mostraSenha.place(x=555,y=100)

lb_url.place(x=10,y=135)
et_url.place(x=100,y=135)

lb_tags.place(x=10,y=170)
et_tags.place(x=100,y=170)

lb_notes.place(x=10,y=205)
et_notes.place(x=100,y=205)

#lb_id.place(x=10,y=300,width=150)

btn_limpar.place(x=350,y=350)
btn_cancel.place(x=435,y=350)
btn_gravar.place(x=520,y=350)

############# Fim Cadastro #############

############# Gerador de senhas #############
fr_gerador_senhas=ctk.CTkFrame(app)
#fr_gerador_senhas.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

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
    lb_qualityPassB.configure(text=qualidadeSenha)

def copiarSenha():
    senhaGerada=et_senhaSugerida.get()
    pyperclip.copy(str(senhaGerada))
    #print("Senha Gerada.:"+ str(senhaGerada))
    print(pyperclip.copy(et_senhaSugerida.get()))
    for x in range(6):
        print(x)
        time.sleep(1)
    senhaComparar=pyperclip.paste()
    if senhaGerada == str(senhaComparar):
        pyperclip.copy("Limpando area de transferencia")

def mostrarSenha2():
    if et_senhaSugerida.cget("show")=="":
        et_senhaSugerida.configure(show="*")
        btn_view.configure(text="View")
    else:
        et_senhaSugerida.configure(show="")
        btn_view.configure(text="Hide")

def sb_size_pass_function(event):
    gerarSenha()
    sc_escala.set(int(sb_size_pass.get()))

def sc_escala_function(event):
    sb_size_pass.delete(0,END)
    sb_size_pass.insert(END,int(sc_escala.get()))
    gerarSenha()

def retornoCadastro():
    fr_gerador_senhas.pack_forget()
    fr_cad.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)


############# Frame 1 #############
fr_generate1=ctk.CTkFrame(fr_gerador_senhas)
fr_generate1.pack(padx=5,pady=5)

et_senhaSugerida=ctk.CTkEntry(fr_generate1,show="*",width=250)
et_senhaSugerida.grid(column=0,row=1,padx=5,pady=5)

btn_view=ctk.CTkButton(fr_generate1,text="View",command=mostrarSenha2)
btn_view.grid(column=2,row=1,pady=5)

btn_regerar=ctk.CTkButton(fr_generate1,text="Gerar",command=gerarSenha)
btn_regerar.grid(column=3,row=1,padx=5,pady=5)

btn_copy=ctk.CTkButton(fr_generate1,text="Copy",command=copiarSenha)
btn_copy.grid(column=4,row=1,padx=5,pady=5)

############# Frame 2 #############

fr_generate2=ctk.CTkFrame(fr_gerador_senhas,width=590,height=60)
fr_generate2.pack(padx=5,pady=5)

varBarra=DoubleVar()
varBarra.set(0.4)

pb_qualityPass = ctk.CTkProgressBar(fr_generate2, orientation="horizontal",variable=varBarra)
pb_qualityPass.grid(column=0,row=2,padx=10,pady=15)

lb_qualityPass=ctk.CTkLabel(fr_generate2,text="Password Quality: ")
lb_qualityPass.grid(column=0,row=3,pady=5)

lb_qualityPassB=ctk.CTkLabel(fr_generate2,text="xxx")
lb_qualityPassB.grid(column=1,row=3,padx=10,pady=5)

############# Frame 3 #############

fr_generate3=ctk.CTkFrame(fr_gerador_senhas,width=590,height=220)
fr_generate3.pack(padx=5,pady=5)

nb_pass = ctk.CTkTabview(master=fr_generate3, width=580, height=210)
nb_pass.place(x=5,y=5)

nb_pass.add("Password")  # add tab at the end
#tabview.set("Password")

fr_generate3_a=ctk.CTkFrame(master=nb_pass.tab("Password"))
fr_generate3_a.place(x=5,y=35)

lb_length=ctk.CTkLabel(fr_generate3_a,text="Tamanho:")
lb_length.grid(column=0,row=0)

sc_escala = ctk.CTkSlider(fr_generate3_a, from_=0, to=30, command=sc_escala_function)
sc_escala.set(6)
sc_escala.grid(column=1,row=0,pady=1)

sb_size_pass=Spinbox(fr_generate3_a,from_=1, to=30)
sb_size_pass.delete(0,END)
sb_size_pass.insert(END,6)
sb_size_pass.grid(column=2,row=0,pady=1)

sb_size_pass.bind('<Button-1>', sb_size_pass_function)


############# Frame 4 #############

fr_generate4=ctk.CTkFrame(fr_gerador_senhas,width=590,height=40)
fr_generate4.pack(padx=5,pady=5)

btn_generate_close=ctk.CTkButton(fr_generate4,text="Cancel",command=retornoCadastro)
btn_generate_close.grid(column=0,row=0,padx=5,pady=5)

btn_apply_password=ctk.CTkButton(fr_generate4,text="Apply",command=applyPass)
btn_apply_password.grid(column=1,row=0,padx=5,pady=5)

############# Fim Gerador de senhas #############

app.mainloop()