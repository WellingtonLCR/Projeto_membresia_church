import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from werkzeug.security import generate_password_hash

from app import app


class MembresiaAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def autenticar(self):
        with self.client.session_transaction() as sess:
            sess["usuario_logado"] = "teste@igreja.org"
            sess["usuario_nome"] = "Usuario Teste"
            sess["usuario_perfil"] = "Administrador"
            sess["usuario_modo"] = "admin"
            sess["usuario_id"] = 1

    def test_rotas_publicas_renderizam(self):
        for rota in [
            "/",
            "/login",
            "/cadastro",
            "/sobre-equipe",
            "/app",
            "/app/eventos",
            "/app/cultos",
            "/app/feed",
            "/app/devocional",
            "/app/oracao",
            "/app/doacoes",
            "/app/cadastro",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 200)

    def test_assets_essenciais_sao_entregues(self):
        for rota, trecho in [
            ("/static/css/styles.css", b"admin-shell"),
            ("/static/js/script.js", b"DOMContentLoaded"),
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                conteudo = resposta.get_data()
                resposta.close()

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(trecho, conteudo)

    def test_css_fallback_preserva_responsividade_do_layout_admin(self):
        resposta = self.client.get("/static/css/styles.css")
        css = resposta.get_data(as_text=True)
        resposta.close()

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(".d-none", css)
        self.assertIn(".d-lg-flex", css)
        self.assertLess(css.index(".d-none"), css.index(".d-lg-flex"))

    def test_identidade_visual_usa_nome_correto_da_aplicacao(self):
        self.autenticar()

        resposta = self.client.get("/dashboard")
        html = resposta.get_data(as_text=True)
        resposta.close()

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Sistema de Membresia da Igreja Viva", html)
        self.assertIn("Igreja Viva", html)
        marca_antiga = "Do" + "mus Control"
        self.assertNotIn(marca_antiga, html)

    def test_codigo_principal_nao_usa_identidade_antiga(self):
        marca_antiga = "Do" + "mus"
        arquivos = [
            "README.md",
            "app.py",
            "templates/base.html",
            "templates/base_publica.html",
            "static/css/styles.css",
            "static/js/script.js",
            "material_TCC/gerar_docx_abnt.py",
        ]

        for arquivo in arquivos:
            with self.subTest(arquivo=arquivo):
                conteudo = Path(arquivo).read_text(encoding="utf-8")
                self.assertNotIn(marca_antiga, conteudo)

    def test_tema_e_filtros_tem_fallback_estavel(self):
        self.autenticar()
        resposta = self.client.get("/dashboard")
        html = resposta.get_data(as_text=True)
        resposta.close()

        script = Path("static/js/script.js").read_text(encoding="utf-8")
        css = Path("static/css/styles.css").read_text(encoding="utf-8")

        self.assertIn("data-theme-toggle", html)
        self.assertIn('data-theme-option="light"', html)
        self.assertIn('data-theme-option="dark"', html)
        self.assertIn('data-theme-option="contrast"', html)
        self.assertIn('data-theme-option="system"', html)
        self.assertIn("Igreja Viva &middot; Membresia", html)
        self.assertIn("membresia-theme", script)
        self.assertIn("TEMAS_VALIDOS", script)
        self.assertIn("prefers-color-scheme", script)
        self.assertIn("membresia-backdrop", script)
        self.assertIn("membresia-backdrop", css)
        self.assertIn("hidden.bs.modal", script)
        self.assertIn("liberarPagina", script)
        self.assertIn("form.filter-modal", script)
        self.assertIn("URLSearchParams", script)
        self.assertIn("window.location.assign", script)
        self.assertIn("show.bs.modal", script)
        self.assertIn("body.admin-shell.modal-open", css)
        self.assertIn("padding-right: 0 !important", css)
        self.assertNotIn("getOrCreateInstance(alvo)", script)
        self.assertIn(':root[data-theme="dark"] body.admin-shell', css)
        self.assertIn(':root[data-theme="contrast"] body.admin-shell', css)
        self.assertIn("body.admin-shell .admin-mobile-menu .offcanvas-footer", css)
        self.assertIn("body.admin-shell .dashboard-chart-legend", css)
        overlay_antigo = "do" + "mus-backdrop"
        self.assertNotIn(overlay_antigo, script)
        self.assertNotIn(overlay_antigo, css)

    def test_filtro_de_cultos_aplica_dia_da_semana_na_consulta(self):
        self.autenticar()
        consultas = []

        def db_select_fake(sql, params=None):
            consultas.append((sql, params or []))
            return []

        with patch("app.db_select", side_effect=db_select_fake), \
             patch("app.db_scalar", return_value=0):
            resposta = self.client.get("/eventos/listar?dia_semana=Domingo&status=Agendado")

        self.assertEqual(resposta.status_code, 200)
        sql_eventos, params_eventos = next(
            item for item in consultas if "FROM eventos e" in item[0]
        )
        self.assertIn("e.status = %s", sql_eventos)
        self.assertIn("DAYOFWEEK(e.data_inicio) = %s", sql_eventos)
        self.assertEqual(params_eventos, ["Agendado", 1])
        html = resposta.get_data(as_text=True)
        self.assertIn('name="dia_semana"', html)
        self.assertNotIn('name="recorrencia"', html)

    def test_filtro_financeiro_aplica_parametros_na_consulta(self):
        self.autenticar()
        consultas = []

        def db_select_fake(sql, params=None):
            consultas.append((sql, params or []))
            return []

        with patch("app.db_select", side_effect=db_select_fake), \
             patch("app.db_scalar", return_value=0):
            resposta = self.client.get(
                "/financeiro/listar"
                "?data_inicio=2026-06-01"
                "&data_fim=2026-06-07"
                "&tipo=Entrada"
                "&conta_id=1"
                "&categoria_id=2"
                "&status_baixa=Baixado"
                "&usuario_id=3"
            )

        self.assertEqual(resposta.status_code, 200)
        sql_financeiro, params_financeiro = next(
            item for item in consultas if "FROM lancamentos_financeiros l" in item[0]
        )
        self.assertIn("l.tipo = %s", sql_financeiro)
        self.assertIn("l.data_lancamento >= %s", sql_financeiro)
        self.assertIn("l.data_lancamento <= %s", sql_financeiro)
        self.assertIn("l.conta_id = %s", sql_financeiro)
        self.assertIn("l.categoria_id = %s", sql_financeiro)
        self.assertIn("l.criado_por_usuario_id = %s", sql_financeiro)
        self.assertIn("l.data_lancamento <= CURDATE()", sql_financeiro)
        self.assertEqual(params_financeiro, ["Entrada", "2026-06-01", "2026-06-07", "1", "2", "3"])

    def test_busca_superior_tem_comportamento_local(self):
        resposta = self.client.get("/static/js/script.js")
        script = resposta.get_data(as_text=True)
        resposta.close()

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("data-local-search", script)
        self.assertIn("local-search-hidden", script)
        self.assertIn("Nenhum resultado encontrado", script)

    def test_rotas_get_sem_parametros_nao_quebram_com_admin_logado(self):
        self.autenticar()
        rotas_ignoradas = {"static", "logout"}

        for regra in app.url_map.iter_rules():
            if regra.endpoint in rotas_ignoradas or "GET" not in regra.methods or regra.arguments:
                continue

            with self.subTest(rota=regra.rule, endpoint=regra.endpoint):
                resposta = self.client.get(regra.rule, follow_redirects=False)

                self.assertLess(resposta.status_code, 500)

    def test_app_usuario_home_exibe_conteudo_alimentado_pelo_admin(self):
        evento = {
            "id": 10,
            "nome": "Culto Jovem",
            "data_inicio": datetime(2026, 6, 12, 20, 0),
            "local": "Templo principal",
            "banner_path": None,
        }
        aviso = {
            "titulo": "Aviso Admin",
            "categoria": "Comunicado",
            "conteudo": "Conteudo publicado pelo painel administrativo.",
        }
        devocional = {
            "titulo": "Devocional Admin",
            "categoria": "Devocional",
            "conteudo": "Reflexao publicada pela equipe.",
        }

        def config(chave, padrao=""):
            valores = {
                "programacao.domingo": "Domingo as 18h",
                "programacao.quarta": "Quarta as 20h",
                "programacao.celulas": "Durante a semana",
                "doacao.mensagem": "Mensagem de contribuicao configurada no painel.",
            }
            return valores.get(chave, padrao)

        with patch("app.obter_igreja", return_value={"nome": "Igreja Teste", "endereco": "Rua Central"}), \
             patch("app.listar_eventos_publicos", return_value=[evento]), \
             patch("app.listar_mural_publico", side_effect=[[aviso], [devocional]]), \
             patch("app.gerar_metricas_app", return_value={"eventos": 1, "avisos": 1, "devocionais": 1, "testemunhos": 0, "visitantes": 3}), \
             patch("app.gerar_metricas", return_value={}), \
             patch("app.obter_config", side_effect=config):
            resposta = self.client.get("/app")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Culto Jovem".encode(), resposta.data)
        self.assertIn("Aviso Admin".encode(), resposta.data)
        self.assertIn("Devocional Admin".encode(), resposta.data)
        self.assertIn("Domingo".encode(), resposta.data)

    def test_app_usuario_evento_inexistente_redireciona_para_agenda(self):
        resposta = self.client.get("/app/eventos/999999", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app/eventos", resposta.headers["Location"])

    def test_app_usuario_oracao_valida_campos_obrigatorios(self):
        resposta = self.client.post(
            "/app/oracao",
            data={"solicitante_nome": "", "pedido": ""},
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Informe seu nome e o pedido de".encode(), resposta.data)

    def test_rotas_privadas_exigem_login(self):
        resposta = self.client.get("/membros/listar", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.headers["Location"])

    def test_listagens_privadas_renderizam_com_login(self):
        self.autenticar()

        for rota in [
            "/pessoas/painel",
            "/pessoas/aniversarios",
            "/membros/listar",
            "/financeiro/painel",
            "/financeiro/receitas",
            "/financeiro/despesas",
            "/financeiro/cadastros",
            "/financeiro/categorias",
            "/financeiro/centros-custo",
            "/financeiro/contas",
            "/financeiro/formas-recebimento",
            "/financeiro/formas-pagamento",
            "/ministerios/listar",
            "/ministerios/painel",
            "/usuarios/listar",
            "/celulas/listar",
            "/celulas/painel",
            "/eventos/listar",
            "/financeiro/listar",
            "/comunicacao/painel",
            "/comunicacao/listar",
            "/relatorios/listar",
            "/configuracoes/listar",
            "/configuracoes/igreja",
            "/configuracoes/historia",
            "/configuracoes/informacoes",
            "/configuracoes/programacao",
            "/configuracoes/permissoes",
            "/configuracoes/app",
            "/configuracoes/modulos",
            "/familias/listar",
            "/fornecedores/listar",
            "/doacoes/listar",
            "/mural/listar",
            "/intercessao/painel",
            "/intercessao/listar",
            "/intercessao/testemunhos",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 200)

    def test_cadastro_publico_exige_email_e_senha_para_visitante(self):
        resposta = self.client.post(
            "/cadastro",
            data={"nome": "Pessoa Teste"},
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Informe seu nome, e-mail e senha".encode(), resposta.data)

    def test_cadastro_publico_registra_visitante_no_app(self):
        with patch("app.email_membro_em_uso", return_value=False), \
             patch("app.email_em_uso", return_value=False), \
             patch("app.cadastrar_visitante_app") as cadastrar_visitante:
            resposta = self.client.post(
                "/app/cadastro",
                data={
                    "nome": "Visitante Teste",
                    "email": "visitante@exemplo.com",
                    "telefone": "(14) 99999-9999",
                    "whatsapp": "(14) 99999-9999",
                    "senha": "visitante123",
                    "confirmar_senha": "visitante123",
                    "interesse": "Quero conhecer a igreja",
                    "mensagem": "Participei do culto pelo app.",
                },
                follow_redirects=False,
            )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.headers["Location"])
        cadastrar_visitante.assert_called_once_with(
            "Visitante Teste",
            "visitante@exemplo.com",
            "(14) 99999-9999",
            "(14) 99999-9999",
            "Quero conhecer a igreja",
            "Participei do culto pelo app.",
            "visitante123",
        )

    def test_inserir_membro_valida_telefone(self):
        self.autenticar()

        resposta = self.client.post(
            "/membros/inserir",
            data={"nome": "Novo Membro", "telefone": "123", "ministerio": "Louvor"},
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Informe um telefone v".encode(), resposta.data)

    def test_login_admin_redireciona_para_dashboard(self):
        resposta = self.client.post(
            "/login",
            data={"email": "admin@igreja.org", "senha": "admin123"},
            follow_redirects=False,
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/dashboard", resposta.headers["Location"])

    def test_login_visitante_redireciona_para_app(self):
        usuario = {
            "id": 2,
            "nome": "Visitante Teste",
            "email": "visitante@igreja.org",
            "senha_hash": generate_password_hash("visitante123"),
            "status": "Ativo",
            "perfil": "Visitante",
        }
        with patch("app.obter_usuario_por_email", return_value=usuario), patch("app.db_write"):
            resposta = self.client.post(
                "/login",
                data={"email": "visitante@igreja.org", "senha": "visitante123"},
                follow_redirects=False,
            )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app", resposta.headers["Location"])

    def test_visitante_logado_nao_acessa_admin(self):
        with self.client.session_transaction() as sess:
            sess["usuario_logado"] = "visitante@igreja.org"
            sess["usuario_nome"] = "Visitante Teste"
            sess["usuario_perfil"] = "Visitante"
            sess["usuario_id"] = 2

        resposta = self.client.get("/dashboard", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app", resposta.headers["Location"])

    def test_app_oracao_registra_reacao_publica(self):
        with patch("app.pedido_oracao_publico_existe", return_value=True), patch("app.db_write") as db_write:
            resposta = self.client.post(
                "/app/oracao/10/reagir",
                data={"tipo": "amem", "autor_nome": "Visitante"},
                follow_redirects=False,
            )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app/oracao", resposta.headers["Location"])
        self.assertIn("INSERT INTO pedido_oracao_reacoes", db_write.call_args_list[0].args[0])
        self.assertIn("UPDATE pedidos_oracao", db_write.call_args_list[1].args[0])

    def test_app_oracao_registra_comentario_publico(self):
        with patch("app.pedido_oracao_publico_existe", return_value=True), patch("app.db_write") as db_write:
            resposta = self.client.post(
                "/app/oracao/10/comentar",
                data={"autor_nome": "Visitante", "comentario": "Estamos juntos em oracao."},
                follow_redirects=False,
            )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app/oracao", resposta.headers["Location"])
        self.assertIn("INSERT INTO pedido_oracao_comentarios", db_write.call_args.args[0])

    def test_exclusao_logica_nao_aceita_get(self):
        self.autenticar()

        for rota in [
            "/membros/excluir/101",
            "/membros/inativar/101",
            "/ministerios/excluir/201",
            "/usuarios/excluir/1",
            "/familias/excluir/1",
            "/fornecedores/excluir/1",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 405)

    def test_acoes_operacionais_nao_aceitam_get(self):
        self.autenticar()

        for rota in [
            "/mural/publicar/1",
            "/mural/arquivar/1",
            "/intercessao/orar/1",
            "/intercessao/responder/1",
            "/intercessao/arquivar/1",
            "/app/oracao/1/reagir",
            "/app/oracao/1/comentar",
            "/doacoes/receber/1",
            "/doacoes/cancelar/1",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 405)

    def test_inativar_membro_usa_post_com_redirect(self):
        self.autenticar()

        resposta = self.client.post("/membros/inativar/103", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/membros/listar", resposta.headers["Location"])


if __name__ == "__main__":
    unittest.main()
