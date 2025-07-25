import panel as pn
from backend.init_db import initialize_database
from frontend.melk_vacinas import GestaoVacinasFabricantes # Importa a classe da tela de Melk
from frontend.eduarda_pacientes import GestaoPacientesAplicacoes # Importa a classe da tela de Eduarda

pn.extension('tabulator', 'notifications') # Habilita extensões do Panel para tabelas e notificações

# --- PASSO CRÍTICO: Inicialização do Banco de Dados ---
# Rode esta função SOMENTE NA PRIMEIRA VEZ para criar as tabelas e popular o banco.
# Se as tabelas já existem e estão populadas, MANTENHA COMENTADO para evitar duplicatas ou erros.
# initialize_database()
# print("Banco de dados inicializado (tabelas e povoamento).") # Esta linha será exibida no console Python.


# Crie instâncias das suas telas
melk_app = GestaoVacinasFabricantes()
eduarda_app = GestaoPacientesAplicacoes()

# Crie um Dashboard com abas para cada tela
dashboard = pn.Tabs(
    ("Gestão de Vacinas e Fabricantes (Melk)", melk_app),
    ("Gestão de Pacientes e Aplicações (Eduarda)", eduarda_app)
)

# Servir a aplicação
dashboard.servable(title="Sistema de Gestão de Campanhas de Vacinação")