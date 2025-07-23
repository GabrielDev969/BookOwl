from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
import telegram
from telegram.constants import ParseMode
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

def home(request):
    """
    Render the home page.
    """
    return render(request, 'Home/home.html')

def about(request):
    """
    Render the about page.
    """
    return render(request, 'Home/about.html')

async def send_to_telegram(name, username, email, message):
    bot = telegram.Bot(token=os.environ.get('YOUR_TELEGRAM_BOT_TOKEN'))
    group_id = os.environ.get('YOUR_GROUP_CHAT_ID')
    text = f"<b>BookOwl</b>\n\n<b>Nome</b>: {name}\n<b>Username:</b> {username}\n<b>Email:</b> {email or 'Não fornecido'}\n<b>Mensagem:</b>\n {message}"
    await bot.send_message(chat_id=group_id, text=text, parse_mode=ParseMode.HTML)

def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.user.username
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Get the referring URL to redirect back to the same page
        redirect_url = request.META.get('HTTP_REFERER', reverse('home'))
        
        if name and message:
            try:
                asyncio.run(send_to_telegram(name, username, email, message))
                messages.success(request, 'Feedback enviado com sucesso para o grupo no Telegram!')
            except Exception as e:
                messages.error(request, f'Erro ao enviar feedback: {str(e)}')
        else:
            messages.error(request, 'Nome e mensagem são obrigatórios.')
        
        return HttpResponseRedirect(redirect_url)
    
    # For GET requests, redirect to the referring page or home
    redirect_url = request.META.get('HTTP_REFERER', reverse('home'))
    return HttpResponseRedirect(redirect_url)