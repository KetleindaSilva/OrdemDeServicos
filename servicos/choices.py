from django.db.models import TextChoices

class ChoicesCategoriaManutencao(TextChoices):
    TROCAR_VALVULA_MOTOR = "TVM", "Trocar válvula do motor",
    TROCAR_OLEO = "TO", "Troca de óleo",
    TROCAR_FREIO = "TF", "Troca de freio",
    TROCAR_PNEUS = "TP", "Troca de pneus",
    TROCAR_AMORTECEDOR = "TA", "Troca de amortecedor",
    BALANCEAMENTO = "B", "Balanceamento"