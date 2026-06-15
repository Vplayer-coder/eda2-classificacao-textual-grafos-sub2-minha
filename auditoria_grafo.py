import json
import os
import re
import unicodedata
import random

# ==============================================================================
# 1. ESTRUTURAS BASE E CONSTRUÇÃO DO GRAFO (Idênticas ao motor principal)
# ==============================================================================
class Fila:
    def __init__(self): self._itens = []
    def enfileirar(self, item): self._itens.append(item)
    def desenfileirar(self): return self._itens.pop(0) if not self.vazia() else None
    def vazia(self): return len(self._itens) == 0

class Grafo:
    def __init__(self):
        self.vertices_nome = []  
        self.vertices_tipo = []  
        self.adjacencias = []    
        self.pesos = []          

    def adicionar_vertice(self, nome, tipo):
        id_vertice = len(self.vertices_nome)
        self.vertices_nome.append(nome)
        self.vertices_tipo.append(tipo)
        self.adjacencias.append([])
        self.pesos.append([]) 
        return id_vertice

    def adicionar_aresta(self, id_origem, id_destino, peso=1):
        if id_destino not in self.adjacencias[id_origem]:
            self.adjacencias[id_origem].append(id_destino)
            self.pesos[id_origem].append(peso)
        if id_origem not in self.adjacencias[id_destino]:
            self.adjacencias[id_destino].append(id_origem)
            self.pesos[id_destino].append(peso)

    def atualizar_peso_aresta(self, id_o, id_d, novo_peso):
        for i in range(len(self.adjacencias[id_o])):
            if self.adjacencias[id_o][i] == id_d: self.pesos[id_o][i] = novo_peso; break
        for i in range(len(self.adjacencias[id_d])):
            if self.adjacencias[id_d][i] == id_o: self.pesos[id_d][i] = novo_peso; break

    def buscar_id_por_nome(self, nome):
        for i in range(len(self.vertices_nome)):
            if self.vertices_nome[i] == nome: return i
        return -1

def construir_grafo_subnautica():
    grafo = Grafo()
    id_casual   = grafo.adicionar_vertice("CASUAL / IMERSIVO", 2)
    id_tecnico  = grafo.adicionar_vertice("TÉCNICO / PERFORMANCE", 2)
    id_hardcore = grafo.adicionar_vertice("HARDCORE / SOBREVIVÊNCIA", 2)

    id_exploradores = grafo.adicionar_vertice("Exploradores Narrativos", 1)
    id_sociais      = grafo.adicionar_vertice("Jogadores Sociais", 1)
    id_vitimas_medo = grafo.adicionar_vertice("Vítimas do Medo", 1)
    grafo.adicionar_aresta(id_exploradores, id_casual, 1)
    grafo.adicionar_aresta(id_sociais, id_casual, 1)
    grafo.adicionar_aresta(id_vitimas_medo, id_casual, 1)

    id_hardware     = grafo.adicionar_vertice("Hardware / Engine", 1)
    id_estabilidade = grafo.adicionar_vertice("Estabilidade e Bugs", 1)
    id_incompatib   = grafo.adicionar_vertice("Incompatibilidade / Corporativo", 1)
    grafo.adicionar_aresta(id_hardware, id_tecnico, 1)
    grafo.adicionar_aresta(id_estabilidade, id_tecnico, 1)
    grafo.adicionar_aresta(id_incompatib, id_tecnico, 1)

    id_sobrevivencia = grafo.adicionar_vertice("Sobrevivência Pura", 1)
    id_combate       = grafo.adicionar_vertice("Mecânicas de Combate", 1)
    id_progresso     = grafo.adicionar_vertice("Críticos de Progresso", 1)
    grafo.adicionar_aresta(id_sobrevivencia, id_hardcore, 1)
    grafo.adicionar_aresta(id_combate, id_hardcore, 1)
    grafo.adicionar_aresta(id_progresso, id_hardcore, 1)

# ---------------------------------------------------------
# [0] CATEGORIA: CASUAL / IMERSIVO
# ---------------------------------------------------------

# Subcategoria 0.0: Exploradores Narrativos (Foco em beleza, história e mundo)
    exploradores = [
    "historia", "historias", "alienigena", "alienigenas", "alien", "aliens", 
    "lore", "enredo", "narrativa", "misterio", "misterios", "exploracao", 
    "explorar", "explorador", "descobrimento", "descobrir", "bioma", "biomas", 
    "fauna", "flora", "ecossistema", "planeta", "oceano", "mar", "fundo", "agua", 
    "aguas", "lindo", "lindos", "linda", "lindas", "maravilha", "maravilhoso", 
    "incrivel", "espetacular", "cinema", "goty", "goat", "visual", "visuais", 
    "arte", "trilha", "sonora", "musica", "musicas", "audio", "audios", "pda", 
    "imersao", "imersivo", "universo", "segredo", "segredos", "beleza", "peixe", 
    "peixes", "scan", "scanner", "escanear", "ambientacao", "sons", "som"
]

# Subcategoria 0.1: Jogadores Sociais (Foco em multiplayer)
    sociais = [
    "coop", "cooperativo", "multiplayer", "mp", "amigos", "amigo", "amigas", 
    "amiga", "dupla", "trio", "equipe", "grupo", "galera", "social", "party", 
    "juntos", "companhia", "squad", "divertir", "diversao", "divertido", 
    "engracado", "engracados", "rir", "risada", "risadas", "jogarmos", "solo", 
    "sozinho", "singleplayer", "sozinha"
]

# Subcategoria 0.2: Vítimas do Medo (Foco em fobias, sustos e terror)
    vitimas_medo = [
    "assustador", "assustadores", "susto", "sustos", "medo", "pavor", "panico", 
    "fobia", "talassofobia", "megalofobia", "caguei", "infarto", "taquicardia", 
    "coracao", "gelou", "tenso", "tensao", "terror", "horror", "sinistro", 
    "bizarro", "perigoso", "leviata", "leviatas", "monstro", "monstros", 
    "bicho", "bichos", "criatura", "criaturas", "reaper", "ghost", "escuro", 
    "escuridao", "noite", "abismo", "void", "vazio", "arrepio", "kraken", 
    "lula", "molusco", "coletor", "collector", "cagaco", "pânico"
]


# ---------------------------------------------------------
# [1] CATEGORIA: TÉCNICO / PERFORMANCE
# ---------------------------------------------------------

# Subcategoria 1.0: Hardware / Engine (Foco em peças e gráficos técnicos)
    hardware_engine = [
    "ue5", "unreal", "engine", "rtx", "gtx", "amd", "intel", "placa", "video", 
    "gpu", "cpu", "processador", "ram", "memoria", "dlss", "fsr", "fps", 
    "frame", "frames", "40fps", "60fps", "120fps", "1080p", "1440p", "4k", 
    "monitor", "hz", "graficos", "grafico", "textura", "texturas", "iluminacao", 
    "sombras", "ray", "tracing", "pc", "computador", "notebook", "laptop", 
    "specs", "requisitos", "maquina", "loading", "carregamento", "médio", "medio"
]

# Subcategoria 1.1: Estabilidade (Foco em como o jogo roda)
    estabilidade = [
    "crash", "crashes", "travando", "trava", "travamento", "travamentos", 
    "queda", "quedas", "lag", "stuttering", "stutter", "congelou", "congelando", 
    "bug", "bugs", "glitch", "glitches", "otimizacao", "otimizado", "mal", 
    "porca", "pesado", "leve", "desempenho", "performance", "liso", "fluido", 
    "rodou", "roda", "rodando", "crashando", "lixo"
]

# Subcategoria 1.2: Incompatibilidade / Corporativo (Problemas externos e devs)
    incompatibilidade = [
    "dx12", "driver", "drivers", "abrir", "inicia", "tela", "preta", "branca", 
    "erro", "fatal", "eula", "krafton", "dev", "devs", "desenvolvedor", 
    "desenvolvedores", "atualizacao", "atualizacoes", "update", "patch", "fix", 
    "early", "access", "acesso", "antecipado", "ea", "caro", "preco", 
    "reembolso", "refund", "suporte", "unknown", "worlds", "empresa"
]


# ---------------------------------------------------------
# [2] CATEGORIA: SOBREVIVÊNCIA / HARDCORE
# ---------------------------------------------------------

# Subcategoria 2.0: Sobrevivência Pura (Foco em grind, materiais e bases)
    sobrevivencia_pura = [
    "sobrevivencia", "survival", "hardcore", "recurso", "recursos", "farm", 
    "farmar", "grind", "grindar", "minerio", "minerios", "titanio", "cobre", 
    "prata", "ouro", "chumbo", "quartzo", "crafting", "craft", "craftar", 
    "fabricador", "construir", "construcao", "base", "bases", "habitat", 
    "oxigenio", "o2", "comida", "fome", "sede", "inventario", "espaco", 
    "armazenamento", "veiculo", "veiculos", "submarino", "prawn", "traje", 
    "seamoth", "cyclops", "girino", "tadpole", "bateria", "energia", "fôlego", 
    "potável", "potavel", "calcário", "calcario", "vidro"
]

# Subcategoria 2.1: Mecânicas de Combate (Foco na polêmica da violência/defesa)
    mecanicas_combate = [
    "matar", "matei", "morta", "morto", "morre", "mortes", "morrer", "combate", 
    "arma", "armas", "defender", "defesa", "atacar", "ataque", "agressivo", 
    "agressivos", "pacifista", "desarmado", "imortal", "imortais", "invencivel", 
    "dano", "hp", "vida", "faca", "stasis", "rifle", "torpedo", "repulsor", 
    "bater", "fugir", "predador", "predadores", "violencia", "indefeso", 
    "frustrante", "frustração", "porrada", "afugentar", "repelir"
]

# Subcategoria 2.2: Críticos de Progresso (Foco em zerar, limites e upgrades)
    criticos_progresso = [
    "progressao", "progredir", "objetivo", "missoes", "missao", "final", 
    "zerar", "zerei", "limite", "mapa", "barreira", "parede", "invisivel", 
    "biomod", "biomods", "adaptacao", "adaptacoes", "upgrade", "upgrades", 
    "modulo", "modulos", "profundidade", "pressao", "balanceamento", "nerf", 
    "buff", "dificil", "dificuldade", "facil", "curto", "conteudo"
]
    def inserir(palavras, subcat):
        for p in palavras:
            id_p = grafo.buscar_id_por_nome(p)
            if id_p == -1: id_p = grafo.adicionar_vertice(p, 0)
            grafo.adicionar_aresta(id_p, subcat, 1)

    inserir(exploradores, id_exploradores); inserir(sociais, id_sociais); inserir(vitimas_medo, id_vitimas_medo)
    inserir(hardware_engine, id_hardware); inserir(estabilidade, id_estabilidade); inserir(incompatibilidade, id_incompatib)
    inserir(sobrevivencia_pura, id_sobrevivencia); inserir(mecanicas_combate, id_combate); inserir(criticos_progresso, id_progresso)
    return grafo

def calcular_pesos_por_frequencia(grafo, dataset):
    frequencias = [0] * len(grafo.vertices_nome)
    for review in dataset:
        for token in review["tokens_limpos"]:
            id_palavra = grafo.buscar_id_por_nome(token)
            if id_palavra != -1: frequencias[id_palavra] += 1
                
    for i in range(len(grafo.vertices_nome)):
        if grafo.vertices_tipo[i] == 0: 
            peso_calculado = frequencias[i] + 1
            for vizinho in grafo.adjacencias[i]:
                if grafo.vertices_tipo[vizinho] == 1:
                    grafo.atualizar_peso_aresta(i, vizinho, peso_calculado)

def limpar_e_tokenizar(texto_review):
    texto = texto_review.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto_limpo = re.sub(r'[^\w\s]', '', texto)
    todas_palavras = texto_limpo.split()
    
    stopwords = ["o", "a", "os", "as", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "para", "com", "por", "que", "se", "mais", "mas", "me", "meu", "minha", "te", "seu", "sua", "ele", "ela", "eles", "elas", "e", "sao", "foi", "era", "vou", "vai", "esta", "ta", "q", "pra", "nao", "eu", "isso", "esse", "essa", "como", "nada", "ja", "vc", "tu", "voce", "oque", "oq", "assim", "ia", "ter", "so", "muito", "mt", "mto", "bem", "fazer", "quando", "pq", "porque", "sobre", "tudo", "tbm", "tambem", "daqui", "aqui", "entao", "num", "numa", "pelo", "pela", "tipo", "cara", "gente", "alguem", "mim", "comigo", "ti", "contigo", "nosso", "nossa", "vcs", "voces", "queria", "quer", "dizer", "diga", "achei", "acho", "ver", "ir", "ser", "sendo", "fica", "ficou", "ficar", "da", "tem", "tinha", "pode", "podem", "consigo", "faz", "feito", "fizeram"]
    
    tokens_limpos = []
    for palavra in todas_palavras:
        eh_stopword = False
        for stop in stopwords:
            if palavra == stop:
                eh_stopword = True; break
        if not eh_stopword and len(palavra) > 1 and not palavra.isdigit():
            tokens_limpos.append(palavra)
            
    tokens_unicos = []
    for t in tokens_limpos:
        if t not in tokens_unicos: tokens_unicos.append(t)
    return tokens_unicos

# ==============================================================================
# 3. MOTOR DE AUDITORIA E APRESENTAÇÃO
# ==============================================================================
def auditar_bfs_ponderada(grafo, tokens, modo_detalhado=False):
    pontuacoes = [0, 0, 0]
    percentuais = [0.0, 0.0, 0.0]
    categorias_nomes = ["Casual", "Técnico", "Hardcore"]
    tokens_reconhecidos = []
    
    for token in tokens:
        id_palavra = grafo.buscar_id_por_nome(token)
        if id_palavra == -1: continue
        
        tokens_reconhecidos.append(token)
        if modo_detalhado:
            print(f"\n[Token Processado]: '{token}' (Energia Inicial = 1)")
            
        fila = Fila()
        visitados = [False] * len(grafo.vertices_nome)
        
        fila.enfileirar([id_palavra, 1]) 
        visitados[id_palavra] = True
        
        while not fila.vazia():
            item_fila = fila.desenfileirar()
            atual, energia_herdada = item_fila[0], item_fila[1]
            tipo_atual, nome_atual = grafo.vertices_tipo[atual], grafo.vertices_nome[atual]
            
            if tipo_atual == 2:
                if modo_detalhado:
                    print(f"   -> Chegou à Raiz [{nome_atual}] depositando +{energia_herdada} pontos!")
                if "CASUAL" in nome_atual: pontuacoes[0] += energia_herdada
                elif "TÉCNICO" in nome_atual: pontuacoes[1] += energia_herdada
                elif "HARDCORE" in nome_atual: pontuacoes[2] += energia_herdada
                continue 
                
            for idx_vizinho in range(len(grafo.adjacencias[atual])):
                vizinho = grafo.adjacencias[atual][idx_vizinho]
                peso_aresta = grafo.pesos[atual][idx_vizinho]
                
                if grafo.vertices_tipo[vizinho] > tipo_atual and not visitados[vizinho]:
                    nova_energia = energia_herdada * peso_aresta
                    if modo_detalhado:
                        nome_vizinho = grafo.vertices_nome[vizinho]
                        print(f"   -> Propagando de '{nome_atual}' para '{nome_vizinho}' (Peso da Aresta: {peso_aresta}) => Energia Acumulada: {nova_energia}")
                    fila.enfileirar([vizinho, nova_energia])
                    visitados[vizinho] = True
                    
    total_energia = sum(pontuacoes)
    rotulos_finais = []
    
    if total_energia > 0:
        percentuais = [(p / total_energia) * 100 for p in pontuacoes]
    
    if total_energia == 0:
        rotulos_finais = ["Indefinido"]
    elif total_energia < 5:
        maior = max(pontuacoes)
        for i in range(3):
            if pontuacoes[i] == maior:
                rotulos_finais.append(categorias_nomes[i])
                break
    else:
        for i in range(3):
            if percentuais[i] >= 30.0:
                rotulos_finais.append(categorias_nomes[i])
                
    return tokens_reconhecidos, pontuacoes, percentuais, rotulos_finais

def executar_testes_controlados(grafo):
    print("\n" + "="*50)
    print("        BATERIA DE TESTES CONTROLADOS (UNIT TESTS)   ")
    print("="*50)
    
    casos = [
        ("o oceano é lindo, a história do mundo é maravilhosa e o coop é divertido", ["Casual"]),
        ("que jogo lixo, trava muito, a otimização está um lixo, fps caindo", ["Técnico"]),
        ("não deixam a gente matar os monstros, mecânica de sobrevivência ruim", ["Hardcore"]),
        ("o jogo é muito lindo, mas os bugs estão quebrando o fps na minha ue5", ["Casual", "Técnico"])
    ]
    
    for i, (texto, esperado) in enumerate(casos):
        print(f"\n[Teste {i+1}] Entrada: \"{texto}\"")
        tokens = limpar_e_tokenizar(texto)
        _, _, _, obtido = auditar_bfs_ponderada(grafo, tokens, modo_detalhado=False)
        
        esperado_str = " + ".join(esperado)
        obtido_str = " + ".join(obtido)
        
        status = "✅ PASSOU" if set(esperado) == set(obtido) else "❌ FALHOU"
        
        print(f"Esperado: {esperado_str}")
        print(f"Obtido  : {obtido_str}")
        print(f"Status  : {status}")
    print("\nBateria de testes finalizada.")

def exibir_resultados_formatados(reconhecidos, pts, percs, rotulos):
    print("\n-------------------------------------------")
    print("PONTUAÇÃO BRUTA E PERCENTUAIS:")
    print(f"Casual   = {pts[0]} pts ({percs[0]:.1f}%)")
    print(f"Técnico  = {pts[1]} pts ({percs[1]:.1f}%)")
    print(f"Hardcore = {pts[2]} pts ({percs[2]:.1f}%)")
    print(f"\n-> Tokens Validados no Grafo: {reconhecidos}")
    print(f"-> CLASSIFICAÇÃO FINAL      : {' + '.join(rotulos)}")
    print("-------------------------------------------")

def menu_interativo(grafo, dataset):
    while True:
        print("\n" + "="*50)
        print("    SISTEMA DE AUDITORIA E VALIDAÇÃO DE GRAFOS")
        print("="*50)
        print("1 - Testar uma review manual simples")
        print("2 - Auditoria profunda da BFS (Escolher ID ou Aleatório)")
        print("3 - Sortear 5 reviews do Dataset JSON")
        print("4 - Bateria de Testes Controlados (Unit Tests)")
        print("5 - Analisar uma review 'Indefinida' (Sem Correspondência)")
        print("6 - Sair")
        
        escolha = input("\nEscolha uma opção: ")
        
        if escolha == "1":
            texto = input("\nDigite a sua review: ")
            tokens = limpar_e_tokenizar(texto)
            reconhecidos, pts, percs, rotulos = auditar_bfs_ponderada(grafo, tokens, modo_detalhado=False)
            exibir_resultados_formatados(reconhecidos, pts, percs, rotulos)
            
        elif escolha == "2":
            entrada_id = input("\nDigite o ID da review (ou aperte ENTER para aleatória): ")
            review = None
            if entrada_id.isdigit():
                for r in dataset:
                    if r.get("id") == int(entrada_id):
                        review = r; break
                if not review: print("ID não encontrado."); continue
            else:
                review = random.choice(dataset)
                
            texto = review["texto_original"]
            print(f"\n[TEXTO SELECIONADO - ID {review.get('id', '?')}]:\n\"{texto}\"")
            tokens = limpar_e_tokenizar(texto)
            print(f"\nIniciando Auditoria Passo a Passo para os tokens: {tokens}")
            reconhecidos, pts, percs, rotulos = auditar_bfs_ponderada(grafo, tokens, modo_detalhado=True)
            exibir_resultados_formatados(reconhecidos, pts, percs, rotulos)
            
        elif escolha == "3":
            amostras = random.sample(dataset, 5)
            for i, review in enumerate(amostras):
                texto = review["texto_original"].replace('\n', ' ')
                tokens = limpar_e_tokenizar(texto)
                _, pts, percs, rotulos = auditar_bfs_ponderada(grafo, tokens, False)
                print(f"\n[ID: {review.get('id', '?')}] \"{texto[:100]}...\"")
                print(f"-> Classificação: {' + '.join(rotulos)}")
                
        elif escolha == "4":
            executar_testes_controlados(grafo)
            
        elif escolha == "5":
            indefinidas = []
            for rev in dataset:
                tokens = limpar_e_tokenizar(rev["texto_original"])
                _, _, _, rotulos = auditar_bfs_ponderada(grafo, tokens, False)
                if "Indefinido" in rotulos:
                    indefinidas.append((rev, tokens))
            
            if not indefinidas:
                print("Não existem reviews indefinidas no dataset.")
            else:
                escolhida, tokens = random.choice(indefinidas)
                print(f"\n[REVIEW INDEFINIDA SORTEADA - ID {escolhida.get('id', '?')}]")
                print(f"Texto: \"{escolhida['texto_original']}\"")
                print(f"\nMotivo da falha de classificação:")
                print(f"1. Tokens extraídos após limpeza PLN: {tokens}")
                
                reconhecidos = [t for t in tokens if grafo.buscar_id_por_nome(t) != -1]
                print(f"2. Destes, tokens que existem no Dicionário do Grafo: {reconhecidos}")
                
                if not reconhecidos:
                    print("-> CONCLUSÃO: O texto é composto apenas de Stopwords ou jargões não mapeados no Dicionário do Grafo.")
                else:
                    _, pts, _, _ = auditar_bfs_ponderada(grafo, tokens, False)
                    print(f"-> CONCLUSÃO: Os tokens encontrados geraram pouquíssima energia (Soma = {sum(pts)} pontos). A Review não possui carga semântica suficiente para atingir o limiar.")
                
        elif escolha == "6":
            print("Encerrando o sistema de validação...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    nome_ficheiro = "reviews_subnautica2.json"
    if not os.path.exists(nome_ficheiro):
        print(f"Erro: O ficheiro {nome_ficheiro} não foi encontrado!")
        exit()
        
    meu_grafo = construir_grafo_subnautica()
    with open(nome_ficheiro, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    calcular_pesos_por_frequencia(meu_grafo, dataset)
    print("Grafo calibrado. Iniciando terminal de auditoria...")
    
    menu_interativo(meu_grafo, dataset)