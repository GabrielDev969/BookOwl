import pandas as pd
from django.core.exceptions import ValidationError
from django.db import transaction
from library.models import Book, Library
import logging
import json

logger = logging.getLogger(__name__)

def validate_books(file_path, file_type='csv', user=None):
    try:
        if not user or not user.is_authenticated or not hasattr(user, 'library'):
            raise ValueError("Usuário não autenticado ou sem biblioteca associada.")
        library = user.library

        if file_type.lower() == 'csv':
            df = pd.read_csv(file_path)
        elif file_type.lower() == 'xlsx':
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Tipo de arquivo não suportado. Use 'csv' ou 'xlsx'.")
        
        expected_columns = {'title', 'author', 'description', 'status'}
        if not expected_columns.issubset(df.columns):
            missing = expected_columns - set(df.columns)
            raise ValueError(f"Colunas faltando no arquivo: {missing}")
        
        total_processed = 0
        valid_books = []
        errors = []
        data_for_review = []

        valid_statuses = {'available', 'unavailable'}

        for index, row in df.iterrows():
            total_processed += 1
            row_errors = {}
            is_valid = True
            row_data = {
                'title': row['title'],
                'author': row['author'],
                'description': row['description'],
                'status': row['status']
            }

            try:
                if row['status'] not in valid_statuses:
                    row_errors['status'] = f"Status inválido: {row['status']} (deve ser 'available' ou 'unavailable')"
                    is_valid = False
                
                if not isinstance(row['title'], str) or len(row['title']) > 200:
                    row_errors['title'] = 'Título inválido ou muito longo'
                    is_valid = False
                if not isinstance(row['author'], str) or len(row['author']) > 100:
                    row_errors['author'] = "Autor inválido ou muito longo"
                    is_valid = False
                if not isinstance(row['description'], str):
                    row_errors['description'] = "Descrição inválida"
                    is_valid = False
                
                if is_valid:
                    book = Book(
                        library=library,
                        title=row['title'],
                        author=row['author'],
                        description=row['description'],
                        status=row['status']
                    )
                    valid_books.append(book)

            except Exception as e:
                row_errors['general'] = f"Erro inesperado: {str(e)}"
                is_valid = False
                logger.error(f"Erro ao processar linha {index + 2}: {str(e)}")
            
            data_for_review.append({
                'row': index + 2,
                'data': row_data,
                'errors': row_errors
            })

            if row_errors:
                errors.append({'row': index + 2, 'errors': row_errors})

        return {
            'status': 'success' if not errors else 'partial',
            'total_processed': total_processed,
            'valid_books': valid_books,
            'data_for_review': data_for_review,
            'errors': errors
        }
    
    except Exception as e:
        logger.error(f"Erro ao validar arquivo: {str(e)}")

        return {
            'status': 'error',
            'total_processed': 0,
            'valid_books': [],
            'data_for_review': [],
            'errors': [f"Erro geral: {str(e)}"]
        }
    
def save_books(valid_books, batch_size=1000):
    try:
        total_imported = 0
        if valid_books:
            with transaction.atomic():
                Book.objects.bulk_create(valid_books, batch_size=batch_size)
                total_imported = len(valid_books)

        return {
            'status': 'success',
            'total_imported': total_imported,
            'errors': []
        }
    
    except Exception as e:
        logger.error(f"Erro ao salvar lotes: {str(e)}")
        return {
            'status': 'error',
            'total_imported': 0,
            'errors': [f"Erro ao salvar lotes: {str(e)}"]
        }