#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇧🇷 Mapa Interativo de Gírias Brasileiras - Sistema de Validação
Validador inteligente para garantir qualidade dos dados das gírias
Autor: João Lucas de Oliveira
"""

import json
import re
import unicodedata
from typing import Dict, List, Tuple, Any
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]

class GiriasValidator:
    """Sistema inteligente de validação de gírias brasileiras"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.girias_file = self.base_path / "girias.json"
        
        # Estados brasileiros válidos
        self.valid_estados = {
            'ac': 'Acre', 'al': 'Alagoas', 'ap': 'Amapá', 'am': 'Amazonas',
            'ba': 'Bahia', 'ce': 'Ceará', 'df': 'Distrito Federal', 'es': 'Espírito Santo',
            'go': 'Goiás', 'ma': 'Maranhão', 'mt': 'Mato Grosso', 'ms': 'Mato Grosso do Sul',
            'mg': 'Minas Gerais', 'pa': 'Pará', 'pb': 'Paraíba', 'pr': 'Paraná',
            'pe': 'Pernambuco', 'pi': 'Piauí', 'rj': 'Rio de Janeiro', 'rn': 'Rio Grande do Norte',
            'rs': 'Rio Grande do Sul', 'ro': 'Rondônia', 'rr': 'Roraima',
            'sc': 'Santa Catarina', 'sp': 'São Paulo', 'se': 'Sergipe', 'to': 'Tocantins'
        }
        
        # Palavras ofensivas ou inadequadas
        self.inappropriate_words = [
            'palavrão1', 'palavrão2'  # Lista básica - expandir conforme necessário
        ]
        
        # Contextos válidos
        self.valid_contexts = [
            'informal', 'formal', 'regional', 'gíria jovem', 'familiar',
            'religioso-cultural', 'técnico', 'histórico', 'identidade',
            'carinhoso', 'pejorativo', 'interjeição', 'urbano', 'rural'
        ]
        
        # Categorias válidas
        self.valid_categories = [
            'tratamento', 'aprovação', 'desaprovação', 'personalidade', 'sentimento',
            'local', 'atividade', 'objeto', 'trabalho', 'família', 'comida',
            'natureza', 'qualidade', 'situação', 'expressão', 'interjeição',
            'gentílico', 'profissão', 'social', 'classe', 'energia', 'erro',
            'comunicação', 'ação', 'grupo', 'diversão', 'origem', 'afeto',
            'comportamento', 'surpresa', 'habilidade', 'tamanho'
        ]
    
    def load_data(self) -> Dict[str, Any]:
        """Carrega dados do arquivo JSON"""
        try:
            with open(self.girias_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {self.girias_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido: {e}")
    
    def normalize_text(self, text: str) -> str:
        """Normaliza texto removendo acentos e convertendo para minúsculas"""
        return unicodedata.normalize('NFKD', text.lower()).encode('ascii', 'ignore').decode()
    
    def validate_estado_structure(self, codigo: str, data: Dict) -> ValidationResult:
        """Valida estrutura de um estado"""
        errors = []
        warnings = []
        suggestions = []
        
        # Verificar código do estado
        if codigo not in self.valid_estados:
            errors.append(f"Código de estado inválido: {codigo}")
        
        # Verificar se tem campo 'estado'
        if 'estado' not in data:
            errors.append(f"Campo 'estado' obrigatório ausente para {codigo}")
        elif data['estado'] != self.valid_estados.get(codigo, ''):
            warnings.append(f"Nome do estado inconsistente para {codigo}: esperado '{self.valid_estados.get(codigo)}', encontrado '{data['estado']}'")
        
        # Verificar se tem campo 'girias'
        if 'girias' not in data:
            errors.append(f"Campo 'girias' obrigatório ausente para {codigo}")
        elif not isinstance(data['girias'], list):
            errors.append(f"Campo 'girias' deve ser uma lista para {codigo}")
        elif len(data['girias']) == 0:
            warnings.append(f"Estado {codigo} não possui gírias cadastradas")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions
        )
    
    def validate_giria_structure(self, giria: Dict, estado_codigo: str) -> ValidationResult:
        """Valida estrutura de uma gíria"""
        errors = []
        warnings = []
        suggestions = []
        
        # Campos obrigatórios
        required_fields = ['termo', 'significado', 'exemplo']
        for field in required_fields:
            if field not in giria:
                errors.append(f"Campo obrigatório '{field}' ausente em gíria do estado {estado_codigo}")
            elif not giria[field] or not giria[field].strip():
                errors.append(f"Campo '{field}' vazio em gíria do estado {estado_codigo}")
        
        if errors:  # Se há erros estruturais, não continuar validação
            return ValidationResult(False, errors, warnings, suggestions)
        
        # Validar conteúdo dos campos
        termo = giria['termo'].strip()
        significado = giria['significado'].strip()
        exemplo = giria['exemplo'].strip()
        
        # Validar termo
        if len(termo) < 2:
            errors.append(f"Termo muito curto: '{termo}' no estado {estado_codigo}")
        elif len(termo) > 50:
            warnings.append(f"Termo muito longo: '{termo}' no estado {estado_codigo}")
        
        # Verificar caracteres especiais no termo
        if re.search(r'[^\w\s\-]', termo):
            warnings.append(f"Termo contém caracteres especiais: '{termo}' no estado {estado_codigo}")
        
        # Validar significado
        if len(significado) < 5:
            errors.append(f"Significado muito curto para '{termo}' no estado {estado_codigo}")
        elif len(significado) > 200:
            warnings.append(f"Significado muito longo para '{termo}' no estado {estado_codigo}")
        
        # Validar exemplo
        if len(exemplo) < 10:
            errors.append(f"Exemplo muito curto para '{termo}' no estado {estado_codigo}")
        elif len(exemplo) > 300:
            warnings.append(f"Exemplo muito longo para '{termo}' no estado {estado_codigo}")
        
        # Verificar se o termo aparece no exemplo
        if termo.lower() not in exemplo.lower():
            suggestions.append(f"Termo '{termo}' não aparece no exemplo. Considere incluí-lo para maior clareza.")
        
        # Validar campos opcionais
        if 'contexto' in giria and giria['contexto'] not in self.valid_contexts:
            warnings.append(f"Contexto inválido '{giria['contexto']}' para '{termo}'. Contextos válidos: {', '.join(self.valid_contexts)}")
        
        if 'categoria' in giria and giria['categoria'] not in self.valid_categories:
            warnings.append(f"Categoria inválida '{giria['categoria']}' para '{termo}'. Categorias válidas: {', '.join(self.valid_categories)}")
        
        # Verificar palavras inadequadas
        all_text = f"{termo} {significado} {exemplo}".lower()
        for word in self.inappropriate_words:
            if word in all_text:
                errors.append(f"Conteúdo inadequado detectado em '{termo}' no estado {estado_codigo}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions
        )
    
    def check_duplicates(self, data: Dict) -> ValidationResult:
        """Verifica gírias duplicadas entre estados"""
        errors = []
        warnings = []
        suggestions = []
        
        all_terms = {}  # termo_normalizado -> [(estado, termo_original)]
        
        for estado_codigo, estado_data in data.items():
            if 'girias' not in estado_data:
                continue
                
            for giria in estado_data['girias']:
                if 'termo' not in giria:
                    continue
                    
                termo_normalizado = self.normalize_text(giria['termo'])
                termo_original = giria['termo']
                
                if termo_normalizado in all_terms:
                    all_terms[termo_normalizado].append((estado_codigo, termo_original))
                else:
                    all_terms[termo_normalizado] = [(estado_codigo, termo_original)]
        
        # Verificar duplicatas
        for termo_normalizado, occurrences in all_terms.items():
            if len(occurrences) > 1:
                estados_list = [f"{occ[1]} ({occ[0]})" for occ in occurrences]
                warnings.append(f"Termo duplicado: {' | '.join(estados_list)}")
        
        return ValidationResult(True, errors, warnings, suggestions)
    
    def validate_statistics(self, data: Dict) -> ValidationResult:
        """Valida estatísticas dos dados"""
        errors = []
        warnings = []
        suggestions = []
        
        total_estados = len(data)
        total_girias = 0
        estados_sem_girias = []
        
        for estado_codigo, estado_data in data.items():
            girias = estado_data.get('girias', [])
            if len(girias) == 0:
                estados_sem_girias.append(estado_codigo)
            total_girias += len(girias)
        
        # Verificações estatísticas
        if total_estados < 27:
            warnings.append(f"Apenas {total_estados} estados cadastrados. Brasil tem 27 unidades federativas.")
        
        if total_girias < 100:
            warnings.append(f"Apenas {total_girias} gírias cadastradas. Considere expandir a base de dados.")
        
        if estados_sem_girias:
            warnings.append(f"Estados sem gírias: {', '.join(estados_sem_girias)}")
        
        # Sugestões baseadas em estatísticas
        media_girias = total_girias / total_estados if total_estados > 0 else 0
        if media_girias < 5:
            suggestions.append("Considere adicionar mais gírias por estado para enriquecer o conteúdo.")
        
        return ValidationResult(True, errors, warnings, suggestions)
    
    def generate_report(self, results: List[Tuple[str, ValidationResult]]) -> str:
        """Gera relatório completo de validação"""
        report = ["🇧🇷 RELATÓRIO DE VALIDAÇÃO - GÍRIAS BRASILEIRAS", "=" * 60, ""]
        
        total_errors = sum(len(result.errors) for _, result in results)
        total_warnings = sum(len(result.warnings) for _, result in results)
        total_suggestions = sum(len(result.suggestions) for _, result in results)
        
        # Resumo
        report.extend([
            "📊 RESUMO:",
            f"   ✅ Status: {'APROVADO' if total_errors == 0 else 'COM PROBLEMAS'}",
            f"   ❌ Erros: {total_errors}",
            f"   ⚠️  Avisos: {total_warnings}",
            f"   💡 Sugestões: {total_suggestions}",
            ""
        ])
        
        # Detalhes por seção
        for section_name, result in results:
            if result.errors or result.warnings or result.suggestions:
                report.append(f"📋 {section_name.upper()}:")
                
                if result.errors:
                    report.append("   ❌ ERROS:")
                    for error in result.errors:
                        report.append(f"      • {error}")
                
                if result.warnings:
                    report.append("   ⚠️  AVISOS:")
                    for warning in result.warnings:
                        report.append(f"      • {warning}")
                
                if result.suggestions:
                    report.append("   💡 SUGESTÕES:")
                    for suggestion in result.suggestions:
                        report.append(f"      • {suggestion}")
                
                report.append("")
        
        # Conclusão
        if total_errors == 0:
            report.extend([
                "✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO!",
                "   Os dados estão prontos para produção.",
                ""
            ])
        else:
            report.extend([
                "❌ VALIDAÇÃO FALHOU!",
                "   Corrija os erros antes de prosseguir.",
                ""
            ])
        
        return "\n".join(report)
    
    def validate_all(self) -> str:
        """Executa validação completa dos dados"""
        print("🔍 Iniciando validação dos dados...")
        
        try:
            data = self.load_data()
        except Exception as e:
            return f"❌ Erro ao carregar dados: {e}"
        
        results = []
        
        # Validar estrutura de cada estado
        for estado_codigo, estado_data in data.items():
            result = self.validate_estado_structure(estado_codigo, estado_data)
            if not result.is_valid or result.warnings or result.suggestions:
                results.append((f"Estado {estado_codigo}", result))
            
            # Validar cada gíria do estado
            if 'girias' in estado_data:
                for i, giria in enumerate(estado_data['girias']):
                    giria_result = self.validate_giria_structure(giria, estado_codigo)
                    if not giria_result.is_valid or giria_result.warnings or giria_result.suggestions:
                        results.append((f"Gíria {i+1} de {estado_codigo}", giria_result))
        
        # Verificar duplicatas
        duplicates_result = self.check_duplicates(data)
        if duplicates_result.warnings or duplicates_result.suggestions:
            results.append(("Verificação de Duplicatas", duplicates_result))
        
        # Validar estatísticas
        stats_result = self.validate_statistics(data)
        if stats_result.warnings or stats_result.suggestions:
            results.append(("Estatísticas Gerais", stats_result))
        
        return self.generate_report(results)

def main():
    """Função principal"""
    try:
        validator = GiriasValidator()
        report = validator.validate_all()
        
        # Exibir relatório
        print(report)
        
        # Salvar relatório em arquivo
        report_file = Path(__file__).parent.parent / "validation_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Relatório salvo em: {report_file}")
        
        # Retornar código de saída baseado no resultado
        if "VALIDAÇÃO FALHOU" in report:
            return 1
        else:
            return 0
        
    except Exception as e:
        print(f"❌ Erro durante validação: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 