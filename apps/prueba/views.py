import random

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from typing import List, Dict, Any


from .utils import find_shortest_possible_key


class FileUploadView(APIView):
    """
    View to process the text file and generate the expected response
    """

    parser_class = FileUploadParser

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("keylog")

        if file:
            #Valida el tipo de archivo
            if not file.name.lower().endswith(".txt"):
                raise ValidationError({"error": "This file must be a txt file (.txt)"})

            # Selecciona el archivo, lo lee, decodifica y genera una selección aleatoria como muestra
            lines: List[str] = file.read().decode("utf-8").splitlines()
            len_lines: int = len(lines)
            amount_random: int = random.randint(1, len_lines)
            selected_items: List[str] = random.choices(lines, k=amount_random)

            # Validar la cantidad de caracteres de cada intento de login
            selected_items_wrong_format = [
                item for item in selected_items if len(item) != 3
            ]
            if selected_items_wrong_format:
                raise ValidationError(
                    {
                        "error": "The attemps have a format invalid, must be 3 characters",
                        "attempts_invalid": selected_items_wrong_format,
                    }
                )

            #Usa el útil de forma recursiva para obtener el key de login más corto posible
            key: str = find_shortest_possible_key(selected_items)
            return Response(
                {
                    "secret_code": key,
                    "amount_data_sample": amount_random,
                    "data_sample": selected_items,
                },
                status=status.HTTP_200_OK,
            )

        raise ValidationError({"error": "The file was not provided"})
