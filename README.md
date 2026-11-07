# Classificação de Ocorrências em São Paulo com MLP

Projeto desenvolvido para a **Global Solution 2026 – Segurança Pública Inteligente em São Paulo**, da disciplina de Aprendizado Profundo com Redes Neurais Convolucionais, na FIAP.

Nosso objetivo é aplicar uma rede neural do tipo **Multilayer Perceptron (MLP)** para classificar registros de ocorrências policiais em duas categorias: **furto** e **roubo**, utilizando dados do estado de São Paulo.

## Integrantes

- **Hanin Atwi** — RM 567626
- **Laura Stephanie Vasquez Oliveira** — RM 567277

## Sobre o projeto

Utilizamos dados de ocorrências policiais de 2016 para desenvolver um modelo de classificação binária.

A partir dos registros selecionados, treinamos e comparamos três arquiteturas de redes neurais MLP. Com base nos resultados de validação, selecionamos a arquitetura com melhor desempenho segundo o F1-score.

Também desenvolvemos uma aplicação web com Streamlit para demonstrar a utilização do modelo treinado, permitindo inserir características de uma ocorrência e visualizar a classificação estimada.

**Classes utilizadas:**

- `0` — Furto
- `1` — Roubo

A classificação considera as seguintes categorias da coluna `RUBRICA`:

- `Furto (art. 155)`
- `Furto qualificado (art. 155, §4o.)`
- `Roubo (art. 157)`

## Fonte dos dados

Utilizamos o dataset **Crime Data in Brazil**, disponibilizado no Kaggle:

https://www.kaggle.com/datasets/inquisitivecrow/crime-data-in-brazil

Arquivo utilizado: `BO_2016.csv`

Selecionamos os registros de 2016 referentes à cidade de São Paulo, utilizando o campo `CIDADE == "S.PAULO"`.

Após a limpeza e preparação dos dados, obtivemos:

- **442.672 registros**
- **439.897 boletins de ocorrência únicos**

O pré-processamento incluiu tratamento de valores ausentes, remoção de registros com classificações conflitantes e transformação das variáveis numéricas e categóricas.

## Variáveis utilizadas

Utilizamos cinco variáveis como entrada do modelo:

| Variável | Tipo |
|---|---|
| `MES` | Numérica |
| `LATITUDE` | Numérica |
| `LONGITUDE` | Numérica |
| `CONDUTA` | Categórica |
| `NOME_DELEGACIA_CIRC` | Categórica |

A coluna `RUBRICA` foi utilizada exclusivamente para gerar a variável-alvo, evitando vazamento de dados (*data leakage*).

Após o pré-processamento, as variáveis foram transformadas em **158 características**, utilizadas como entrada da rede neural.

## Divisão dos dados

Utilizamos `StratifiedGroupKFold` para dividir os dados em três conjuntos:

| Conjunto | Registros | Proporção |
|---|---:|---:|
| Treinamento | 309.868 | 70% |
| Validação | 66.402 | 15% |
| Teste | 66.402 | 15% |

Essa estratégia permitiu manter os registros de um mesmo boletim de ocorrência no mesmo conjunto, evitando sobreposição entre treinamento, validação e teste.

## Arquiteturas MLP

Experimentamos três arquiteturas:

| Modelo | Camadas ocultas |
|---|---|
| MLP 1 | 32 neurônios |
| MLP 2 | 64 e 32 neurônios |
| MLP 3 | 128, 64 e 32 neurônios |

Utilizamos camadas ocultas com função de ativação ReLU e uma camada de saída com ativação Sigmoid, adequada para classificação binária.

A arquitetura selecionada foi a **MLP 3 (128–64–32)**, de acordo com o melhor F1-score obtido na validação.

### Configuração do treinamento

- Otimizador: Adam
- Taxa de aprendizado: 0.001
- Função de perda: Binary Crossentropy
- Batch size: 512
- Máximo de épocas: 40
- Early Stopping: paciência de 5 épocas
- Semente aleatória: 42

## Aplicação web

Desenvolvemos uma aplicação utilizando **Streamlit**, integrada ao modelo MLP treinado.

Na aplicação, é possível informar:

- Mês da ocorrência;
- Latitude;
- Longitude;
- Conduta;
- Delegacia responsável pela circunscrição.

A aplicação processa os dados com o pré-processador salvo e apresenta a classificação estimada pelo modelo, juntamente com as probabilidades de cada classe.

**Acesso à aplicação:** Local URL: http://localhost:8502
                        Network URL: http://172.16.1.208:8502

## Estrutura do repositório

```text
classificacao-ocorrencias-sp/
│
├── ClassificacaoOcorrencias_APRNC.ipynb
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── modelo/
│   ├── modelo_mlp_furto_roubo_compat.keras
│   └── preprocessor_furto_roubo.pkl
│
└── Relatorio_Tecnico_Global_Solution.pdf
```

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/haninatwi0/classificacao-ocorrencias-sp.git
```

### 2. Entrar na pasta

```bash
cd classificacao-ocorrencias-sp
```

### 3. Criar um ambiente virtual

```bash
python -m venv .venv
```

Ativar no Windows:

```bash
.venv\Scripts\activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação

```bash
streamlit run app.py
```

A aplicação será aberta no navegador, normalmente no endereço:

```text
http://localhost:8501
```

## Tecnologias utilizadas

- Python
- TensorFlow / Keras
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Dill
- Streamlit
- Google Colab
- Git e GitHub

## Limitações

O modelo foi desenvolvido para fins acadêmicos e utiliza registros históricos de 2016. Seus resultados representam uma classificação baseada nas características informadas, não uma previsão de crimes futuros.

A saída do modelo não deve ser utilizada isoladamente para decisões policiais ou operacionais. A qualidade da classificação também depende das informações disponíveis e das limitações presentes no conjunto de dados.

## Uso de inteligência artificial generativa

Utilizamos ferramentas de inteligência artificial generativa para auxiliar na identificação de erros, revisar códigos e organizar a documentação.

## Autores

**Hanin Atwi** — RM 567626  
**Laura Stephanie Vasquez Oliveira** — RM 567277

FIAP — Ciência da Computação  
Global Solution 2026 — Segurança Pública Inteligente em São Paulo
