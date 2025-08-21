        // Simulação de API para o chat com IA
        document.addEventListener('DOMContentLoaded', function() {
            const chatInput = document.querySelector('#ai input[type="text"]');
            const chatSendBtn = document.querySelector('#ai button');
            const chatContainer = document.querySelector('.ai-chat .space-y-4');
            const typingIndicator = document.querySelector('.typing-indicator').parentNode.parentNode;
            
            typingIndicator.style.display = 'none';
            
            chatSendBtn.addEventListener('click', sendMessage);
            chatInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            function sendMessage() {
                const message = chatInput.value.trim();
                if (message === '') return;
                
                // Adiciona mensagem do usuário
                const userMessageDiv = document.createElement('div');
                userMessageDiv.className = 'flex justify-end';
                userMessageDiv.innerHTML = `
                    <div class="message user-message p-3">
                        <p>${message}</p>
                    </div>
                `;
                chatContainer.appendChild(userMessageDiv);
                
                // Limpa o input
                chatInput.value = '';
                
                // Mostra indicador de digitação
                typingIndicator.style.display = 'flex';
                
                // Rola para baixo
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                // Simula resposta da API após 1-2 segundos
                setTimeout(() => {
                    typingIndicator.style.display = 'none';
                    
                    // Resposta simulada da IA
                    const aiResponses = [
                        "Entendi sua dúvida! Vou explicar isso de forma clara e detalhada.",
                        "Ótima pergunta! Vamos abordar esse tópico passo a passo.",
                        "Posso te ajudar com isso. Aqui está a explicação que você precisa:",
                        "Esse é um conceito importante. Deixe-me esclarecer para você."
                    ];
                    
                    const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)];
                    
                    const aiMessageDiv = document.createElement('div');
                    aiMessageDiv.className = 'flex justify-start';
                    aiMessageDiv.innerHTML = `
                        <div class="message ai-message p-3">
                            <p>${randomResponse}</p>
                        </div>
                    `;
                    chatContainer.appendChild(aiMessageDiv);
                    
                    // Rola para baixo novamente
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }, 1500 + Math.random() * 1000);
            }
            
            // Anima os cards de matérias ao rolar
            const subjectCards = document.querySelectorAll('.subject-card');
            
            function animateCards() {
                subjectCards.forEach((card, index) => {
                    const cardPosition = card.getBoundingClientRect().top;
                    const screenPosition = window.innerHeight / 1.3;
                    
                    if (cardPosition < screenPosition) {
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, index * 100);
                    }
                });
            }
            
            // Define opacidade inicial para a animação
            subjectCards.forEach(card => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            });
            
            window.addEventListener('scroll', animateCards);
            animateCards(); // Executa uma vez ao carregar
        });