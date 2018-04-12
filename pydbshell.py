import npyscreen
import pickle

CONEXOES = None


def carregar():
	global CONEXOES 
	try:
		with open("conexoes.db", "rb+") as handle:
			CONEXOES = pickle.load(handle)
	except:
		CONEXOES = []


def salvar():
	global CONEXOES 
	try:
		with open("conexoes.db", "wb+") as handle:
			pickle.dump(CONEXOES, handle)
	except:
		print("nao tinha")


class FormConexoes(npyscreen.ActionPopup):
	def create(self):
		super(FormConexoes, self).create()
		self.name="Conexões"
		self.conexoes = self.add(npyscreen.SelectOne, max_height=3,
                                name='Department',
                                values = [item['nome'] for item in CONEXOES],
                                scroll_exit = True  # Let the user move out of the widget by pressing the down arrow instead of tab.  Try it without
                                                    # to see the difference.
                                )
	def on_ok(self):
		FormAdicionarConexao().edit()


class FormAdicionarConexao(npyscreen.ActionPopup):
	def create(self):
		super(FormAdicionarConexao, self).create()
		self.nome = self.add(npyscreen.TitleText, name="Nome")
		self.host = self.add(npyscreen.TitleText, name="Host")
		self.porta = self.add(npyscreen.TitleText, name="Porta")
		self.banco = self.add(npyscreen.TitleText, name="Banco")
		self.usuario = self.add(npyscreen.TitleText, name="Usuário")
		self.senha = self.add(npyscreen.TitlePassword, name="Senha")
		
	
	def on_ok(self):
		global CONEXOES
		CONEXOES += [
			{
				'nome':self.nome.value,
				'host':self.host.value,
				'porta':self.porta.value,
				'banco':self.banco.value,
				'usuario':self.usuario.value,
				'senha':self.senha.value,
				
			}
		]
		
		salvar()
		
		self.parentApp.setNextForm(FormConexoes)

class FormIntro(npyscreen.Form):
	def __init__(self):
		super(FormIntro, self).__init__(name="PyDbShell")


class Aplicacao(npyscreen.NPSAppManaged):
	def onStart(self):
		self.registerForm("CONEXOES", FormConexoes())
		self.registerForm("INTRO", FormIntro())
		self.registerForm("ADICIONAR", FormAdicionarConexao())

	def main(self):
		intro = FormIntro()
		intro.display()

		form = FormConexoes()
		form.edit()

if __name__ == "__main__":
	carregar()
	
	App = Aplicacao()
	App.run()
