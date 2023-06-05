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
            #Validation for the type of file
            if not file.name.lower().endswith(".txt"):
                raise ValidationError({"error": "This file must be a txt file (.txt)"})

            #Select the file and generate randomly selected elements
            lines: List[str] = file.read().decode("utf-8").splitlines()
            len_lines: int = len(lines)
            amount_random: int = random.randint(1, len_lines)
            selected_items: List[str] = random.choices(lines, k=amount_random)

            
            return Response({
                "secret_code": "key",
                "amount_data_sample": amount_random,
                "data_sample": selected_items 
            }, status=status.HTTP_200_OK)

        raise ValidationError({"error": "The file was not provided"})
