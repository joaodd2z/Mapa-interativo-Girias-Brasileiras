#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇧🇷 Mapa Interativo de Gírias Brasileiras - Sistema de Analytics
Gerador de insights e estatísticas sobre gírias regionais brasileiras
Autor: João Lucas de Oliveira
"""

import json
import re
from typing import Dict, List, Any, Tuple
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

class GiriasAnalytics:
    """Sistema de analytics para gírias brasileiras"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.girias_file = self.base_path / "girias.json"
        
        # Regiões brasileiras
        self.regioes = {
            'Norte': ['ac', 'ap', 'am', 'pa', 'ro', 'rr', 'to'],
            'Nordeste': ['al', 'ba', 'ce', 'ma', 'pb', 'pe', 'pi', 'rn', 'se'],
            'Centro-Oeste': ['df', 'go', 'mt', 'ms'],
            'Sudeste': ['es', 'mg', 'rj', 'sp'],
            'Sul': ['pr', 'rs', 'sc']
        }
    
    def load_data(self) -> Dict[str, Any]:
        """Carrega dados do arquivo JSON"""
        with open(self.girias_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_regiao_by_estado(self, estado_codigo: str) -> str:
        """Retorna a região de um estado"""
        for regiao, estados in self.regioes.items():
            if estado_codigo in estados:
                return regiao
        return "Indefinida"
    
    def analyze_general_stats(self, data: Dict) -> Dict[str, Any]:
        """Análise de estatísticas gerais"""
        total_estados = len(data)
        total_girias = sum(len(estado.get('girias', [])) for estado in data.values())
        
        # Estatísticas por região
        stats_por_regiao = {}
        for regiao, estados in self.regioes.items():
            girias_regiao = 0
            estados_regiao = 0
            for estado_codigo in estados:
                if estado_codigo in data:
                    estados_regiao += 1
                    girias_regiao += len(data[estado_codigo].get('girias', []))
            
            stats_por_regiao[regiao] = {
                'estados': estados_regiao,
                'girias': girias_regiao,
                'media_por_estado': round(girias_regiao / max(estados_regiao, 1), 2)
            }
        
        # Estado com mais gírias
        estado_max_girias = max(data.items(), key=lambda x: len(x[1].get('girias', [])))
        
        # Estado com menos gírias
        estado_min_girias = min(data.items(), key=lambda x: len(x[1].get('girias', [])))
        
        return {
            'total_estados': total_estados,
            'total_girias': total_girias,
            'media_girias_por_estado': round(total_girias / max(total_estados, 1), 2),
            'stats_por_regiao': stats_por_regiao,
            'estado_mais_girias': {
                'codigo': estado_max_girias[0],
                'nome': estado_max_girias[1]['estado'],
                'quantidade': len(estado_max_girias[1].get('girias', []))
            },
            'estado_menos_girias': {
                'codigo': estado_min_girias[0],
                'nome': estado_min_girias[1]['estado'],
                'quantidade': len(estado_min_girias[1].get('girias', []))
            }
        }
    
    def analyze_terms_patterns(self, data: Dict) -> Dict[str, Any]:
        """Análise de padrões nos termos"""
        all_terms = []
        term_lengths = []
        
        for estado_data in data.values():
            for giria in estado_data.get('girias', []):
                termo = giria.get('termo', '')
                if termo:
                    all_terms.append(termo.lower())
                    term_lengths.append(len(termo))
        
        # Análise de comprimento
        avg_length = sum(term_lengths) / len(term_lengths) if term_lengths else 0
        
        # Termos mais comuns
        term_counter = Counter(all_terms)
        most_common_terms = term_counter.most_common(10)
        
        # Análise de caracteres/padrões
        vowels_count = sum(termo.count(v) for termo in all_terms for v in 'aeiou')
        consonants_count = sum(len(re.sub(r'[aeiou\s]', '', termo)) for termo in all_terms)
        
        # Prefixos e sufixos comuns
        prefixes = Counter([termo[:2] for termo in all_terms if len(termo) >= 2])
        suffixes = Counter([termo[-2:] for termo in all_terms if len(termo) >= 2])
        
        return {
            'total_termos': len(all_terms),
            'termos_unicos': len(set(all_terms)),
            'comprimento_medio': round(avg_length, 2),
            'comprimento_min': min(term_lengths) if term_lengths else 0,
            'comprimento_max': max(term_lengths) if term_lengths else 0,
            'termos_mais_comuns': most_common_terms,
            'proporcao_vogais': round(vowels_count / (vowels_count + consonants_count), 3) if (vowels_count + consonants_count) > 0 else 0,
            'prefixos_comuns': prefixes.most_common(5),
            'sufixos_comuns': suffixes.most_common(5)
        }
    
    def analyze_categories_contexts(self, data: Dict) -> Dict[str, Any]:
        """Análise de categorias e contextos"""
        categories = Counter()
        contexts = Counter()
        category_by_region = defaultdict(Counter)
        context_by_region = defaultdict(Counter)
        
        for estado_codigo, estado_data in data.items():
            regiao = self.get_regiao_by_estado(estado_codigo)
            
            for giria in estado_data.get('girias', []):
                categoria = giria.get('categoria', 'sem_categoria')
                contexto = giria.get('contexto', 'sem_contexto')
                
                categories[categoria] += 1
                contexts[contexto] += 1
                category_by_region[regiao][categoria] += 1
                context_by_region[regiao][contexto] += 1
        
        return {
            'categorias_populares': categories.most_common(10),
            'contextos_populares': contexts.most_common(10),
            'categorias_por_regiao': dict(category_by_region),
            'contextos_por_regiao': dict(context_by_region),
            'total_categorias': len(categories),
            'total_contextos': len(contexts)
        }
    
    def analyze_semantic_content(self, data: Dict) -> Dict[str, Any]:
        """Análise semântica do conteúdo"""
        # Palavras mais comuns nos significados
        significados_words = []
        exemplos_words = []
        
        for estado_data in data.values():
            for giria in estado_data.get('girias', []):
                significado = giria.get('significado', '').lower()
                exemplo = giria.get('exemplo', '').lower()
                
                # Limpar e extrair palavras
                sig_words = re.findall(r'\b\w+\b', significado)
                ex_words = re.findall(r'\b\w+\b', exemplo)
                
                significados_words.extend([w for w in sig_words if len(w) > 3])
                exemplos_words.extend([w for w in ex_words if len(w) > 3])
        
        # Palavras mais frequentes
        sig_counter = Counter(significados_words)
        ex_counter = Counter(exemplos_words)
        
        # Análise de sentimento (básica)
        positive_words = ['legal', 'bom', 'boa', 'bonito', 'bonita', 'feliz', 'alegre', 'querido', 'querida']
        negative_words = ['ruim', 'chato', 'feio', 'feia', 'triste', 'bravo', 'brava', 'maluco', 'maluca']
        
        positive_count = sum(significados_words.count(word) for word in positive_words)
        negative_count = sum(significados_words.count(word) for word in negative_words)
        
        return {
            'palavras_significado_comuns': sig_counter.most_common(15),
            'palavras_exemplo_comuns': ex_counter.most_common(15),
            'sentiment_analysis': {
                'positivas': positive_count,
                'negativas': negative_count,
                'neutras': len(significados_words) - positive_count - negative_count,
                'polaridade': 'positiva' if positive_count > negative_count else 'negativa' if negative_count > positive_count else 'neutra'
            }
        }
    
    def analyze_regional_uniqueness(self, data: Dict) -> Dict[str, Any]:
        """Análise de características únicas por região"""
        regional_terms = defaultdict(set)
        regional_meanings = defaultdict(list)
        
        for estado_codigo, estado_data in data.items():
            regiao = self.get_regiao_by_estado(estado_codigo)
            
            for giria in estado_data.get('girias', []):
                termo = giria.get('termo', '').lower()
                significado = giria.get('significado', '').lower()
                
                regional_terms[regiao].add(termo)
                regional_meanings[regiao].append(significado)
        
        # Termos únicos por região (não aparecem em outras)
        unique_terms_by_region = {}
        for regiao, terms in regional_terms.items():
            other_terms = set()
            for other_regiao, other_terms_set in regional_terms.items():
                if other_regiao != regiao:
                    other_terms.update(other_terms_set)
            
            unique_terms_by_region[regiao] = list(terms - other_terms)
        
        # Características semânticas por região
        regional_characteristics = {}
        for regiao, meanings in regional_meanings.items():
            all_meanings_text = ' '.join(meanings)
            words = re.findall(r'\b\w+\b', all_meanings_text)
            word_freq = Counter([w for w in words if len(w) > 3])
            
            regional_characteristics[regiao] = {
                'total_girias': len(meanings),
                'termos_unicos': len(unique_terms_by_region[regiao]),
                'palavras_caracteristicas': word_freq.most_common(5)
            }
        
        return {
            'termos_unicos_por_regiao': unique_terms_by_region,
            'caracteristicas_regionais': regional_characteristics
        }
    
    def generate_insights(self, analytics: Dict) -> List[str]:
        """Gera insights baseados nos analytics"""
        insights = []
        
        general = analytics['estatisticas_gerais']
        patterns = analytics['padroes_termos']
        categories = analytics['categorias_contextos']
        semantic = analytics['analise_semantica']
        regional = analytics['unicidade_regional']
        
        # Insights gerais
        insights.append(f"📊 O Brasil possui {general['total_girias']} gírias catalogadas em {general['total_estados']} estados")
        
        # Região mais rica
        regiao_mais_rica = max(general['stats_por_regiao'].items(), key=lambda x: x[1]['girias'])
        insights.append(f"🏆 A região {regiao_mais_rica[0]} lidera com {regiao_mais_rica[1]['girias']} gírias")
        
        # Padrões linguísticos
        if patterns['termos_mais_comuns']:
            termo_popular = patterns['termos_mais_comuns'][0]
            insights.append(f"🗣️ A gíria mais comum é '{termo_popular[0]}' (aparece {termo_popular[1]} vezes)")
        
        insights.append(f"📏 Gírias têm em média {patterns['comprimento_medio']} caracteres")
        
        # Categorias dominantes
        if categories['categorias_populares']:
            cat_popular = categories['categorias_populares'][0]
            insights.append(f"🏷️ A categoria mais comum é '{cat_popular[0]}' ({cat_popular[1]} gírias)")
        
        # Análise semântica
        sentiment = semantic['sentiment_analysis']
        insights.append(f"😊 Sentimento geral: {sentiment['polaridade']} ({sentiment['positivas']} positivas, {sentiment['negativas']} negativas)")
        
        # Diversidade regional
        total_unicos = sum(len(terms) for terms in regional['termos_unicos_por_regiao'].values())
        insights.append(f"🌍 {total_unicos} termos são únicos de suas regiões, mostrando a riqueza da diversidade brasileira")
        
        return insights
    
    def generate_report(self, analytics: Dict, insights: List[str]) -> str:
        """Gera relatório completo de analytics"""
        report = [
            "🇧🇷 RELATÓRIO DE ANALYTICS - GÍRIAS BRASILEIRAS",
            "=" * 60,
            f"📅 Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            "",
            "🧠 PRINCIPAIS INSIGHTS:",
        ]
        
        for i, insight in enumerate(insights, 1):
            report.append(f"   {i}. {insight}")
        
        report.extend([
            "",
            "📊 ESTATÍSTICAS DETALHADAS:",
            ""
        ])
        
        # Estatísticas gerais
        general = analytics['estatisticas_gerais']
        report.extend([
            "📈 VISÃO GERAL:",
            f"   • Total de Estados: {general['total_estados']}",
            f"   • Total de Gírias: {general['total_girias']}",
            f"   • Média por Estado: {general['media_girias_por_estado']}",
            f"   • Estado com mais gírias: {general['estado_mais_girias']['nome']} ({general['estado_mais_girias']['quantidade']})",
            f"   • Estado com menos gírias: {general['estado_menos_girias']['nome']} ({general['estado_menos_girias']['quantidade']})",
            ""
        ])
        
        # Por região
        report.append("🗺️ ESTATÍSTICAS POR REGIÃO:")
        for regiao, stats in general['stats_por_regiao'].items():
            report.append(f"   • {regiao}: {stats['girias']} gírias em {stats['estados']} estados (média: {stats['media_por_estado']})")
        report.append("")
        
        # Padrões de termos
        patterns = analytics['padroes_termos']
        report.extend([
            "🔤 PADRÕES LINGUÍSTICOS:",
            f"   • Total de termos: {patterns['total_termos']}",
            f"   • Termos únicos: {patterns['termos_unicos']}",
            f"   • Comprimento médio: {patterns['comprimento_medio']} caracteres",
            f"   • Proporção de vogais: {patterns['proporcao_vogais']}",
            ""
        ])
        
        # Top termos
        if patterns['termos_mais_comuns']:
            report.append("🏆 TERMOS MAIS COMUNS:")
            for termo, freq in patterns['termos_mais_comuns'][:5]:
                report.append(f"   • '{termo}': {freq} ocorrências")
            report.append("")
        
        # Categorias
        categories = analytics['categorias_contextos']
        if categories['categorias_populares']:
            report.append("🏷️ CATEGORIAS MAIS POPULARES:")
            for cat, freq in categories['categorias_populares'][:5]:
                report.append(f"   • {cat}: {freq} gírias")
            report.append("")
        
        # Contextos
        if categories['contextos_populares']:
            report.append("📋 CONTEXTOS MAIS COMUNS:")
            for ctx, freq in categories['contextos_populares'][:5]:
                report.append(f"   • {ctx}: {freq} gírias")
            report.append("")
        
        # Análise semântica
        semantic = analytics['analise_semantica']
        sentiment = semantic['sentiment_analysis']
        report.extend([
            "🎭 ANÁLISE DE SENTIMENTO:",
            f"   • Polaridade geral: {sentiment['polaridade']}",
            f"   • Gírias positivas: {sentiment['positivas']}",
            f"   • Gírias negativas: {sentiment['negativas']}",
            f"   • Gírias neutras: {sentiment['neutras']}",
            ""
        ])
        
        # Palavras mais comuns nos significados
        if semantic['palavras_significado_comuns']:
            report.append("📝 PALAVRAS MAIS COMUNS NOS SIGNIFICADOS:")
            for palavra, freq in semantic['palavras_significado_comuns'][:5]:
                report.append(f"   • '{palavra}': {freq} vezes")
            report.append("")
        
        # Uniqueness regional
        regional = analytics['unicidade_regional']
        report.append("🌍 CARACTERÍSTICAS REGIONAIS:")
        for regiao, chars in regional['caracteristicas_regionais'].items():
            report.append(f"   • {regiao}: {chars['total_girias']} gírias, {chars['termos_unicos']} termos únicos")
        
        report.extend([
            "",
            "✅ RELATÓRIO CONCLUÍDO!",
            "   Este projeto celebra a rica diversidade linguística brasileira.",
            ""
        ])
        
        return "\n".join(report)
    
    def run_analytics(self) -> str:
        """Executa análise completa"""
        print("📊 Iniciando analytics das gírias brasileiras...")
        
        try:
            data = self.load_data()
        except Exception as e:
            return f"❌ Erro ao carregar dados: {e}"
        
        # Executar todas as análises
        analytics = {
            'estatisticas_gerais': self.analyze_general_stats(data),
            'padroes_termos': self.analyze_terms_patterns(data),
            'categorias_contextos': self.analyze_categories_contexts(data),
            'analise_semantica': self.analyze_semantic_content(data),
            'unicidade_regional': self.analyze_regional_uniqueness(data)
        }
        
        # Gerar insights
        insights = self.generate_insights(analytics)
        
        # Gerar relatório
        return self.generate_report(analytics, insights)

def main():
    """Função principal"""
    try:
        analytics = GiriasAnalytics()
        report = analytics.run_analytics()
        
        # Exibir relatório
        print(report)
        
        # Salvar relatório em arquivo
        report_file = Path(__file__).parent.parent / "analytics_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Relatório de analytics salvo em: {report_file}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erro durante analytics: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 