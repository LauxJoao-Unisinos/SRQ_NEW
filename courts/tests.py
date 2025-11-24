from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from courts.models import Court, Block
from courts.forms import BlockForm
from reservations.models import Reservation
from django.contrib.auth import get_user_model


User = get_user_model()


class BlockFormTest(TestCase):
    def setUp(self):
        self.court = Court.objects.create(
            name="Quadra Teste",
            court_type="futebol",
            price_per_hour=120,
            is_active=True,
        )
        self.user = User.objects.create_user(
            username="user1",
            password="teste123",
        )

        # faz reserva 
        now = timezone.now()
        self.res_start = now + timedelta(days=1)
        self.res_end = self.res_start + timedelta(hours=1)

        self.reservation = Reservation.objects.create(
            user=self.user,
            court=self.court,
            start=self.res_start,
            end=self.res_end,
        )

    def test_block_cannot_overlap_existing_reservation(self):
        """
        O BlockForm não deve ser válido se tentar bloquear um horário
        em que já existe uma reserva.
        """
        # tentar bloqueio dando overlap em uma reserva
        form_data = {
            "court": self.court.id,
            "start": self.res_start,
            "end": self.res_end,
            "reason": "Manutenção",
        }
        form = BlockForm(data=form_data)

        self.assertFalse(form.is_valid())
        # deve dar erro
        self.assertTrue(
            form.non_field_errors()
            or form.errors.get("start")
            or form.errors.get("end")
        )
