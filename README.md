# Classificação de Ocorrências em São Paulo com MLP

Projeto desenvolvido para a **Global Solution 2026 — Segurança Pública Inteligente em São Paulo**, da disciplina de **Aprendizado Profundo com Redes Neurais Convolucionais**, na FIAP.

O objetivo é desenvolver uma rede neural do tipo **Multilayer Perceptron (MLP)** para classificar registros de ocorrências policiais da cidade de São Paulo em duas categorias: **furto e roubo**.

## Aplicação web

A aplicação utiliza o modelo MLP treinado para classificar exemplos de ocorrências a partir das características informadas pelo usuário.

**Acesse e teste a aplicação pelo navegador:**

[**Classificação de Ocorrências em São Paulo — Abrir aplicação**](https://classificacao-ocorrencias-sp.streamlit.app/)

O sistema apresenta a classe estimada pelo modelo e as probabilidades atribuídas a cada categoria.

**Importante:** o modelo classifica as características de uma ocorrência informada. Ele não prevê a possibilidade de um crime acontecer em determinado local ou horário.

## Integrantes

| Nome completo | RM |
|---|---|
| Hanin Atwi | 567626 |
| Laura Stephanie Vasquez Oliveira | 567277 |

## 1. Sobre o projeto

O projeto utiliza registros de ocorrências policiais de 2016 para desenvolver um modelo de classificação binária.

O desenvolvimento envolveu a seleção e preparação dos dados, implementação e treinamento de três arquiteturas MLP, comparação dos resultados e integração do modelo selecionado a uma aplicação web desenvolvida com Streamlit.

As classes utilizadas foram:

| Classe | Código |
|---|---:|
| Furto | 0 |
| Roubo | 1 |

A classificação foi definida com base nas categorias da coluna `RUBRICA`:

- Furto (art. 155).
- Furto qualificado (art. 155, §4º).
- Roubo (art. 157).

## 2. Fonte e seleção dos dados

**Fonte:** [Crime Data in Brazil — Kaggle](https://www.kaggle.com/datasets/inquisitivecrow/crime-data-in-brazil)

**Arquivo utilizado:** `BO_2016.csv`

Foram selecionados registros referentes ao ano de 2016 da cidade de São Paulo, utilizando o campo:

`CIDADE == "S.PAULO"`

Após a limpeza e preparação dos dados, foram obtidos:

- **442.672 registros** selecionados.
- **439.897 boletins de ocorrência únicos.**

O tratamento incluiu a análise de valores ausentes, remoção de registros com classificações conflitantes e preparação das variáveis para utilização na rede neural.

## 3. Variáveis utilizadas

Foram selecionadas cinco variáveis de entrada:

| Variável | Tipo | Justificativa |
|---|---|---|
| `MES` | Numérica | Identifica o mês da ocorrência. |
| `LATITUDE` | Numérica | Representa a localização geográfica da ocorrência. |
| `LONGITUDE` | Numérica | Complementa a informação geográfica. |
| `CONDUTA` | Categórica | Representa a conduta registrada. |
| `NOME_DELEGACIA_CIRC` | Categórica | Identifica a delegacia responsável pela circunscrição. |

A coluna `RUBRICA` foi utilizada exclusivamente para criar a variável-alvo, sem ser incluída entre as entradas da MLP. Essa separação evita o vazamento de informações (*data leakage*).

Após o pré-processamento, as cinco variáveis foram transformadas em **158 características**, utilizadas como entrada da rede neural.

## 4. Preparação e divisão dos dados

O pré-processamento envolveu:

- Tratamento de valores ausentes e inconsistentes.
- Codificação das variáveis categóricas.
- Transformação das variáveis numéricas.
- Preparação dos dados para entrada na MLP.

A divisão dos dados foi realizada utilizando `StratifiedGroupKFold`, mantendo os registros de um mesmo boletim de ocorrência no mesmo conjunto.

| Conjunto | Registros | Proporção |
|---|---:|---:|
| Treinamento | 309.868 | 70% |
| Validação | 66.402 | 15% |
| Teste | 66.402 | 15% |

O conjunto de treinamento foi utilizado para ajustar os modelos, enquanto o conjunto de validação serviu para comparar as arquiteturas e selecionar o melhor modelo.

O conjunto de teste foi reservado para a avaliação final, evitando sua utilização durante o treinamento e a seleção da arquitetura.

## 5. Implementação e arquiteturas da MLP

Foram implementadas e comparadas três arquiteturas diferentes, variando a quantidade de camadas ocultas e neurônios.

| Modelo | Arquitetura |
|---|---|
| MLP 1 | 32 neurônios |
| MLP 2 | 64 → 32 neurônios |
| MLP 3 | 128 → 64 → 32 neurônios |

As redes utilizaram:

- **Camadas ocultas:** função de ativação ReLU.
- **Camada de saída:** função de ativação Sigmoid.
- **Classificação:** binária, entre furto e roubo.

A arquitetura selecionada foi a **MLP 3 (128–64–32)**, por apresentar o melhor F1-score no conjunto de validação.

## 6. Configuração do treinamento

| Parâmetro | Configuração |
|---|---|
| Otimizador | Adam |
| Taxa de aprendizado | 0.001 |
| Função de perda | Binary Crossentropy |
| Batch size | 512 |
| Máximo de épocas | 40 |
| Early Stopping | Paciência de 5 épocas |
| Semente aleatória | 42 |

A comparação das arquiteturas considerou as seguintes métricas:

- Acurácia (*accuracy*).
- Precisão (*precision*).
- Revocação (*recall*).
- F1-score.

Os resultados comparativos, as curvas de treinamento e validação e a matriz de confusão do modelo selecionado estão documentados no notebook e no relatório técnico.

## 7. Avaliação e seleção do modelo

A seleção da arquitetura final foi baseada no desempenho apresentado durante a validação.

A **MLP 3**, com três camadas ocultas de 128, 64 e 32 neurônios, foi escolhida por apresentar o melhor F1-score nesse conjunto.

A avaliação do modelo considera:

- Acurácia.
- Precision.
- Recall.
- F1-score.
- Matriz de confusão.
- Curvas de acurácia e perda durante o treinamento e a validação.

A análise dessas métricas permite avaliar o desempenho da classificação, comparar as arquiteturas e identificar possíveis sinais de overfitting ou underfitting.

Os resultados detalhados da avaliação e a comparação entre os modelos estão disponíveis no notebook e no relatório técnico incluídos no repositório.

## 8. Aplicação web

A aplicação foi desenvolvida utilizando **Streamlit**, integrada à MLP selecionada e aos arquivos de pré-processamento salvos.

O usuário pode informar as seguintes características de uma ocorrência:

- Mês da ocorrência.
- Latitude.
- Longitude.
- Conduta.
- Delegacia responsável pela circunscrição.

Após o preenchimento do formulário, a aplicação utiliza o pré-processador salvo (`preprocessador_furto_roubo.joblib`) para transformar os dados e enviá-los ao modelo treinado.

O resultado apresenta a classificação estimada entre furto e roubo, juntamente com as probabilidades atribuídas a cada classe.

**Acesse a aplicação:** [Classificação de Ocorrências em São Paulo](https://classificacao-ocorrencias-sp.streamlit.app/)

## 9. Notebook e relatório técnico

O repositório inclui os materiais utilizados para documentar o desenvolvimento e os resultados do projeto:

- **Notebook (`classificacao-ocorrencias-sp.ipynb`):** exploração dos dados, pré-processamento, implementação e treinamento das três arquiteturas MLP, comparação de métricas, curvas de treinamento e validação e avaliação do modelo selecionado.
- **Relatório técnico (`Relatorio_Tecnico_Global_Solution.pdf`):** apresentação do problema, fonte dos dados, preparação, arquiteturas, configuração do treinamento, resultados, aplicação web, conclusões e limitações.

## 10. Estrutura do repositório

```text
classificacao-ocorrencias-sp/
│
├── modelo/
│   ├── modelo_mlp_furto_roubo_compat.keras
│   └── preprocessador_furto_roubo.joblib
│
├── app.py
├── requirements.txt
├── classificacao-ocorrencias-sp.ipynb
├── Relatorio_Tecnico_Global_Solution.pdf
├── README.md
└── .gitignore
```

## 11. Como executar o projeto localmente

### Pré-requisitos

- Python 3.13.
- pip.
- Git.

### 1. Clonar o repositório

```bash
git clone https://github.com/haninatwi0/classificacao-ocorrencias-sp.git
```

### 2. Entrar na pasta do projeto

```bash
cd classificacao-ocorrencias-sp
```

### 3. Criar um ambiente virtual

```bash
python -m venv .venv
```

Para ativar no Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação

```bash
streamlit run app.py
```

A aplicação será disponibilizada no navegador, normalmente no endereço:

`http://localhost:8501`

## 12. Tecnologias utilizadas

- Python.
- TensorFlow / Keras.
- Pandas.
- NumPy.
- Scikit-learn.
- Joblib.
- Dill.
- Streamlit.
- Google Colab.
- Git e GitHub.

## 13. Limitações e considerações

O modelo foi desenvolvido para fins acadêmicos, utilizando registros históricos de 2016 referentes à cidade de São Paulo.

Sua finalidade é classificar uma ocorrência com base nas características informadas, identificando se o registro é mais compatível com furto ou roubo.

O modelo não prevê crimes futuros, não calcula o risco de ocorrência de crimes em determinada região ou horário e não deve ser utilizado isoladamente para decisões policiais ou operacionais.

Os resultados também dependem da qualidade, da representatividade e das limitações dos dados utilizados durante o treinamento.

## 14. Uso de inteligência artificial generativa

Foram utilizadas ferramentas de inteligência artificial generativa como apoio durante o desenvolvimento, principalmente para:

- Auxiliar na identificação e correção de erros no código.
- Apoiar a organização e a documentação do projeto.

As decisões sobre a preparação dos dados, treinamento, comparação das arquiteturas e seleção do modelo foram revisadas pela equipe, que é responsável pela compreensão e validação da solução.

---

**FIAP — Ciência da Computação**

**Global Solution 2026 — Segurança Pública Inteligente em São Paulo**

Disciplina: Aprendizado Profundo com Redes Neurais Convolucionais
