#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇧🇷 Mapa Interativo de Gírias Brasileiras - Sistema de Atualização
Sistema Python para enriquecer e validar dados das gírias regionais
Autor: João Lucas de Oliveira
"""

import json
import re
import random
from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Giria:
    termo: str
    significado: str
    exemplo: str
    contexto: str = "informal"
    frequencia: str = "comum"
    origem: str = ""
    sinonimos: List[str] = None
    categoria: str = "expressão"

class GiriasUpdater:
    """Sistema inteligente para atualização e validação de gírias brasileiras"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.girias_file = self.base_path / "girias.json"
        
        # Base expandida de gírias autênticas por estado
        self.new_girias_data = {
            "ac": {
                "estado": "Acre",
                "girias": [
                    {"termo": "gaiato", "significado": "pessoa engraçada, brincalhona", "exemplo": "Esse cara é muito gaiato, sempre fazendo piada!", "contexto": "informal", "categoria": "personalidade"},
                    {"termo": "cabra macho", "significado": "homem corajoso, valente", "exemplo": "Aquele cabra macho enfrentou a onça sozinho.", "contexto": "regional", "categoria": "qualidade"},
                    {"termo": "manauara", "significado": "pessoa de Manaus, amazônico", "exemplo": "Sou manauara de coração!", "contexto": "identidade", "categoria": "gentílico"},
                    {"termo": "beiradeiro", "significado": "pessoa que mora nas margens dos rios", "exemplo": "Os beiradeiros conhecem todos os segredos da floresta.", "contexto": "regional", "categoria": "profissão"},
                    {"termo": "encalacrado", "significado": "pessoa em situação difícil", "exemplo": "Fiquei encalacrado sem dinheiro na cidade.", "contexto": "informal", "categoria": "situação"},
                    {"termo": "piracema", "significado": "época de reprodução dos peixes", "exemplo": "Na piracema não pode pescar.", "contexto": "técnico", "categoria": "natureza"},
                    {"termo": "colocação", "significado": "área de trabalho do seringueiro", "exemplo": "Minha colocação fica rio acima.", "contexto": "regional", "categoria": "local"},
                    {"termo": "estrada de seringa", "significado": "caminho entre seringueiras", "exemplo": "Saiu cedo para correr a estrada de seringa.", "contexto": "histórico", "categoria": "trabalho"}
                ]
            },
            "al": {
                "estado": "Alagoas",
                "girias": [
                    {"termo": "oxente", "significado": "expressão de espanto ou surpresa", "exemplo": "Oxente, que história é essa?", "contexto": "informal", "categoria": "interjeição"},
                    {"termo": "massa", "significado": "legal, bacana", "exemplo": "Essa festa tá massa demais!", "contexto": "gíria jovem", "categoria": "aprovação"},
                    {"termo": "aperreado", "significado": "pessoa preocupada, aflita", "exemplo": "Tô aperreado com essa situação.", "contexto": "informal", "categoria": "sentimento"},
                    {"termo": "bichinho", "significado": "pessoa querida", "exemplo": "Que bichinho mais fofo!", "contexto": "carinhoso", "categoria": "afeto"},
                    {"termo": "cabra da peste", "significado": "pessoa esperta, danada", "exemplo": "Esse menino é um cabra da peste mesmo.", "contexto": "regional", "categoria": "personalidade"},
                    {"termo": "brutamonte", "significado": "muito grande, imenso", "exemplo": "Uma casa brutamonte de bonita!", "contexto": "intensificador", "categoria": "tamanho"},
                    {"termo": "arigó", "significado": "pessoa não muito inteligente", "exemplo": "Não seja arigó, rapaz!", "contexto": "pejorativo", "categoria": "personalidade"},
                    {"termo": "sem eira nem beira", "significado": "pessoa sem recursos", "exemplo": "Ficou sem eira nem beira depois da seca.", "contexto": "regional", "categoria": "situação"}
                ]
            },
            "sp": {
                "estado": "São Paulo",
                "girias": [
                    {"termo": "mano", "significado": "amigo, parceiro", "exemplo": "E aí, mano, beleza?", "contexto": "informal", "categoria": "tratamento"},
                    {"termo": "bagulho", "significado": "coisa, objeto", "exemplo": "Pega aquele bagulho pra mim.", "contexto": "gíria urbana", "categoria": "objeto"},
                    {"termo": "trampo", "significado": "trabalho, emprego", "exemplo": "Hoje tenho trampo até tarde.", "contexto": "informal", "categoria": "trabalho"},
                    {"termo": "mó", "significado": "muito, mega", "exemplo": "Esse filme é mó legal!", "contexto": "gíria jovem", "categoria": "intensificador"},
                    {"termo": "paulista", "significado": "pessoa de SP", "exemplo": "Todo paulista é corrido.", "contexto": "identidade", "categoria": "gentílico"},
                    {"termo": "rolê", "significado": "passeio, programa", "exemplo": "Vamos dar um rolê no centro?", "contexto": "gíria jovem", "categoria": "atividade"},
                    {"termo": "quebrada", "significado": "bairro, região", "exemplo": "Lá na minha quebrada é diferente.", "contexto": "gíria urbana", "categoria": "local"},
                    {"termo": "sinistro", "significado": "legal, maneiro", "exemplo": "Essa festa tá sinistra!", "contexto": "gíria jovem", "categoria": "aprovação"},
                    {"termo": "paia", "significado": "chato, ruim", "exemplo": "Que paia esse trânsito.", "contexto": "informal", "categoria": "desaprovação"},
                    {"termo": "paulistano", "significado": "pessoa da capital", "exemplo": "Paulistano vive correndo.", "contexto": "identidade", "categoria": "gentílico"},
                    {"termo": "maloqueiro", "significado": "pessoa da periferia", "exemplo": "Maloqueiro de coração!", "contexto": "identidade", "categoria": "social"},
                    {"termo": "zé povinho", "significado": "pessoa comum do povo", "exemplo": "Sou zé povinho mesmo.", "contexto": "popular", "categoria": "social"},
                    {"termo": "corujão", "significado": "programa noturno, pessoa que sai à noite", "exemplo": "Hoje tem corujão no cinema.", "contexto": "informal", "categoria": "atividade"},
                    {"termo": "embaçado", "significado": "complicado, difícil", "exemplo": "A situação tá embaçada.", "contexto": "gíria urbana", "categoria": "situação"},
                    {"termo": "desenrolo", "significado": "jeitinho, habilidade para resolver", "exemplo": "Ele tem um bom desenrolo.", "contexto": "informal", "categoria": "habilidade"}
                ]
            },
            "rj": {
                "estado": "Rio de Janeiro",
                "girias": [
                    {"termo": "mermão", "significado": "irmão, parceiro", "exemplo": "Caraca, mermão, que doideira!", "contexto": "informal", "categoria": "tratamento"},
                    {"termo": "maneiro", "significado": "legal, bacana", "exemplo": "Esse filme tá maneiro demais!", "contexto": "carioca", "categoria": "aprovação"},
                    {"termo": "parada", "significado": "coisa, situação", "exemplo": "Essa parada tá estranha.", "contexto": "gíria urbana", "categoria": "situação"},
                    {"termo": "vacilo", "significado": "erro, besteira", "exemplo": "Foi um vacilo eu não ter ido.", "contexto": "informal", "categoria": "erro"},
                    {"termo": "carioca", "significado": "pessoa do Rio de Janeiro", "exemplo": "Todo carioca ama a praia.", "contexto": "identidade", "categoria": "gentílico"},
                    {"termo": "galera", "significado": "pessoal, turma", "exemplo": "A galera tá chegando na praia.", "contexto": "informal", "categoria": "grupo"},
                    {"termo": "papo", "significado": "conversa", "exemplo": "Que papo é esse, cara?", "contexto": "informal", "categoria": "comunicação"},
                    {"termo": "mandar brasa", "significado": "ir com tudo", "exemplo": "Vou mandar brasa nessa festa!", "contexto": "informal", "categoria": "ação"},
                    {"termo": "zona sul", "significado": "região nobre do Rio", "exemplo": "Vamos na zona sul hoje?", "contexto": "geográfico", "categoria": "local"},
                    {"termo": "malandro", "significado": "pessoa esperta", "exemplo": "Esse malandro sabe se virar.", "contexto": "cultural", "categoria": "personalidade"},
                    {"termo": "otário", "significado": "pessoa ingênua", "exemplo": "Não seja otário, cara.", "contexto": "pejorativo", "categoria": "personalidade"},
                    {"termo": "barra pesada", "significado": "situação difícil", "exemplo": "A situação tá barra pesada.", "contexto": "informal", "categoria": "situação"},
                    {"termo": "zoação", "significado": "brincadeira, bagunça", "exemplo": "Isso é só zoação.", "contexto": "informal", "categoria": "diversão"},
                    {"termo": "ralé", "significado": "classe baixa", "exemplo": "Somos ralé mesmo.", "contexto": "social", "categoria": "classe"}
                ]
            },
            "ba": {
                "estado": "Bahia",
                "girias": [
                    {"termo": "axé", "significado": "energia positiva, força", "exemplo": "Muito axé pra você hoje!", "contexto": "religioso-cultural", "categoria": "energia"},
                    {"termo": "arretado", "significado": "legal, bacana, incrível", "exemplo": "Essa música é arretada demais!", "contexto": "regional", "categoria": "aprovação"},
                    {"termo": "bichinho", "significado": "pessoa querida, fofa", "exemplo": "Que bichinho mais fofo esse menino!", "contexto": "carinhoso", "categoria": "afeto"},
                    {"termo": "danado", "significado": "esperto, travesso", "exemplo": "Esse menino é muito danado mesmo.", "contexto": "informal", "categoria": "personalidade"},
                    {"termo": "peba", "significado": "ruim, de baixa qualidade", "exemplo": "Esse filme é muito peba.", "contexto": "informal", "categoria": "qualidade"},
                    {"termo": "avexado", "significado": "apressado, com pressa", "exemplo": "Para de ficar avexado, rapaz!", "contexto": "regional", "categoria": "comportamento"},
                    {"termo": "égua", "significado": "expressão de espanto", "exemplo": "Égua, que susto!", "contexto": "interjeição", "categoria": "surpresa"},
                    {"termo": "mainha", "significado": "mãe", "exemplo": "Mainha fez um almoço arretado.", "contexto": "familiar", "categoria": "família"},
                    {"termo": "painho", "significado": "pai", "exemplo": "Painho chegou do trabalho.", "contexto": "familiar", "categoria": "família"},
                    {"termo": "aloprado", "significado": "doido, maluco", "exemplo": "Esse cara é aloprado mesmo.", "contexto": "informal", "categoria": "personalidade"},
                    {"termo": "cafuçu", "significado": "caipira, interiorano", "exemplo": "Sou cafuçu do sertão.", "contexto": "identidade", "categoria": "origem"},
                    {"termo": "xodó", "significado": "pessoa querida, favorita", "exemplo": "Você é meu xodó.", "contexto": "carinhoso", "categoria": "afeto"}
                ]
            }
        }
        
    def load_current_data(self) -> Dict[str, Any]:
        """Carrega dados atuais do arquivo JSON"""
        try:
            with open(self.girias_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def validate_giria(self, giria: Dict[str, str]) -> bool:
        """Valida se uma gíria tem todos os campos necessários"""
        required_fields = ['termo', 'significado', 'exemplo']
        return all(field in giria and giria[field].strip() for field in required_fields)
    
    def enrich_giria(self, giria: Dict[str, str]) -> Dict[str, str]:
        """Enriquece uma gíria com metadados adicionais"""
        enriched = giria.copy()
        
        # Adicionar contexto se não existir
        if 'contexto' not in enriched:
            enriched['contexto'] = self.determine_context(giria['termo'])
        
        # Adicionar categoria se não existir
        if 'categoria' not in enriched:
            enriched['categoria'] = self.determine_category(giria['termo'], giria['significado'])
        
        # Adicionar frequência de uso
        if 'frequencia' not in enriched:
            enriched['frequencia'] = self.determine_frequency(giria['termo'])
        
        return enriched
    
    def determine_context(self, termo: str) -> str:
        """Determina o contexto de uso de uma gíria"""
        contexts = {
            'interjeição': ['oxente', 'eita', 'égua', 'bah', 'uai'],
            'familiar': ['mainha', 'painho', 'vovô', 'vovó'],
            'gíria jovem': ['mó', 'sinistro', 'paia', 'rolê'],
            'regional': ['arretado', 'cabra', 'tchê', 'sô'],
            'urbano': ['bagulho', 'trampo', 'quebrada', 'parada']
        }
        
        for context, terms in contexts.items():
            if any(term in termo.lower() for term in terms):
                return context
        
        return 'informal'
    
    def determine_category(self, termo: str, significado: str) -> str:
        """Determina a categoria de uma gíria baseada no significado"""
        categories = {
            'tratamento': ['amigo', 'parceiro', 'cara', 'mano'],
            'aprovação': ['legal', 'bacana', 'bom', 'massa'],
            'personalidade': ['esperto', 'danado', 'esperta', 'malandro'],
            'sentimento': ['preocupado', 'aflito', 'feliz', 'triste'],
            'local': ['bairro', 'região', 'lugar', 'cidade']
        }
        
        significado_lower = significado.lower()
        for category, keywords in categories.items():
            if any(keyword in significado_lower for keyword in keywords):
                return category
        
        return 'expressão'
    
    def determine_frequency(self, termo: str) -> str:
        """Determina a frequência de uso estimada"""
        common_terms = ['mano', 'cara', 'legal', 'massa', 'bom']
        if any(term in termo.lower() for term in common_terms):
            return 'muito comum'
        return 'comum'
    
    def merge_data(self, current_data: Dict, new_data: Dict) -> Dict:
        """Mescla dados existentes com novos dados"""
        merged = current_data.copy()
        
        for estado_code, estado_data in new_data.items():
            if estado_code not in merged:
                merged[estado_code] = estado_data
            else:
                # Manter o nome do estado
                merged[estado_code]['estado'] = estado_data['estado']
                
                # Mesclar gírias
                existing_terms = {g['termo'].lower() for g in merged[estado_code].get('girias', [])}
                
                for new_giria in estado_data['girias']:
                    if new_giria['termo'].lower() not in existing_terms:
                        merged[estado_code].setdefault('girias', []).append(new_giria)
                    else:
                        # Atualizar gíria existente com novos campos
                        for i, existing_giria in enumerate(merged[estado_code]['girias']):
                            if existing_giria['termo'].lower() == new_giria['termo'].lower():
                                merged[estado_code]['girias'][i] = {**existing_giria, **new_giria}
                                break
        
        return merged
    
    def add_statistics(self, data: Dict) -> Dict:
        """Adiciona estatísticas aos dados"""
        for estado_code, estado_data in data.items():
            girias = estado_data.get('girias', [])
            estado_data['estatisticas'] = {
                'total_girias': len(girias),
                'categorias': self.count_categories(girias),
                'contextos': self.count_contexts(girias),
                'ultima_atualizacao': '2025-01-02'
            }
        
        return data
    
    def count_categories(self, girias: List[Dict]) -> Dict[str, int]:
        """Conta gírias por categoria"""
        categories = {}
        for giria in girias:
            cat = giria.get('categoria', 'expressão')
            categories[cat] = categories.get(cat, 0) + 1
        return categories
    
    def count_contexts(self, girias: List[Dict]) -> Dict[str, int]:
        """Conta gírias por contexto"""
        contexts = {}
        for giria in girias:
            ctx = giria.get('contexto', 'informal')
            contexts[ctx] = contexts.get(ctx, 0) + 1
        return contexts
    
    def save_data(self, data: Dict) -> None:
        """Salva dados atualizados no arquivo JSON"""
        with open(self.girias_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def update(self) -> None:
        """Executa processo completo de atualização"""
        print("🇧🇷 Iniciando atualização das gírias brasileiras...")
        
        # Carregar dados atuais
        current_data = self.load_current_data()
        print(f"📊 Dados atuais carregados: {len(current_data)} estados")
        
        # Enriquecer dados existentes
        for estado_code, estado_data in current_data.items():
            if 'girias' in estado_data:
                for i, giria in enumerate(estado_data['girias']):
                    current_data[estado_code]['girias'][i] = self.enrich_giria(giria)
        
        # Mesclar com novos dados
        merged_data = self.merge_data(current_data, self.new_girias_data)
        print(f"🔄 Dados mesclados: {len(merged_data)} estados")
        
        # Adicionar estatísticas
        final_data = self.add_statistics(merged_data)
        
        # Salvar dados atualizados
        self.save_data(final_data)
        
        # Estatísticas finais
        total_girias = sum(len(estado['girias']) for estado in final_data.values())
        print(f"✅ Atualização concluída!")
        print(f"📈 Total de gírias: {total_girias}")
        print(f"🗺️ Estados cobertos: {len(final_data)}")
        print(f"💾 Arquivo salvo: {self.girias_file}")

def main():
    """Função principal"""
    try:
        updater = GiriasUpdater()
        updater.update()
    except Exception as e:
        print(f"❌ Erro durante atualização: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 