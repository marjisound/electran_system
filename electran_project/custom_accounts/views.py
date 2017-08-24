from django.shortcuts import render
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()
