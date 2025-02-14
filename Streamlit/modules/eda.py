import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

@st.cache_data
def exploratory_data_analysis(df):
    st.header("📊 Análise Exploratória dos Dados")
    
    # Seção 1.1: Estrutura do Dataset
    with st.expander("📁 **Estrutura do Dataset**", expanded=False):
        st.markdown("""
        ### ❓ **Perguntas-chave**  
        - Quantas observações e variáveis temos?  
        - Como são os primeiros registros?  
        - Quais tipos de dados estamos lidando?  
        - Existem valores ausentes?  
        """)
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("#### 🔍 **Amostra dos Dados:**")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            st.dataframe(df[numeric_cols].head().style.format("{:.2f}"), height=250)
        with col2:
            st.markdown("#### 📊 **Total de Observações**")
            st.metric("📊 Total de Registros", df.shape[0])
            st.metric("📂 Total de Variáveis", df.shape[1])
        with col3:
            st.markdown("#### 🛠 **Tipos de Dados:**")
            dtype_counts = df.dtypes.value_counts().reset_index()
            dtype_counts.columns = ['Tipo', 'Contagem']
            st.dataframe(dtype_counts, hide_index=True)
    
    # Seção 1.2: Distribuição das Notas Fiscais
    with st.expander("🧾 **Distribuição das Notas Fiscais**", expanded=False):
        st.markdown("""
        ### ❓ **Perguntas-chave**  
        - Como as notas fiscais estão distribuídas entre válidas e inválidas?  
        - Qual a porcentagem de cada classe?  
        """)
        st.markdown("### 📊 **Distribuição das Notas Fiscais**")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.countplot(x='class_label', data=df, order=['valid', 'not valid'], ax=ax)
        ax.set_title('Distribuição de Notas Fiscais Válidas vs. Inválidas', fontsize=14)
        ax.set_xlabel('Classificação')
        ax.set_ylabel('Contagem')
        total = len(df)
        for p in ax.patches:
            percentage = f'{100 * p.get_height()/total:.1f}%'
            x = p.get_x() + p.get_width() / 2
            y = p.get_height() + 10
            ax.annotate(percentage, (x, y), ha='center')
        st.pyplot(fig)
    
    # Seção 1.3: Análise das Variáveis Numéricas
    with st.expander("📊 **Distribuição das Variáveis Numéricas**", expanded=False):
        col1, col2 = st.columns([0.9, 1])
        with col1:
            st.markdown("""
            ### ❓ **Perguntas-chave**  
            - Quais são os valores principais das variáveis numéricas?  
            - Existem outliers nas taxas de impostos?  
            """)
            numeric_cols = [
                'calculated_value', 'iss_tax_rate', 'inss_tax_rate',
                'csll_tax_rate', 'ir_tax_rate', 'cofins_tax_rate', 'pis_tax_rate'
            ]
            st.markdown("### 📌 **Estatísticas Descritivas**")
            st.dataframe(df[numeric_cols].describe().T.style.format("{:.2f}"))
        with col2:
            st.markdown("### 📉 **Outliers nas Taxas de Impostos**")
            fig, ax = plt.subplots(figsize=(12, 6))
            tax_cols = [col for col in numeric_cols if 'tax_rate' in col]
            sns.boxplot(data=df[tax_cols], orient='h', ax=ax)
            ax.set_title('Distribuição das Taxas de Impostos', fontsize=14)
            ax.set_xlabel('Valor (%)')
            st.pyplot(fig)
    
    # Seção 1.4: Distribuição das Variáveis Categóricas
    with st.expander("🏷️ **Distribuição das Variáveis Categóricas**", expanded=False):
        col1, col2 = st.columns([0.9, 1])
        with col1:
            st.markdown("""
            ### ❓ **Perguntas-chave**  
            - Como as notas fiscais estão distribuídas por estado?  
            - Existe alguma relação entre o estado e a validade da nota?  
            """)
        with col2:
            st.markdown("### 📌 **Distribuição das Notas por Estado**")
            fig, ax = plt.subplots(figsize=(12, 6))
            order = df['state'].value_counts().index
            sns.countplot(x='state', hue='class_label', data=df, order=order, ax=ax)
            ax.set_title('Validade das Notas por Estado', fontsize=14)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            ax.legend(title='Status')
            st.pyplot(fig)
    
    # # Seção 1.5: Análise Temporal
    # with st.expander("📆 **Análise Temporal**", expanded=False):
    #     col1, col2 = st.columns([0.9, 1])
    #     with col1:
    #         st.markdown("""
    #         ### ❓ **Perguntas-chave**  
    #         - Como as notas válidas e inválidas evoluíram ao longo do tempo?  
    #         """)
    #     with col2:
    #         df['issue_date'] = pd.to_datetime(df['issue_date'])
    #         df['ano'] = df['issue_date'].dt.year
    #         df['mes'] = df['issue_date'].dt.month
    #         invalid_notes = df[df['class_label'] == 'not valid'].groupby(['ano', 'mes']).size().reset_index(name='count')
    #         valid_notes = df[df['class_label'] == 'valid'].groupby(['ano', 'mes']).size().reset_index(name='count')
    #         st.markdown("### 📈 **Evolução Mensal de Notas Válidas e Inválidas**")
    #         fig, ax = plt.subplots(figsize=(14, 6))
    #         sns.lineplot(data=invalid_notes, x='mes', y='count', hue='ano', marker='o', ax=ax)
    #         sns.lineplot(data=valid_notes, x='mes', y='count', hue='ano', marker='o', ax=ax)
    #         ax.set_title('Evolução Mensal de Notas Válidas vs. Inválidas', fontsize=14)
    #         ax.set_xlabel('Mês')
    #         ax.set_ylabel('Quantidade de Notas')
    #         ax.legend(title='Ano', labels=['Inválidas', 'Válidas'])
    #         st.pyplot(fig)
    
    # Seção 1.6: Matriz de Correlação
    with st.expander("🔗 **Matriz de Correlação entre Variáveis**", expanded=False):
        col1, col2 = st.columns([0.9, 1])
        with col1:
            st.markdown("""
            ### ❓ **Perguntas-chave**  
            - Como as variáveis numéricas estão correlacionadas entre si?  
            """)
        with col2:
            df_corr = df.copy()
            le = LabelEncoder()
            df_corr['class_label'] = le.fit_transform(df_corr['class_label'])
            st.markdown("### 📊 **Matriz de Correlação entre Variáveis Numéricas**")
            fig, ax = plt.subplots(figsize=(14, 10))
            corr_matrix = df_corr[numeric_cols + ['class_label']].corr()
            sns.heatmap(
                corr_matrix, annot=True, cmap='coolwarm', fmt=".2f",
                mask=np.triu(np.ones_like(corr_matrix, dtype=bool)), ax=ax
            )
            ax.set_title('Matriz de Correlação entre Variáveis Numéricas', fontsize=14)
            st.pyplot(fig)