from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from hashlib import md5, sha256
import Banco

#Cores
bg="#3B3F40"
fg="#B2BEBF"
bg_et="#252626"

app=Tk()
app.title("Gerenciador de senhas")
app.geometry("1130x710")
app.configure(background=bg)

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

def itemSelectTreeview():
    try:
        itemSelect=tv.selection()[0]
        valores=tv.item(itemSelect,"values")
        pesquisa = Banco.selectOne(valores[0])
        #print(pesquisa[titulo])
        lb_caminho["text"]=valores[1]
        lb_content_username["text"]=valores[2]
        lb_content_password["text"]=valores[3]
        lb_content_url["text"]=valores[4]        
        lb_content_tags["text"]=valores[5]
        lb_content_notes["text"]=valores[6]
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
    btn_gravar["text"]="Gravar"
    btn_gravar["command"]=gravarDados
    fr_main.pack_forget()
    fr_cad.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)
    #exec(open(pastaApp+"/novaEntrada.py").read())

def alterarCadastro():
    if lb_id["text"] != "":
        Banco.alterar(lb_id["text"],et_title.get(),et_username.get(),criptBasic("encode",et_password.get()),et_url.get(),et_tags.get(),et_notes.get("1.0",END))
    popularTreeview()
    fr_cad.pack_forget()    
    fr_main.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)
    limparCampos()

def editarCadastro():
    limparCampos()
    try:
        itemSelect=tv.selection()[0]
        valores=tv.item(itemSelect,"values")
        lb_id["text"]=valores[0]

        et_title.insert(END, valores[1])
        et_username.insert(END, valores[2])
        et_password.insert(END, criptBasic("decode",valores[3]))
        et_url.insert(END, valores[4])
        et_tags.insert(END, valores[5])
        et_notes.insert(END, valores[6])
        btn_gravar["text"]="Alterar"
        btn_gravar["command"]=alterarCadastro
        fr_main.pack_forget()
        fr_cad.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

    except:
        messagebox.showinfo(title="ERRO", message="Selecione o item!!!")

def criptografarSenha():
    texto = senha.get().encode("utf-8")
    hashmd5 = md5(texto).hexdigest()
    hash256 = sha256(texto).digest()
    print(hash256)

def desCriptografarSenha():
    texto = senha.get().decode("utf-8")
    hash = md5(texto).hexdigest()
    print(texto)

def criptBasic(tipo,word):
    senhaCripto = ""
    if tipo == "encode":
        for i in word:
            senhaCripto = senhaCripto + chr ( ord(i) + 5)        
    else:
        for i in word:
            senhaCripto = senhaCripto + chr ( ord(i) - 5)
    return senhaCripto

# Menu 
#Entrada - Ferramentas - Help
print(ord("A")+5)
print(chr(ord("A")+5))
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

############# Fim menu #############

############# Main #############
fr_main=Frame(app,borderwidth=1,relief="solid", background=bg)
fr_main.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

lb_sideLeft=Label(fr_main,text="sideLeft")
lb_sideLeft.grid(column=0,row=0,padx=100,pady=5)

lb_testeCripto=Label(fr_main,text="Criptografar senha")
lb_testeCripto.grid(column=0,row=1,padx=100,pady=5)

senha=Entry(fr_main,background=bg_et,foreground=fg)
senha.grid(column=0,row=2,padx=5,pady=5)

btn_cripto=Button(fr_main,text="Criptografar",command=criptografarSenha)
btn_cripto.grid(column=0,row=3,padx=5,pady=5)

btn_desCripto=Button(fr_main,text="DesCriptografar",command=desCriptografarSenha)
btn_desCripto.grid(column=0,row=4,padx=5,pady=5)

tv=ttk.Treeview(fr_main,columns=("id","titulo","username","password","url","tags","notes"), show="headings")

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
tv.heading("notes",text="notes")

tv.grid(column=1,row=0,pady=5)

popularTreeview()

fr_btn=Frame(fr_main,borderwidth=1,relief="solid")
fr_btn.grid(column=1,row=2,pady=5)

btn_tv_item_select=Button(fr_btn,text="Selecionar",command=itemSelectTreeview)
btn_tv_item_select.grid(column=0,row=0,padx=5,pady=5)

btn_alterar=Button(fr_btn,text="Alterar",command=editarCadastro)
btn_alterar.grid(column=1,row=0,padx=5,pady=5)

btn_tv=Button(fr_btn,text="Limpar",command=clearTreeview)
btn_tv.grid(column=2,row=0,pady=5)

btn_popular_tv=Button(fr_btn,text="Popular",command=popularTreeview)
btn_popular_tv.grid(column=3,row=0,padx=5,pady=5)

btn_delete=Button(fr_btn,text="Deletar",command=deletar)
btn_delete.grid(column=4,row=0,pady=5)

btn_entrada=Button(fr_btn,text="Adicionar",command=novaEntrada)
btn_entrada.grid(column=5,row=0,padx=5,pady=5)

btn_sair=Button(fr_btn,text="Sair",command=app.quit)
btn_sair.grid(column=6,row=0,padx=5,pady=5)

lb_caminho=Label(fr_main,text="Caminho")
lb_caminho.grid(column=1,row=3,pady=5)

nb=ttk.Notebook(fr_main)
nb.grid(column=1,row=4,pady=5)
#nb.place(x=300,y=420,width=600,height=250)


tb1=Frame(nb)
tb2=Frame(nb)

nb.add(tb1,text="Detalhes")
nb.add(tb2,text="Outros")

lb_username=Label(tb1,text="Username")
lb_password=Label(tb1,text="Password")
lb_tags=Label(tb1,text="Tags")
lb_notes=Label(tb1,text="Notes")
lb_url=Label(tb1,text="Url")
lb_expiration=Label(tb1,text="Expiration")

lb_content_username=Label(tb1,text="Username")
lb_content_password=Label(tb1,text="Password")
lb_content_tags=Label(tb1,text="Tags")
lb_content_notes=Label(tb1,text="Notes")
lb_content_url=Label(tb1,text="Url")
lb_content_expiration=Label(tb1,text="Never")

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

lb_total_entradas=Label(fr_main,text="0 Entrada(s)")
lb_total_entradas.place(x=900,y=680,width=100,height=15)

#tv.bind("<Button-1>", itemSelectTreeview2)
############# Fim Main #############

############# Cadastro #############
def limparCampos():
    et_title.delete(0,END)
    et_username.delete(0,END)
    et_password.delete(0,END)
    et_url.delete(0,END)
    et_tags.delete(0,END)
    et_notes.delete(1.0,END)
    et_password["show"]="*"
    btn_mostraSenha["text"]="View"
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
    fr_main.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

def cancelNovaEntrada():
    limparCampos()
    fr_cad.pack_forget()    
    fr_main.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

def mostrarSenha():
    if et_password["show"]=="":
        et_password["show"]="*"
        btn_mostraSenha["text"]="View"
    else:
        et_password["show"]=""
        btn_mostraSenha["text"]="Hide"
    

fr_cad=Frame(app,borderwidth=1,relief="solid", background=bg)

lb_title=Label(fr_cad,text="Titulo:",background=bg,foreground=fg,anchor=E)
lb_username=Label(fr_cad,text="Username:",background=bg,foreground=fg,anchor=E)
lb_password=Label(fr_cad,text="Password:",background=bg,foreground=fg,anchor=E)
lb_url=Label(fr_cad,text="URL:",background=bg,foreground=fg,anchor=E)
lb_tags=Label(fr_cad,text="Tags:",background=bg,foreground=fg,anchor=E)
lb_notes=Label(fr_cad,text="Notes:",background=bg,foreground=fg,anchor=E)
lb_id=Label(fr_cad,text="ID:",background=bg,foreground=fg,anchor=E)
et_title=Entry(fr_cad,background=bg_et,foreground=fg)
et_username=Entry(fr_cad,background=bg_et,foreground=fg)
et_password=Entry(fr_cad,show="*",background=bg_et,foreground=fg)
et_url=Entry(fr_cad,background=bg_et,foreground=fg)
et_tags=Entry(fr_cad,background=bg_et,foreground=fg)
et_notes=Text(fr_cad,background=bg_et,foreground=fg)

btn_mostraSenha=Button(fr_cad,text="View",command=mostrarSenha)
btn_limpar=Button(fr_cad,text="Limpar",background=bg_et,foreground=fg,command=limparCampos)
btn_cancel=Button(fr_cad,text="Cancel",background=bg_et,foreground=fg,command=cancelNovaEntrada)
btn_gravar=Button(fr_cad,text="Gravar",background=bg_et,foreground=fg,command=gravarDados)

lb_title.place(x=10,y=30,width=80)
et_title.place(x=100,y=30,width=500,height=30)

lb_username.place(x=10,y=65,width=80)
et_username.place(x=100,y=65,width=500,height=30)

lb_password.place(x=10,y=100,width=80)
et_password.place(x=100,y=100,width=450,height=30)
btn_mostraSenha.place(x=555,y=100,width=45,height=30)

lb_url.place(x=10,y=135,width=80)
et_url.place(x=100,y=135,width=500,height=30)

lb_tags.place(x=10,y=170,width=80)
et_tags.place(x=100,y=170,width=500,height=30)

lb_notes.place(x=10,y=205,width=80)
et_notes.place(x=100,y=205,width=500,height=80)

#lb_id.place(x=10,y=300,width=150)

btn_limpar.place(x=350,y=350,width=80)
btn_cancel.place(x=435,y=350,width=80)
btn_gravar.place(x=520,y=350,width=80)

############# Fim Cadastro #############

app.mainloop()