// GymManager — telas TL01 a TL09 (GYM-SRC-006)
// Protótipos: prototipos/ (GYM-REQ-004) · Requisitos: ERS 4.4

import { consulta, del, get, patch, post, put, sessao } from "./api.js";
import {
  $, $$, aviso, confirmar, dataBR, dataHoraBR, erro, erroNoFormulario, esc, graficoLinha,
  hojeISO, iniciais, kg, lerFormulario, opcoes, selo,
} from "./ui.js";

const ehEquipe = () => ["ADMIN", "INSTRUTOR"].includes(sessao.usuario?.perfil);
const primeiroNome = (nome) => (nome || "").split(" ")[0];

function cabecalho(titulo, subtitulo = "", acoes = "", trilha = "") {
  return `<header class="topo">
    <div>${trilha ? `<p class="trilha">${trilha}</p>` : ""}<h1>${titulo}</h1>${subtitulo ? `<p class="sub">${subtitulo}</p>` : ""}</div>
    <div class="acoes">${acoes}</div></header>`;
}

// =========================================================== TL01 — Login
export async function telaLogin(raiz) {
  raiz.innerHTML = `
  <main class="login">
    <form class="cartao login-cartao" id="form-login" novalidate>
      <div class="marca"><span class="marca-icone">◆</span> GymManager</div>
      <h1>Entrar</h1>
      <label>E-mail<input name="email" type="email" autocomplete="username" required></label>
      <label>Senha<input name="senha" type="password" autocomplete="current-password" required></label>
      <button class="btn btn-primario" type="submit">Entrar</button>
    </form>
  </main>`;
  const form = $("#form-login", raiz);
  form.elements.email.focus();
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const dados = lerFormulario(form);
    if (!dados.email || !dados.senha) return aviso("Informe e-mail e senha.", "erro");
    try {
      sessao.salvar(await post("/auth/login", dados));
      window.location.hash = "#/painel";
    } catch (e) {
      erroNoFormulario(form, e);
    }
  });
}

// =========================================================== TL02 — Painel
export async function telaPainel(raiz) {
  return ehEquipe() ? painelEquipe(raiz) : painelAluno(raiz);
}

async function painelEquipe(raiz) {
  const [alunos, fichas, exercicios] = await Promise.all([
    get("/alunos?ativo=true"), get("/fichas?ativa=true"), get("/exercicios?ativo=true"),
  ]);
  const hoje = hojeISO();
  const limite = new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10);
  const renovar = fichas.filter((f) => f.data_fim && f.data_fim >= hoje && f.data_fim <= limite);
  const comFicha = new Set(fichas.map((f) => f.aluno.id));
  const semFicha = alunos.filter((a) => !comFicha.has(a.id));
  const saudacao = new Date().getHours() < 12 ? "Bom dia" : new Date().getHours() < 18 ? "Boa tarde" : "Boa noite";
  const dataExtenso = new Date().toLocaleDateString("pt-BR", { weekday: "long", day: "numeric", month: "long" });

  raiz.innerHTML = `
    ${cabecalho(`${saudacao}, ${esc(primeiroNome(sessao.usuario.nome))}`, esc(dataExtenso),
      `<a class="btn" href="#/alunos?novo=1">+ Novo aluno</a><a class="btn btn-primario" href="#/fichas/nova">+ Novo treino</a>`)}
    <section class="metricas">
      <div class="cartao metrica"><span>Alunos ativos</span><strong>${alunos.length}</strong></div>
      <div class="cartao metrica"><span>Fichas vigentes</span><strong>${fichas.length}</strong></div>
      <div class="cartao metrica"><span>Fichas para renovar (7 dias)</span><strong class="cor-alerta">${renovar.length}</strong></div>
      <div class="cartao metrica"><span>Alunos sem ficha</span><strong class="cor-perigo">${semFicha.length}</strong></div>
    </section>
    <section class="grade-2">
      <div class="cartao">
        <div class="cartao-topo"><h2>Fichas vigentes</h2><a href="#/fichas">Ver todas</a></div>
        ${fichas.length ? `<table class="tabela"><thead><tr><th>Aluno</th><th>Ficha</th><th>Válida até</th><th></th></tr></thead><tbody>
          ${fichas.slice(0, 8).map((f) => `<tr>
            <td><span class="avatar">${esc(iniciais(f.aluno.nome))}</span> ${esc(f.aluno.nome)}</td>
            <td>${esc(f.nome)}</td><td>${dataBR(f.data_fim)}</td>
            <td><a href="#/historico?aluno=${f.aluno.id}">Histórico</a></td></tr>`).join("")}
          </tbody></table>` : `<p class="vazio">Nenhuma ficha vigente.</p>`}
      </div>
      <div class="cartao">
        <div class="cartao-topo"><h2>Alunos sem ficha</h2></div>
        ${semFicha.length ? `<ul class="lista">${semFicha.slice(0, 8).map((a) => `<li>
            <span><span class="avatar">${esc(iniciais(a.nome))}</span> ${esc(a.nome)}</span>
            <a class="btn btn-pequeno" href="#/fichas/nova?aluno=${a.id}">Montar ficha</a></li>`).join("")}</ul>`
          : `<p class="vazio">Todos os alunos ativos têm ficha.</p>`}
        <p class="nota">${exercicios.length} exercícios ativos no catálogo.</p>
      </div>
    </section>`;
}

async function painelAluno(raiz) {
  const eu = sessao.usuario;
  const [fichas, historico] = await Promise.all([get("/fichas?ativa=true"), get(`/alunos/${eu.id}/historico`)]);
  const aberta = historico.execucoes.find((e) => !e.fim && fichas.some((f) => f.id === e.ficha.id));
  const ficha = aberta ? fichas.find((f) => f.id === aberta.ficha.id) : fichas[0];

  // Dias da semana (seg..dom) com treino registrado
  const agora = new Date();
  const segunda = new Date(agora);
  segunda.setHours(0, 0, 0, 0);
  segunda.setDate(agora.getDate() - ((agora.getDay() + 6) % 7));
  const diasComTreino = new Set(historico.execucoes
    .map((e) => new Date(e.inicio)).filter((d) => d >= segunda)
    .map((d) => (d.getDay() + 6) % 7));
  const nomesDias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"];
  const hojeIdx = (agora.getDay() + 6) % 7;

  const feitos = new Set((aberta?.registros || []).map((r) => r.ficha_exercicio_id));
  const evolucao = historico.evolucao.find((s) => s.pontos.length > 1) || historico.evolucao[0];

  raiz.innerHTML = `
    ${cabecalho(`Olá, ${esc(primeiroNome(eu.nome))}`,
      `Você treinou ${diasComTreino.size} ${diasComTreino.size === 1 ? "dia" : "dias"} nesta semana.`,
      ficha ? `<a class="btn btn-primario" href="#/treino/${ficha.id}">${aberta ? "Continuar treino" : "Iniciar treino"}</a>` : "")}
    <section class="grade-2">
      <div class="cartao">
        ${ficha ? `
          <div class="cartao-topo"><div><span class="etiqueta">${esc(ficha.nome)}</span>
            <h2>${aberta ? "Treino em andamento" : "Próximo treino"}</h2></div>
            <div class="placar"><strong>${feitos.size} de ${ficha.exercicios.length}</strong><span>exercícios feitos</span></div></div>
          <progress max="${ficha.exercicios.length}" value="${feitos.size}"></progress>
          <ul class="lista lista-treino">${ficha.exercicios.map((i) => `<li class="${feitos.has(i.id) ? "feito" : ""}">
            <span><span class="check">${feitos.has(i.id) ? "✓" : ""}</span> ${esc(i.exercicio.nome)}</span>
            <span class="mudo">${i.series} × ${i.repeticoes}</span><strong>${kg(i.carga_kg)}</strong></li>`).join("")}</ul>`
          : `<h2>Sem ficha ativa</h2><p class="vazio">Você ainda não tem fichas atribuídas. Procure seu instrutor.</p>`}
      </div>
      <div class="coluna">
        <div class="cartao"><h2>Semana</h2><div class="semana">${nomesDias.map((n, i) => `
          <div><small>${n}</small><span class="dia ${diasComTreino.has(i) ? "dia-ok" : i === hojeIdx ? "dia-hoje" : ""}">${diasComTreino.has(i) ? "✓" : ""}</span></div>`).join("")}
        </div></div>
        <div class="cartao">${evolucao ? `<h2>Carga no ${esc(evolucao.exercicio.nome.toLowerCase())}</h2>
          ${graficoLinha(evolucao.pontos.map((p) => ({ valor: p.carga_kg, rotulo: dataBR(p.data) })), { rotuloY: (v) => `${v}` })}
          <a href="#/historico">Ver evolução completa</a>` : `<h2>Evolução</h2><p class="vazio">Registre treinos para acompanhar sua evolução.</p>`}
        </div>
      </div>
    </section>`;
}

// =========================================================== TL03 — Usuários e instrutores (ADMIN)
export async function telaUsuarios(raiz, _p, q) {
  const filtros = { nome: q.get("nome") || "", perfil: q.get("perfil") || "" };
  const usuarios = await get("/usuarios" + consulta(filtros));
  const perfis = [{ id: "ADMIN", nome: "Administrador" }, { id: "INSTRUTOR", nome: "Instrutor" }, { id: "ALUNO", nome: "Aluno" }];
  const nomePerfil = Object.fromEntries(perfis.map((p) => [p.id, p.nome]));

  raiz.innerHTML = `
    ${cabecalho("Usuários e instrutores", "Cadastro de usuários e definição de perfis", `<button class="btn btn-primario" data-novo>+ Novo usuário</button>`)}
    <form class="filtros" id="filtros">
      <input name="nome" placeholder="Buscar por nome" value="${esc(filtros.nome)}">
      <select name="perfil"><option value="">Todos os perfis</option>${opcoes(perfis, filtros.perfil)}</select>
      <button class="btn">Filtrar</button>
    </form>
    <div id="area-form"></div>
    <div class="cartao"><table class="tabela"><thead><tr><th>Nome</th><th>E-mail</th><th>Perfil</th><th>Situação</th><th></th></tr></thead>
    <tbody>${usuarios.map((u) => `<tr>
      <td>${esc(u.nome)}</td><td>${esc(u.email)}</td><td>${nomePerfil[u.perfil]}</td><td>${selo(u.ativo)}</td>
      <td class="acoes-linha"><button class="btn btn-pequeno" data-editar="${u.id}">Editar</button>
      ${u.ativo && u.id !== sessao.usuario.id ? `<button class="btn btn-pequeno btn-perigo" data-inativar="${u.id}">Inativar</button>` : ""}</td></tr>`).join("")
      || `<tr><td colspan="5" class="vazio">Nenhum usuário encontrado.</td></tr>`}</tbody></table></div>`;

  $("#filtros", raiz).addEventListener("submit", (ev) => {
    ev.preventDefault();
    window.location.hash = "#/usuarios" + consulta(lerFormulario(ev.target));
  });

  const abrirForm = (u) => {
    $("#area-form", raiz).innerHTML = `
      <form class="cartao formulario" id="form-usuario" novalidate>
        <h2>${u ? "Editar usuário" : "Novo usuário"}</h2>
        <div class="grade-campos">
          <label class="largo">Nome completo<input name="nome" value="${esc(u?.nome)}" required></label>
          <label>E-mail<input name="email" type="email" value="${esc(u?.email)}" required></label>
          <label>Perfil<select name="perfil" ${u?.id === sessao.usuario.id ? "disabled" : ""}>${opcoes(perfis, u?.perfil || "INSTRUTOR")}</select></label>
          <label>${u ? "Nova senha (opcional)" : "Senha inicial"}<input name="senha" type="password" autocomplete="new-password" ${u ? "" : "required"}></label>
          ${u && u.id !== sessao.usuario.id ? `<label class="check-linha"><input type="checkbox" name="ativo" ${u.ativo ? "checked" : ""}> Ativo</label>` : ""}
        </div>
        <p class="nota">Senha: mínimo de 8 caracteres, com letras e números.</p>
        <div class="rodape-form"><button type="button" class="btn" data-cancelar>Cancelar</button><button class="btn btn-primario">Salvar</button></div>
      </form>`;
    const form = $("#form-usuario", raiz);
    form.scrollIntoView({ behavior: "smooth" });
    $("[data-cancelar]", form).onclick = () => { $("#area-form", raiz).innerHTML = ""; };
    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const dados = lerFormulario(form);
      if (!dados.senha) delete dados.senha;
      try {
        if (u) await put(`/usuarios/${u.id}`, dados);
        else await post("/usuarios", dados);
        aviso("Usuário salvo.");
        telaUsuarios(raiz, _p, q);
      } catch (e) { erroNoFormulario(form, e); }
    });
  };

  raiz.onclick = async (ev) => {
    const alvo = ev.target.closest("button");
    if (!alvo) return;
    if (alvo.dataset.novo !== undefined) abrirForm(null);
    if (alvo.dataset.editar) abrirForm(usuarios.find((u) => u.id === Number(alvo.dataset.editar)));
    if (alvo.dataset.inativar && confirmar("Inativar este usuário? Ele perderá o acesso ao sistema.")) {
      try { await del(`/usuarios/${alvo.dataset.inativar}`); aviso("Usuário inativado."); telaUsuarios(raiz, _p, q); } catch (e) { erro(e); }
    }
  };
}

// =========================================================== TL04 — Alunos
export async function telaAlunos(raiz, _p, q) {
  const filtros = { nome: q.get("nome") || "", ativo: q.get("ativo") || "true" };
  const alunos = await get("/alunos" + consulta({ ...filtros, ativo: filtros.ativo === "todos" ? "" : filtros.ativo }));

  raiz.innerHTML = `
    ${cabecalho("Alunos", "", `<button class="btn btn-primario" data-novo>+ Novo aluno</button>`)}
    <form class="filtros" id="filtros">
      <input name="nome" placeholder="Buscar por nome ou e-mail" value="${esc(filtros.nome)}">
      <select name="ativo">${opcoes([{ id: "true", nome: "Ativos" }, { id: "false", nome: "Inativos" }, { id: "todos", nome: "Todos" }], filtros.ativo)}</select>
      <button class="btn">Filtrar</button>
    </form>
    <div id="area-form"></div>
    <div class="cartao"><table class="tabela"><thead><tr><th>Aluno</th><th>E-mail</th><th>Telefone</th><th>Situação</th><th></th></tr></thead>
    <tbody>${alunos.map((a) => `<tr>
      <td><span class="avatar">${esc(iniciais(a.nome))}</span> ${esc(a.nome)}</td><td>${esc(a.email)}</td><td>${esc(a.telefone || "—")}</td><td>${selo(a.ativo)}</td>
      <td class="acoes-linha">
        <a class="btn btn-pequeno" href="#/historico?aluno=${a.id}">Histórico</a>
        <button class="btn btn-pequeno" data-editar="${a.id}">Editar</button>
        ${a.ativo ? `<button class="btn btn-pequeno btn-perigo" data-inativar="${a.id}">Inativar</button>`
                  : `<button class="btn btn-pequeno" data-reativar="${a.id}">Reativar</button>`}</td></tr>`).join("")
      || `<tr><td colspan="5" class="vazio">Nenhum aluno encontrado.</td></tr>`}</tbody></table></div>`;

  $("#filtros", raiz).addEventListener("submit", (ev) => {
    ev.preventDefault();
    const dados = lerFormulario(ev.target);
    window.location.hash = "#/alunos" + consulta({ ...dados, ativo: ev.target.elements.ativo.value });
  });

  const recarregar = () => telaAlunos(raiz, _p, new URLSearchParams(consulta(filtros)));

  const abrirForm = (a) => {
    $("#area-form", raiz).innerHTML = `
      <form class="cartao formulario" id="form-aluno" novalidate>
        <p class="trilha">Alunos › ${a ? "Editar aluno" : "Novo aluno"}</p>
        <h2>Dados pessoais</h2>
        <div class="grade-campos">
          <label class="largo">Nome completo<input name="nome" value="${esc(a?.nome)}" required></label>
          <label>E-mail<input name="email" type="email" value="${esc(a?.email)}" required></label>
          <label>Telefone<input name="telefone" value="${esc(a?.telefone)}" placeholder="(92) 99123-4567"></label>
          <label>Data de nascimento<input name="data_nascimento" type="date" value="${esc(a?.data_nascimento)}"></label>
        </div>
        <h2>Acesso ao sistema</h2>
        <div class="grade-campos">
          <label>${a ? "Nova senha (opcional)" : "Senha provisória"}<input name="senha" type="password" autocomplete="new-password" ${a ? "" : "required"}></label>
        </div>
        <p class="nota">Senha: mínimo de 8 caracteres, com letras e números.</p>
        <div class="rodape-form"><button type="button" class="btn" data-cancelar>Cancelar</button><button class="btn btn-primario">Salvar aluno</button></div>
      </form>`;
    const form = $("#form-aluno", raiz);
    form.elements.nome.focus();
    $("[data-cancelar]", form).onclick = () => { $("#area-form", raiz).innerHTML = ""; };
    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const dados = lerFormulario(form);
      if (!dados.senha) delete dados.senha;
      try {
        if (a) await put(`/alunos/${a.id}`, dados);
        else await post("/alunos", dados);
        aviso("Aluno salvo.");
        recarregar();
      } catch (e) { erroNoFormulario(form, e); }
    });
  };

  raiz.onclick = async (ev) => {
    const alvo = ev.target.closest("button");
    if (!alvo) return;
    try {
      if (alvo.dataset.novo !== undefined) abrirForm(null);
      if (alvo.dataset.editar) abrirForm(alunos.find((a) => a.id === Number(alvo.dataset.editar)));
      if (alvo.dataset.inativar && confirmar("Inativar este aluno? Ele não poderá entrar nem receber novas fichas. O histórico será mantido.")) {
        await del(`/alunos/${alvo.dataset.inativar}`); aviso("Aluno inativado."); recarregar();
      }
      if (alvo.dataset.reativar) { await put(`/alunos/${alvo.dataset.reativar}`, { ativo: true }); aviso("Aluno reativado."); recarregar(); }
    } catch (e) { erro(e); }
  };

  if (q.get("novo")) abrirForm(null);
}

// =========================================================== TL05 — Catálogo de exercícios
export async function telaExercicios(raiz, _p, q) {
  const filtros = { nome: q.get("nome") || "", grupo_muscular: q.get("grupo") || "" };
  const todos = await get("/exercicios");
  const grupos = [...new Set(todos.map((e) => e.grupo_muscular).filter(Boolean))].sort();
  const lista = todos.filter((e) =>
    (!filtros.nome || e.nome.toLowerCase().includes(filtros.nome.toLowerCase())) &&
    (!filtros.grupo_muscular || e.grupo_muscular === filtros.grupo_muscular));

  raiz.innerHTML = `
    ${cabecalho("Catálogo de exercícios", "", `<button class="btn btn-primario" data-novo>+ Novo exercício</button>`)}
    <form class="filtros" id="filtros"><input name="nome" placeholder="Buscar exercício..." value="${esc(filtros.nome)}"><button class="btn">Buscar</button></form>
    <div class="chips"><a class="chip ${filtros.grupo_muscular ? "" : "chip-ativo"}" href="#/exercicios">Todos</a>
      ${grupos.map((g) => `<a class="chip ${g === filtros.grupo_muscular ? "chip-ativo" : ""}" href="#/exercicios${consulta({ grupo: g })}">${esc(g)}</a>`).join("")}</div>
    <div id="area-form"></div>
    <div class="cartao"><table class="tabela"><thead><tr><th>Exercício</th><th>Grupo muscular</th><th>Descrição</th><th>Situação</th><th></th></tr></thead>
    <tbody>${lista.map((e) => `<tr>
      <td><strong>${esc(e.nome)}</strong></td><td>${esc(e.grupo_muscular || "—")}</td><td class="mudo">${esc(e.descricao || "")}</td><td>${selo(e.ativo)}</td>
      <td class="acoes-linha"><button class="btn btn-pequeno" data-editar="${e.id}">Editar</button>
        ${e.ativo ? `<button class="btn btn-pequeno btn-perigo" data-inativar="${e.id}">Inativar</button>`
                  : `<button class="btn btn-pequeno" data-reativar="${e.id}">Reativar</button>`}</td></tr>`).join("")
      || `<tr><td colspan="5" class="vazio">Nenhum exercício encontrado.</td></tr>`}</tbody></table></div>`;

  $("#filtros", raiz).addEventListener("submit", (ev) => {
    ev.preventDefault();
    window.location.hash = "#/exercicios" + consulta({ nome: ev.target.elements.nome.value.trim(), grupo: filtros.grupo_muscular });
  });

  const abrirForm = (e) => {
    $("#area-form", raiz).innerHTML = `
      <form class="cartao formulario" id="form-exercicio" novalidate>
        <h2>${e ? "Editar exercício" : "Novo exercício"}</h2>
        <div class="grade-campos">
          <label>Nome<input name="nome" value="${esc(e?.nome)}" required></label>
          <label>Grupo muscular<input name="grupo_muscular" list="grupos" value="${esc(e?.grupo_muscular)}">
            <datalist id="grupos">${grupos.map((g) => `<option value="${esc(g)}">`).join("")}</datalist></label>
          <label class="largo">Descrição<textarea name="descricao" rows="3">${esc(e?.descricao)}</textarea></label>
        </div>
        <div class="rodape-form"><button type="button" class="btn" data-cancelar>Cancelar</button><button class="btn btn-primario">Salvar</button></div>
      </form>`;
    const form = $("#form-exercicio", raiz);
    form.elements.nome.focus();
    $("[data-cancelar]", form).onclick = () => { $("#area-form", raiz).innerHTML = ""; };
    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      try {
        if (e) await put(`/exercicios/${e.id}`, lerFormulario(form));
        else await post("/exercicios", lerFormulario(form));
        aviso("Exercício salvo.");
        telaExercicios(raiz, _p, q);
      } catch (err) { erroNoFormulario(form, err); }
    });
  };

  raiz.onclick = async (ev) => {
    const alvo = ev.target.closest("button");
    if (!alvo) return;
    try {
      if (alvo.dataset.novo !== undefined) abrirForm(null);
      if (alvo.dataset.editar) abrirForm(todos.find((e) => e.id === Number(alvo.dataset.editar)));
      if (alvo.dataset.inativar && confirmar("Inativar este exercício? Ele continuará nas fichas existentes, mas não poderá ser usado em novas.")) {
        await del(`/exercicios/${alvo.dataset.inativar}`); aviso("Exercício inativado."); telaExercicios(raiz, _p, q);
      }
      if (alvo.dataset.reativar) { await put(`/exercicios/${alvo.dataset.reativar}`, { ativo: true }); aviso("Exercício reativado."); telaExercicios(raiz, _p, q); }
    } catch (e) { erro(e); }
  };
}

// =========================================================== TL06 — Fichas (lista e montagem)
export async function telaFichas(raiz, _p, q) {
  const alunoId = q.get("aluno") || "";
  const [fichas, alunos] = await Promise.all([get("/fichas" + consulta({ aluno_id: alunoId })), get("/alunos")]);
  raiz.innerHTML = `
    ${cabecalho("Treinos", "Fichas de treino atribuídas aos alunos", `<a class="btn btn-primario" href="#/fichas/nova">+ Novo treino</a>`)}
    <form class="filtros" id="filtros"><select name="aluno"><option value="">Todos os alunos</option>${opcoes(alunos, alunoId)}</select><button class="btn">Filtrar</button></form>
    <div class="cartao"><table class="tabela"><thead><tr><th>Ficha</th><th>Aluno</th><th>Instrutor</th><th>Período</th><th>Exercícios</th><th>Situação</th><th></th></tr></thead>
    <tbody>${fichas.map((f) => `<tr>
      <td><strong>${esc(f.nome)}</strong></td><td>${esc(f.aluno.nome)}</td><td>${esc(f.instrutor.nome)}</td>
      <td>${dataBR(f.data_inicio)} – ${dataBR(f.data_fim)}</td><td>${f.exercicios.length}</td><td>${selo(f.vigente, ["Vigente", "Encerrada"])}</td>
      <td class="acoes-linha"><a class="btn btn-pequeno" href="#/fichas/${f.id}">Abrir</a></td></tr>`).join("")
      || `<tr><td colspan="7" class="vazio">Nenhuma ficha encontrada.</td></tr>`}</tbody></table></div>`;
  $("#filtros", raiz).addEventListener("submit", (ev) => {
    ev.preventDefault();
    window.location.hash = "#/fichas" + consulta({ aluno: ev.target.elements.aluno.value });
  });
}

export async function telaMontarFicha(raiz, params, q) {
  const id = params.id;
  const [alunos, catalogo, ficha] = await Promise.all([
    get("/alunos?ativo=true"), get("/exercicios"), id ? get(`/fichas/${id}`) : Promise.resolve(null),
  ]);
  if (ficha && !alunos.some((a) => a.id === ficha.aluno.id)) alunos.push({ ...ficha.aluno, nome: `${ficha.aluno.nome} (inativo)` });

  // Estado local dos itens (id existe apenas para itens já salvos)
  let itens = (ficha?.exercicios || []).map((i) => ({
    id: i.id, exercicio: i.exercicio, series: i.series, repeticoes: i.repeticoes, carga_kg: i.carga_kg, descanso_s: i.descanso_s,
  }));
  let busca = "", grupo = "";
  const grupos = [...new Set(catalogo.filter((e) => e.ativo).map((e) => e.grupo_muscular).filter(Boolean))].sort();

  raiz.innerHTML = `
    <form id="form-ficha" novalidate>
      ${cabecalho(id ? "Editar treino" : "Montar treino", "",
        `<a class="btn" href="#/fichas">Cancelar</a>
         ${ficha?.ativa ? `<button type="button" class="btn btn-perigo" data-encerrar>Encerrar ficha</button>` : ""}
         <button class="btn btn-primario">Salvar treino</button>`, `Treinos › ${id ? "Editar treino" : "Novo treino"}`)}
      <div class="grade-campos grade-4">
        <label>Nome do treino<input name="nome" value="${esc(ficha?.nome)}" placeholder="Hipertrofia – Treino A" required></label>
        <label>Aluno<select name="aluno_id" required><option value="">Selecione...</option>${opcoes(alunos, ficha?.aluno.id || q.get("aluno"))}</select></label>
        <label>Data de início<input name="data_inicio" type="date" value="${esc(ficha?.data_inicio || hojeISO())}" required></label>
        <label>Data de fim (opcional)<input name="data_fim" type="date" value="${esc(ficha?.data_fim)}"></label>
      </div>
      <section class="grade-2 grade-montagem">
        <div class="cartao"><h2>Exercícios do treino <span class="mudo" id="qtd"></span></h2><div id="itens"></div></div>
        <div class="cartao"><h2>Biblioteca de exercícios</h2>
          <input id="busca" placeholder="Buscar exercício..." autocomplete="off">
          <div class="chips" id="chips"></div><ul class="lista" id="biblioteca"></ul></div>
      </section>
    </form>`;
  const form = $("#form-ficha", raiz);

  const desenharItens = () => {
    $("#qtd", raiz).textContent = `(${itens.length})`;
    $("#itens", raiz).innerHTML = itens.length ? `<table class="tabela tabela-itens"><thead><tr>
        <th>Exercício</th><th>Séries</th><th>Reps</th><th>Carga (kg)</th><th>Descanso (s)</th><th></th></tr></thead><tbody>
      ${itens.map((i, n) => `<tr data-n="${n}">
        <td><strong>${esc(i.exercicio.nome)}</strong><br><small class="mudo">${esc(i.exercicio.grupo_muscular || "")}</small></td>
        <td><input type="number" min="1" step="1" data-campo="series" value="${i.series}" aria-label="Séries"></td>
        <td><input type="number" min="1" step="1" data-campo="repeticoes" value="${i.repeticoes}" aria-label="Repetições"></td>
        <td><input type="number" min="0" step="0.5" data-campo="carga_kg" value="${i.carga_kg}" aria-label="Carga"></td>
        <td><input type="number" min="0" step="5" data-campo="descanso_s" value="${i.descanso_s}" aria-label="Descanso"></td>
        <td class="acoes-linha"><button type="button" class="btn-icone" data-subir="${n}" title="Subir" ${n === 0 ? "disabled" : ""}>↑</button>
          <button type="button" class="btn-icone" data-descer="${n}" title="Descer" ${n === itens.length - 1 ? "disabled" : ""}>↓</button>
          <button type="button" class="btn-link" data-remover="${n}">Remover</button></td></tr>`).join("")}</tbody></table>`
      : `<p class="vazio">Adicione exercícios da biblioteca. A ficha precisa de pelo menos um exercício.</p>`;
  };

  const desenharBiblioteca = () => {
    $("#chips", raiz).innerHTML = [["", "Todos"], ...grupos.map((g) => [g, g])]
      .map(([v, r]) => `<button type="button" class="chip ${v === grupo ? "chip-ativo" : ""}" data-grupo="${esc(v)}">${esc(r)}</button>`).join("");
    const lista = catalogo.filter((e) => e.ativo &&
      (!grupo || e.grupo_muscular === grupo) && e.nome.toLowerCase().includes(busca.toLowerCase()));
    $("#biblioteca", raiz).innerHTML = lista.map((e) => `<li><span><strong>${esc(e.nome)}</strong><br><small class="mudo">${esc(e.grupo_muscular || "")}</small></span>
      <button type="button" class="btn btn-pequeno" data-adicionar="${e.id}">Adicionar</button></li>`).join("")
      || `<li class="vazio">Nenhum exercício encontrado.</li>`;
  };

  desenharItens();
  desenharBiblioteca();

  $("#busca", raiz).addEventListener("input", (ev) => { busca = ev.target.value; desenharBiblioteca(); });
  $("#itens", raiz).addEventListener("input", (ev) => {
    const linha = ev.target.closest("tr[data-n]");
    if (linha && ev.target.dataset.campo) itens[Number(linha.dataset.n)][ev.target.dataset.campo] = ev.target.value === "" ? null : Number(ev.target.value);
  });

  raiz.onclick = async (ev) => {
    const b = ev.target.closest("button");
    if (!b) return;
    const d = b.dataset;
    if (d.grupo !== undefined) { grupo = d.grupo; desenharBiblioteca(); }
    if (d.adicionar) {
      const e = catalogo.find((x) => x.id === Number(d.adicionar));
      itens.push({ exercicio: e, series: 3, repeticoes: 12, carga_kg: 0, descanso_s: 60 });
      desenharItens();
    }
    if (d.remover !== undefined) { itens.splice(Number(d.remover), 1); desenharItens(); }
    if (d.subir !== undefined) { const n = Number(d.subir); [itens[n - 1], itens[n]] = [itens[n], itens[n - 1]]; desenharItens(); }
    if (d.descer !== undefined) { const n = Number(d.descer); [itens[n + 1], itens[n]] = [itens[n], itens[n + 1]]; desenharItens(); }
    if (d.encerrar !== undefined && confirmar("Encerrar esta ficha? Ela deixará de aparecer como ativa para o aluno; o histórico será mantido.")) {
      try { await put(`/fichas/${id}`, { ativa: false }); aviso("Ficha encerrada."); window.location.hash = "#/fichas"; } catch (e) { erro(e); }
    }
  };

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const dados = lerFormulario(form);
    const corpo = {
      nome: dados.nome,
      aluno_id: dados.aluno_id ? Number(dados.aluno_id) : null,
      data_inicio: dados.data_inicio,
      data_fim: dados.data_fim,
      exercicios: itens.map((i, n) => ({
        ...(i.id ? { id: i.id } : {}), exercicio_id: i.exercicio.id, series: i.series, repeticoes: i.repeticoes,
        carga_kg: i.carga_kg ?? 0, descanso_s: i.descanso_s ?? 0, ordem: n + 1,
      })),
    };
    try {
      const salva = id ? await put(`/fichas/${id}`, corpo) : await post("/fichas", corpo);
      aviso("Treino salvo.");
      window.location.hash = `#/fichas/${salva.id}`;
    } catch (e) {
      const m = /^exercicios\[(\d+)\]\.(\w+)$/.exec(e.campo || "");
      if (m) {
        const campo = $(`tr[data-n="${m[1]}"] [data-campo="${m[2]}"]`, raiz);
        campo?.classList.add("invalido");
        campo?.focus();
      }
      erroNoFormulario(form, e);
    }
  });
}

// =========================================================== TL07 — Minhas fichas (ALUNO)
export async function telaMinhasFichas(raiz) {
  const fichas = await get("/fichas?ativa=true");
  raiz.innerHTML = `
    ${cabecalho("Minhas fichas", "Fichas de treino ativas")}
    ${fichas.length ? fichas.map((f) => `
      <article class="cartao ficha">
        <div class="cartao-topo"><div><h2>${esc(f.nome)}</h2>
          <p class="mudo">Instrutor: ${esc(f.instrutor.nome)} · desde ${dataBR(f.data_inicio)}${f.data_fim ? ` até ${dataBR(f.data_fim)}` : ""}</p></div>
          <a class="btn btn-primario" href="#/treino/${f.id}">Iniciar treino</a></div>
        <table class="tabela"><thead><tr><th>#</th><th>Exercício</th><th>Séries × Reps</th><th>Carga</th><th>Descanso</th></tr></thead><tbody>
        ${f.exercicios.map((i, n) => `<tr><td>${n + 1}</td><td><strong>${esc(i.exercicio.nome)}</strong><br><small class="mudo">${esc(i.exercicio.grupo_muscular || "")}</small></td>
          <td>${i.series} × ${i.repeticoes}</td><td>${kg(i.carga_kg)}</td><td>${i.descanso_s} s</td></tr>`).join("")}
        </tbody></table></article>`).join("")
      : `<div class="cartao"><p class="vazio">Você não tem fichas ativas. Procure seu instrutor.</p></div>`}`;
}

// =========================================================== TL08 — Registro de execução (ALUNO)
export async function telaTreino(raiz, params) {
  const fichaId = Number(params.id);
  const [ficha, historico] = await Promise.all([get(`/fichas/${fichaId}`), get(`/alunos/${sessao.usuario.id}/historico?ficha_id=${fichaId}`)]);
  let execucao = historico.execucoes.find((e) => !e.fim) || null;

  const desenhar = () => {
    const registros = new Map((execucao?.registros || []).map((r) => [r.ficha_exercicio_id, r]));
    raiz.innerHTML = `
      ${cabecalho(esc(ficha.nome), execucao ? `Treino iniciado em ${dataHoraBR(execucao.inicio)}` : "Confira a ficha e inicie o treino",
        execucao ? `<button class="btn btn-primario" data-finalizar>Finalizar treino</button>`
                 : ficha.vigente ? `<button class="btn btn-primario" data-iniciar>Iniciar treino</button>` : "",
        `<a href="#/minhas-fichas">Minhas fichas</a> › Treino`)}
      ${execucao ? `<progress max="${ficha.exercicios.length}" value="${registros.size}"></progress>
        <p class="mudo">${registros.size} de ${ficha.exercicios.length} exercícios registrados</p>` : ""}
      <div class="cartao"><table class="tabela tabela-itens"><thead><tr><th></th><th>Exercício</th><th>Prescrito</th>
        ${execucao ? "<th>Reps feitas</th><th>Carga (kg)</th><th></th>" : "<th>Descanso</th>"}</tr></thead><tbody>
      ${ficha.exercicios.map((i) => {
        const r = registros.get(i.id);
        return `<tr data-item="${i.id}" class="${r ? "feito" : ""}">
          <td><span class="check">${r ? "✓" : ""}</span></td>
          <td><strong>${esc(i.exercicio.nome)}</strong><br><small class="mudo">${esc(i.exercicio.grupo_muscular || "")}</small></td>
          <td>${i.series} × ${i.repeticoes} · ${kg(i.carga_kg)}</td>
          ${execucao ? `<td><input type="number" min="1" step="1" name="repeticoes" value="${r?.repeticoes ?? i.repeticoes}" aria-label="Repetições feitas"></td>
            <td><input type="number" min="0" step="0.5" name="carga_kg" value="${r?.carga_kg ?? i.carga_kg}" aria-label="Carga utilizada"></td>
            <td><button class="btn btn-pequeno ${r ? "" : "btn-primario"}" data-registrar="${i.id}">${r ? "Corrigir" : "Registrar"}</button></td>`
            : `<td>${i.descanso_s} s</td>`}</tr>`;
      }).join("")}</tbody></table></div>`;
  };
  desenhar();

  raiz.onclick = async (ev) => {
    const b = ev.target.closest("button");
    if (!b) return;
    try {
      if (b.dataset.iniciar !== undefined) {
        execucao = await post("/execucoes", { ficha_id: fichaId });
        aviso("Treino iniciado. Bom treino!");
        desenhar();
      }
      if (b.dataset.registrar) {
        const linha = b.closest("tr");
        const repeticoes = Number($("[name=repeticoes]", linha).value);
        const carga = Number($("[name=carga_kg]", linha).value);
        execucao = await post(`/execucoes/${execucao.id}/exercicios`, {
          ficha_exercicio_id: Number(b.dataset.registrar), repeticoes, carga_kg: carga,
        });
        desenhar();
      }
      if (b.dataset.finalizar !== undefined) {
        const faltam = ficha.exercicios.length - execucao.registros.length;
        if (faltam > 0 && !confirmar(`Ainda faltam ${faltam} exercício(s). Finalizar mesmo assim? Só os registrados serão gravados.`)) return;
        await patch(`/execucoes/${execucao.id}/finalizar`);
        aviso("Treino finalizado!");
        window.location.hash = "#/historico";
      }
    } catch (e) { erro(e); }
  };
}

// =========================================================== TL09 — Histórico e evolução
export async function telaHistorico(raiz, _p, q) {
  const equipe = ehEquipe();
  const alunos = equipe ? await get("/alunos") : [];
  const alunoId = equipe ? q.get("aluno") || alunos[0]?.id : sessao.usuario.id;

  if (!alunoId) {
    raiz.innerHTML = `${cabecalho("Histórico e evolução")}<div class="cartao"><p class="vazio">Nenhum aluno cadastrado.</p></div>`;
    return;
  }
  const filtros = { data_inicio: q.get("data_inicio") || "", data_fim: q.get("data_fim") || "" };
  const h = await get(`/alunos/${alunoId}/historico` + consulta(filtros));
  const exId = Number(q.get("exercicio")) || h.evolucao[0]?.exercicio.id;
  const serie = h.evolucao.find((s) => s.exercicio.id === exId);
  const base = equipe ? { aluno: alunoId } : {};

  raiz.innerHTML = `
    ${cabecalho("Histórico e evolução", equipe ? `Aluno: ${esc(h.aluno.nome)}` : "Seus treinos registrados")}
    <form class="filtros" id="filtros">
      ${equipe ? `<select name="aluno">${opcoes(alunos, alunoId)}</select>` : ""}
      <label class="inline">De <input type="date" name="data_inicio" value="${esc(filtros.data_inicio)}"></label>
      <label class="inline">Até <input type="date" name="data_fim" value="${esc(filtros.data_fim)}"></label>
      <button class="btn">Filtrar</button>
    </form>
    <section class="grade-2">
      <div class="cartao"><h2>Evolução de carga</h2>
        ${h.evolucao.length ? `
          <select id="sel-exercicio" aria-label="Exercício">${opcoes(h.evolucao.map((s) => s.exercicio), exId)}</select>
          ${graficoLinha(serie.pontos.map((p) => ({ valor: p.carga_kg, rotulo: dataBR(p.data) })), { rotuloY: (v) => `${v} kg` })}
          ${serie.pontos.length > 1 ? `<p class="destaque">${(() => {
            const dif = serie.pontos.at(-1).carga_kg - serie.pontos[0].carga_kg;
            return `<strong class="${dif >= 0 ? "cor-ok" : "cor-perigo"}">${dif >= 0 ? "+" : ""}${kg(dif)}</strong> desde ${dataBR(serie.pontos[0].data)}`;
          })()}</p>` : ""}`
        : `<p class="vazio">Ainda não há treinos registrados.</p>`}
      </div>
      <div class="cartao"><h2>Treinos realizados (${h.execucoes.length})</h2>
        ${h.execucoes.length ? `<ul class="lista lista-historico">${h.execucoes.map((e) => `<li><details>
          <summary><span><strong>${esc(e.ficha.nome)}</strong><br><small class="mudo">${dataHoraBR(e.inicio)}</small></span>
            <span class="mudo">${e.fim ? `${e.duracao_min} min` : "em andamento"} · ${e.registros.length} exerc.</span></summary>
          <table class="tabela"><tbody>${e.registros.map((r) => `<tr><td>${esc(r.exercicio.nome)}</td><td>${r.repeticoes} reps</td><td>${kg(r.carga_kg)}</td></tr>`).join("")
            || `<tr><td class="vazio">Nenhum exercício registrado.</td></tr>`}</tbody></table>
        </details></li>`).join("")}</ul>` : `<p class="vazio">Nenhum treino no período.</p>`}
      </div>
    </section>`;

  $("#filtros", raiz).addEventListener("submit", (ev) => {
    ev.preventDefault();
    const d = lerFormulario(ev.target);
    window.location.hash = "#/historico" + consulta(equipe ? d : { data_inicio: d.data_inicio, data_fim: d.data_fim });
  });
  $("#sel-exercicio", raiz)?.addEventListener("change", (ev) => {
    window.location.hash = "#/historico" + consulta({ ...base, ...filtros, exercicio: ev.target.value });
  });
}
