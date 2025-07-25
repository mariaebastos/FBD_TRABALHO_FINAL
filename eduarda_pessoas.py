import panel as pn
import param
from datetime import date, datetime
from backend.crud_operations import (
    get_pacientes, create_paciente, delete_paciente,
    get_aplicacoes, create_aplicacao, delete_aplicacao,
    get_vacinas, get_unidades_saude # Funções auxiliares para dropdowns
)
from backend.database_config import get_db

pn.extension('tabulator', 'notifications')

class GestaoPacientesAplicacoes(pn.viewable.Viewer):
    # --- Parâmetros de Filtragem de Pacientes ---
    filtro_paciente_nome = param.String(default="", placeholder="Filtrar por nome do paciente...")
    filtro_paciente_cpf = param.String(default="", placeholder="Filtrar por CPF...")

    # --- Parâmetros para Inclusão de Paciente ---
    novo_paciente_nome = param.String(default="", placeholder="Nome do Paciente")
    novo_paciente_data_nascimento = param.Date(default=date(2000, 1, 1))
    novo_paciente_cpf = param.String(default="", placeholder="CPF (Ex: 12345678900)")
    criar_paciente_btn = pn.widgets.Button(name="Adicionar Paciente", button_type="primary")
    remover_paciente_id = param.Integer(default=0, doc="ID do Paciente para remover")
    remover_paciente_btn = pn.widgets.Button(name="Remover Paciente", button_type="danger")

    # --- Parâmetros de Filtragem de Aplicações ---
    filtro_aplicacao_paciente_nome = param.String(default="", placeholder="Filtrar por paciente...")
    filtro_aplicacao_vacina_nome = param.String(default="", placeholder="Filtrar por vacina...")
    filtro_aplicacao_unidade_nome = param.String(default="", placeholder="Filtrar por unidade...")
    filtro_aplicacao_data = param.Date(default=None, doc="Filtrar por data específica...")

    # --- Parâmetros para Inclusão de Aplicação ---
    nova_aplicacao_paciente_select = param.Selector(objects=[])
    nova_aplicacao_vacina_select = param.Selector(objects=[])
    nova_aplicacao_unidade_select = param.Selector(objects=[])
    nova_aplicacao_data = param.Date(default=date.today())
    criar_aplicacao_btn = pn.widgets.Button(name="Registrar Aplicação", button_type="primary")
    remover_aplicacao_id = param.Integer(default=0, doc="ID da Aplicação para remover")
    remover_aplicacao_btn = pn.widgets.Button(name="Remover Aplicação", button_type="danger")

    def __init__(self, **params):
        super().__init__(**params)
        self._update_aplicacao_selectors() # Preenche seletores ao iniciar
        self.criar_paciente_btn.on_click(self._on_criar_paciente)
        self.remover_paciente_btn.on_click(self._on_remover_paciente)
        self.criar_aplicacao_btn.on_click(self._on_criar_aplicacao)
        self.remover_aplicacao_btn.on_click(self._on_remover_aplicacao)


    def _update_aplicacao_selectors(self):
        db = next(get_db())
        pacientes = get_pacientes(db)
        vacinas = get_vacinas(db)
        unidades = get_unidades_saude(db)
        db.close()

        # Mapeia nomes/CPFs para IDs para os Selectors
        self._pacientes_map = {f"{p.nome} ({p.cpf})": p.id for p in pacientes}
        self.param.nova_aplicacao_paciente_select.objects = list(self._pacientes_map.keys())
        if self._pacientes_map: self.nova_aplicacao_paciente_select = list(self._pacientes_map.keys())[0]

        self._vacinas_map = {v.nome: v.id for v in vacinas}
        self.param.nova_aplicacao_vacina_select.objects = list(self._vacinas_map.keys())
        if self._vacinas_map: self.nova_aplicacao_vacina_select = list(self._vacinas_map.keys())[0]

        self._unidades_map = {u.nome: u.id for u in unidades}
        self.param.nova_aplicacao_unidade_select.objects = list(self._unidades_map.keys())
        if self._unidades_map: self.nova_aplicacao_unidade_select = list(self._unidades_map.keys())[0]

    # --- Métodos de Consulta ---
    @param.depends('filtro_paciente_nome', 'filtro_paciente_cpf', watch=True)
    def _get_pacientes_data(self):
        db = next(get_db())
        pacientes = get_pacientes(db, nome=self.filtro_paciente_nome, cpf=self.filtro_paciente_cpf)
        db.close()
        data = [{'ID': p.id, 'Nome': p.nome, 'Data Nascimento': p.data_nascimento, 'CPF': p.cpf} for p in pacientes]
        return pn.widgets.Tabulator(data, show_index=False, layout='fit_columns', sizing_mode='stretch_width')

    @param.depends('filtro_aplicacao_paciente_nome', 'filtro_aplicacao_vacina_nome', 'filtro_aplicacao_unidade_nome', 'filtro_aplicacao_data', watch=True)
    def _get_aplicacoes_data(self):
        db = next(get_db())
        aplicacoes = get_aplicacoes(db,
                                    paciente_nome=self.filtro_aplicacao_paciente_nome,
                                    vacina_nome=self.filtro_aplicacao_vacina_nome,
                                    unidade_nome=self.filtro_aplicacao_unidade_nome,
                                    data_aplicacao=self.filtro_aplicacao_data)
        db.close()
        data = []
        for a in aplicacoes:
            data.append({
                'ID Aplicação': a.id,
                'Paciente': a.paciente.nome,
                'Vacina': a.vacina.nome,
                'Unidade': a.unidade.nome,
                'Data Aplicação': a.data_aplicacao
            })
        return pn.widgets.Tabulator(data, show_index=False, layout='fit_columns', sizing_mode='stretch_width')

    # --- Métodos de Ação para Pacientes ---
    def _on_criar_paciente(self, event):
        if self.novo_paciente_nome and self.novo_paciente_cpf and self.novo_paciente_data_nascimento:
            db = next(get_db())
            try:
                create_paciente(db, self.novo_paciente_nome, self.novo_paciente_data_nascimento, self.novo_paciente_cpf)
                pn.state.notifications.success("Paciente adicionado com sucesso!")
                self.param.trigger('filtro_paciente_nome') # Atualiza a tabela
                self._update_aplicacao_selectors() # Atualiza seletor de pacientes para aplicação
            except Exception as e:
                pn.state.notifications.error(f"Erro ao adicionar paciente: {e}")
            finally:
                db.close()
            self.novo_paciente_nome = ""
            self.novo_paciente_cpf = ""
            self.novo_paciente_data_nascimento = date(2000,1,1)
        else:
            pn.state.notifications.warning("Nome, CPF e Data de Nascimento são obrigatórios.")

    def _on_remover_paciente(self, event):
        if self.remover_paciente_id > 0:
            db = next(get_db())
            try:
                paciente_removido = delete_paciente(db, self.remover_paciente_id)
                if paciente_removido:
                    pn.state.notifications.success(f"Paciente '{paciente_removido.nome}' removido!")
                    self.param.trigger('filtro_paciente_nome')
                    self._update_aplicacao_selectors()
                else:
                    pn.state.notifications.warning("Paciente não encontrado.")
            except Exception as e:
                pn.state.notifications.error(f"Erro ao remover paciente: {e}. Verifique dependências (aplicações).")
            finally:
                db.close()
            self.remover_paciente_id = 0
        else:
            pn.state.notifications.warning("Forneça um ID de paciente válido.")

    # --- Métodos de Ação para Aplicações ---
    def _on_criar_aplicacao(self, event):
        if self.nova_aplicacao_paciente_select and self.nova_aplicacao_vacina_select and self.nova_aplicacao_unidade_select and self.nova_aplicacao_data:
            paciente_id = self._pacientes_map.get(self.nova_aplicacao_paciente_select)
            vacina_id = self._vacinas_map.get(self.nova_aplicacao_vacina_select)
            unidade_id = self._unidades_map.get(self.nova_aplicacao_unidade_select)

            if not all([paciente_id, vacina_id, unidade_id]):
                pn.state.notifications.error("Erro ao resolver IDs de seleção. Tente novamente.")
                return

            db = next(get_db())
            try:
                create_aplicacao(db, paciente_id, vacina_id, unidade_id, self.nova_aplicacao_data)
                pn.state.notifications.success("Aplicação registrada com sucesso!")
                self.param.trigger('filtro_aplicacao_paciente_nome') # Atualiza a tabela de aplicações
            except Exception as e:
                pn.state.notifications.error(f"Erro ao registrar aplicação: {e}")
            finally:
                db.close()
            # Resetar campos ou manter seleção atual
            self.nova_aplicacao_data = date.today()
        else:
            pn.state.notifications.warning("Preencha todos os campos para registrar a aplicação.")

    def _on_remover_aplicacao(self, event):
        if self.remover_aplicacao_id > 0:
            db = next(get_db())
            try:
                aplicacao_removida = delete_aplicacao(db, self.remover_aplicacao_id)
                if aplicacao_removida:
                    pn.state.notifications.success(f"Aplicação ID {self.remover_aplicacao_id} removida!")
                    self.param.trigger('filtro_aplicacao_paciente_nome')
                else:
                    pn.state.notifications.warning("Aplicação não encontrada.")
            except Exception as e:
                pn.state.notifications.error(f"Erro ao remover aplicação: {e}")
            finally:
                db.close()
            self.remover_aplicacao_id = 0
        else:
            pn.state.notifications.warning("Forneça um ID de aplicação válido.")

    # --- Layout da Tela ---
    def __panel__(self):
        pacientes_pane = pn.Column(
            pn.pane.Markdown("## Gestão de Pacientes", styles={'font-weight': 'bold'}),
            pn.Row(
                pn.widgets.TextInput.from_param(self.param.filtro_paciente_nome, name="Filtrar Nome"),
                pn.widgets.TextInput.from_param(self.param.filtro_paciente_cpf, name="Filtrar CPF")
            ),
            self._get_pacientes_data,
            pn.pane.Markdown("### Adicionar Novo Paciente"),
            pn.Column(
                pn.Row(pn.widgets.TextInput.from_param(self.param.novo_paciente_nome), pn.widgets.TextInput.from_param(self.param.novo_paciente_cpf)),
                pn.widgets.DatePicker.from_param(self.param.novo_paciente_data_nascimento),
                self.criar_paciente_btn
            ),
            pn.pane.Markdown("### Remover Paciente (por ID)"),
            pn.Row(
                pn.widgets.IntInput.from_param(self.param.remover_paciente_id, name="ID Paciente"),
                self.remover_paciente_btn
            ),
            sizing_mode='stretch_width'
        )

        aplicacoes_pane = pn.Column(
            pn.pane.Markdown("## Gestão de Aplicações de Vacina", styles={'font-weight': 'bold'}),
            pn.Row(
                pn.widgets.TextInput.from_param(self.param.filtro_aplicacao_paciente_nome, name="Filtrar Paciente"),
                pn.widgets.TextInput.from_param(self.param.filtro_aplicacao_vacina_nome, name="Filtrar Vacina"),
                pn.widgets.TextInput.from_param(self.param.filtro_aplicacao_unidade_nome, name="Filtrar Unidade"),
                pn.widgets.DatePicker.from_param(self.param.filtro_aplicacao_data, name="Filtrar Data")
            ),
            self._get_aplicacoes_data,
            pn.pane.Markdown("### Registrar Nova Aplicação"),
            pn.Column(
                pn.Row(
                    pn.widgets.Select.from_param(self.param.nova_aplicacao_paciente_select, name="Paciente"),
                    pn.widgets.Select.from_param(self.param.nova_aplicacao_vacina_select, name="Vacina")
                ),
                pn.Row(
                    pn.widgets.Select.from_param(self.param.nova_aplicacao_unidade_select, name="Unidade de Saúde"),
                    pn.widgets.DatePicker.from_param(self.param.nova_aplicacao_data, name="Data da Aplicação")
                ),
                self.criar_aplicacao_btn
            ),
            pn.pane.Markdown("### Remover Aplicação (por ID)"),
            pn.Row(
                pn.widgets.IntInput.from_param(self.param.remover_aplicacao_id, name="ID Aplicação"),
                self.remover_aplicacao_btn
            ),
            sizing_mode='stretch_width'
        )
        return pn.Column(pacientes_pane, aplicacoes_pane, sizing_mode='stretch_width')