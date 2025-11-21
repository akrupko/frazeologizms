// Phraseological Units Training Game

class PhraseologyTrainer {
    constructor() {
        this.phrases = [];
        this.allPhrases = [];
        this.currentQuestion = null;
        this.correctAnswers = 0;
        this.totalQuestions = 0;
        this.usedPhrases = new Set();
        
        this.init();
    }
    
    async init() {
        await this.loadPhrases();
        this.setupEventListeners();
        this.startNewQuestion();
    }
    
    async loadPhrases() {
        try {
            console.log('Loading phrases from API...');
            
            // Get current category from URL or window variable
            const currentCategory = window.CURRENT_CATEGORY || this.getCategoryFromURL();
            
            // Build API URL with parameters
            const apiUrl = new URL(`${window.API_BASE_URL}/phrases`);
            if (currentCategory && currentCategory !== 'general') {
                apiUrl.searchParams.append('category', currentCategory);
            }
            apiUrl.searchParams.append('limit', '1000'); // Load more phrases for better quiz variety
            
            const response = await fetch(apiUrl.toString());
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Store all phrases for use in generating incorrect answers
            const allValidPhrases = data.phrases ? data.phrases.filter(phrase => {
                return phrase.meanings && 
                       phrase.meanings.length > 0 && 
                       phrase.meanings[0] !== "Значение требует уточнения" &&
                       phrase.meanings[0].trim().length > 10;
            }) : [];
            
            // Filter phrases based on category (API already filtered, but ensure consistency)
            if (currentCategory && currentCategory !== 'general') {
                this.phrases = allValidPhrases.filter(phrase => phrase.category === currentCategory);
                this.allPhrases = allValidPhrases; // Store all for generating incorrect options
            } else {
                // Use all phrases for general category
                this.phrases = allValidPhrases;
                this.allPhrases = allValidPhrases;
                window.CATEGORY_NAME = window.CATEGORY_NAME || 'Все категории';
            }
            
            console.log(`Loaded ${this.phrases.length} valid phrases for ${window.CATEGORY_NAME}`);
            
            if (this.phrases.length === 0) {
                throw new Error('No valid phrases found for this category');
            }
            
            // Hide loading, show quiz
            document.getElementById('loading').style.display = 'none';
            document.getElementById('quiz-content').style.display = 'block';
            
        } catch (error) {
            console.error('Error loading phrases:', error);
            this.showError(error);
        }
    }
    
    getCategoryFromURL() {
        const path = window.location.pathname;
        const filename = path.split('/').pop() || 'index.html';
        
        // Map filenames to categories
        const urlCategoryMap = {
            'index.html': 'general',
            // Old filenames (for backward compatibility)
            'animals.html': 'animals',
            'body-parts.html': 'body_parts',
            'emotions.html': 'emotions_feelings',
            'religion.html': 'religion_mythology',
            'work.html': 'work_labor',
            'family.html': 'family_relationships',
            'mind.html': 'mind_intelligence',
            'speech.html': 'speech_communication',
            'money.html': 'money_wealth',
            'time.html': 'time_age',
            'food.html': 'food_drink',
            'house.html': 'house_home',
            // New frazeologizmy_ prefixed filenames
            'frazeologizmy_animals.html': 'animals',
            'frazeologizmy_body-parts.html': 'body_parts',
            'frazeologizmy_emotions.html': 'emotions_feelings',
            'frazeologizmy_religion.html': 'religion_mythology',
            'frazeologizmy_work.html': 'work_labor',
            'frazeologizmy_family.html': 'family_relationships',
            'frazeologizmy_mind.html': 'mind_intelligence',
            'frazeologizmy_speech.html': 'speech_communication',
            'frazeologizmy_money.html': 'money_wealth',
            'frazeologizmy_time.html': 'time_age',
            'frazeologizmy_food.html': 'food_drink',
            'frazeologizmy_house.html': 'house_home',
            'frazeologizmy_appearance_beauty.html': 'appearance_beauty',
            'frazeologizmy_clothes_appearance.html': 'clothes_appearance',
            'frazeologizmy_games_entertainment.html': 'games_entertainment',
            'frazeologizmy_luck_fortune.html': 'luck_fortune',
            'frazeologizmy_quantity_measure.html': 'quantity_measure',
            'frazeologizmy_transport_travel.html': 'transport_travel',
            'frazeologizmy_war_conflict.html': 'war_conflict',
            'frazeologizmy_weather_nature.html': 'weather_nature'
        };
        
        return urlCategoryMap[filename] || 'general';
    }
    
    setupEventListeners() {
        document.getElementById('next-button').addEventListener('click', () => {
            // Check if this is the last question
            if (this.usedPhrases.size >= this.phrases.length) {
                this.showGameComplete();
            } else {
                this.startNewQuestion();
            }
        });
        
        document.getElementById('restart-button').addEventListener('click', () => {
            this.restart();
        });
        
        document.getElementById('show-etymology').addEventListener('click', () => {
            this.toggleEtymology();
        });
    }
    
    startNewQuestion() {
        // Hide feedback and etymology
        document.getElementById('feedback').style.display = 'none';
        document.getElementById('etymology-info').style.display = 'none';
        document.getElementById('show-etymology').style.display = 'none';
        
        // Hide control buttons until answer is given
        document.getElementById('next-button').style.display = 'none';
        document.getElementById('restart-button').style.display = 'none';
        
        // Check if all phrases have been used (game complete)
        if (this.usedPhrases.size >= this.phrases.length) {
            this.showGameComplete();
            return;
        }
        
        // Get a random phrase that hasn't been used yet
        const availablePhrases = this.phrases.filter(p => !this.usedPhrases.has(p.phrase));
        
        if (availablePhrases.length === 0) {
            // This shouldn't happen with the check above, but just in case
            this.showGameComplete();
            return;
        }
        
        const randomIndex = Math.floor(Math.random() * availablePhrases.length);
        const selectedPhrase = availablePhrases[randomIndex];
        
        this.currentQuestion = selectedPhrase;
        this.usedPhrases.add(selectedPhrase.phrase);
        
        console.log(`Selected phrase ${this.usedPhrases.size}/${this.phrases.length}: "${selectedPhrase.phrase}"`);
        
        this.displayQuestion();
        this.generateAnswerOptions();
    }
    
    displayQuestion() {
        document.getElementById('phrase').textContent = this.currentQuestion.phrase;
    }
    
    generateAnswerOptions() {
        const correctMeaning = this.getRandomMeaning(this.currentQuestion);
        const incorrectMeanings = this.getRandomIncorrectMeanings(correctMeaning, 2);
        
        // Combine and shuffle
        const allOptions = [correctMeaning, ...incorrectMeanings];
        this.shuffleArray(allOptions);
        
        // Store correct answer for checking
        this.correctAnswer = correctMeaning;
        
        this.displayAnswerOptions(allOptions);
    }
    
    getRandomMeaning(phrase) {
        const meanings = phrase.meanings.filter(m => 
            m && m.trim().length > 10 && m !== "Значение требует уточнения"
        );
        
        if (meanings.length === 0) {
            return "Значение недоступно";
        }
        
        return meanings[Math.floor(Math.random() * meanings.length)];
    }
    
    getRandomIncorrectMeanings(correctMeaning, count) {
        const incorrectMeanings = [];
        
        // First, try to get meanings from the same category
        const sameCategoryPhrases = this.phrases.filter(p => p !== this.currentQuestion);
        
        // If we don't have enough phrases in the same category, use all phrases
        let availablePhrases = sameCategoryPhrases.length >= count ? 
            sameCategoryPhrases : 
            this.allPhrases ? this.allPhrases.filter(p => p !== this.currentQuestion) : sameCategoryPhrases;
        
        // If we still don't have enough phrases, use what we have
        if (availablePhrases.length === 0) {
            availablePhrases = this.phrases.filter(p => p !== this.currentQuestion);
        }
        
        while (incorrectMeanings.length < count && availablePhrases.length > 0) {
            const randomPhrase = availablePhrases[Math.floor(Math.random() * availablePhrases.length)];
            const meaning = this.getRandomMeaning(randomPhrase);
            
            // Avoid duplicates and make sure it's different from correct answer
            if (meaning !== correctMeaning && 
                !incorrectMeanings.includes(meaning) &&
                meaning !== "Значение недоступно") {
                incorrectMeanings.push(meaning);
            }
            
            // Remove used phrase to avoid infinite loop
            const index = availablePhrases.indexOf(randomPhrase);
            availablePhrases.splice(index, 1);
        }
        
        // If we couldn't find enough different meanings, add some generic ones
        while (incorrectMeanings.length < count) {
            const genericMeanings = [
                "выражение радости или удовлетворения",
                "обозначение быстрого движения или действия", 
                "описание сложной или запутанной ситуации",
                "характеристика ненадежного человека",
                "обозначение большого количества чего-либо",
                "выражение недовольства или возмущения",
                "описание красивого внешнего вида",
                "характеристика умного человека",
                "обозначение трудной работы",
                "выражение согласия или одобрения"
            ];
            
            const generic = genericMeanings[Math.floor(Math.random() * genericMeanings.length)];
            if (!incorrectMeanings.includes(generic) && generic !== correctMeaning) {
                incorrectMeanings.push(generic);
            }
        }
        
        return incorrectMeanings;
    }
    
    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
    
    displayAnswerOptions(options) {
        const container = document.getElementById('answer-options');
        container.innerHTML = '';
        
        options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'answer-button';
            button.textContent = option;
            button.addEventListener('click', () => this.handleAnswer(option, button));
            container.appendChild(button);
        });
    }
    
    handleAnswer(selectedMeaning, buttonElement) {
        const isCorrect = selectedMeaning === this.correctAnswer;
        
        // Disable all buttons
        const allButtons = document.querySelectorAll('.answer-button');
        allButtons.forEach(btn => {
            btn.classList.add('disabled');
            btn.style.pointerEvents = 'none';
            
            // Mark correct/incorrect
            if (btn.textContent === this.correctAnswer) {
                btn.classList.add('correct');
            } else if (btn === buttonElement && !isCorrect) {
                btn.classList.add('incorrect');
            }
        });
        
        this.totalQuestions++;
        
        if (isCorrect) {
            this.correctAnswers++;
            this.showFeedback(true, "Правильно! 🎉", "Отличная работа!");
        } else {
            this.showFeedback(false, "Неправильно 😔", `Правильный ответ: ${this.correctAnswer}`);
        }
        
        this.updateStats();
        this.showControls();
    }
    
    showFeedback(isCorrect, title, message) {
        const feedback = document.getElementById('feedback');
        const feedbackMessage = document.getElementById('feedback-message');
        const correctAnswer = document.getElementById('correct-answer');
        
        feedback.className = `feedback ${isCorrect ? 'success' : 'error'}`;
        feedbackMessage.innerHTML = `<span class="emoji">${isCorrect ? '✅' : '❌'}</span>${title}`;
        
        // Add etymology if available (for both correct and incorrect answers)
        if (this.currentQuestion.etymology && this.currentQuestion.etymology.trim()) {
            correctAnswer.innerHTML = `${message}<br><br><strong>📖 Происхождение:</strong> ${this.currentQuestion.etymology}`;
        } else {
            correctAnswer.textContent = message;
        }
        
        feedback.style.display = 'block';
    }
    
    showControls() {
        // Check if this was the last question
        const isLastQuestion = this.usedPhrases.size >= this.phrases.length;
        
        // Handle next button visibility and text
        const nextButton = document.getElementById('next-button');
        if (isLastQuestion) {
            nextButton.style.display = 'none';
        } else {
            nextButton.style.display = 'inline-block'; // Explicitly show the button
            nextButton.textContent = 'Следующий вопрос';
        }
        
        document.getElementById('restart-button').style.display = 'inline-block';
        
        // Show etymology button if etymology is available
        if (this.currentQuestion.etymology && this.currentQuestion.etymology.trim()) {
            document.getElementById('show-etymology').style.display = 'inline-block';
        }
        
        // If this is the last question, automatically show completion after a delay
        if (isLastQuestion) {
            setTimeout(() => {
                this.showGameComplete();
            }, 2500); // Give user time to read feedback
        }
    }
    
    toggleEtymology() {
        const etymologyInfo = document.getElementById('etymology-info');
        const etymologyText = document.getElementById('etymology-text');
        
        if (etymologyInfo.style.display === 'none' || !etymologyInfo.style.display) {
            etymologyText.textContent = this.currentQuestion.etymology || 'Информация о происхождении недоступна';
            etymologyInfo.style.display = 'block';
        } else {
            etymologyInfo.style.display = 'none';
        }
    }
    
    updateStats() {
        document.getElementById('correct-count').textContent = this.correctAnswers;
        
        // Show progress more clearly
        const progressText = `${this.totalQuestions} / ${this.phrases.length}`;
        document.getElementById('total-count').textContent = progressText;
        
        const accuracy = this.totalQuestions > 0 ? 
            Math.round((this.correctAnswers / this.totalQuestions) * 100) : 0;
        document.getElementById('accuracy').textContent = `${accuracy}%`;
        
        // Update progress indicator if near completion
        const remaining = this.phrases.length - this.usedPhrases.size;
        if (remaining <= 3 && remaining > 0) {
            const totalCountElement = document.getElementById('total-count');
            totalCountElement.style.color = '#f59e0b';
            totalCountElement.style.fontWeight = '600';
        }
    }
    
    restart() {
        this.correctAnswers = 0;
        this.totalQuestions = 0;
        this.usedPhrases.clear();
        
        // Reset stats styling
        const totalCountElement = document.getElementById('total-count');
        totalCountElement.style.color = '';
        totalCountElement.style.fontWeight = '';
        
        this.updateStats();
        
        // Hide game complete screen if visible
        const gameCompleteDiv = document.getElementById('game-complete');
        if (gameCompleteDiv) {
            gameCompleteDiv.style.display = 'none';
        }
        
        // Show quiz content
        document.getElementById('quiz-content').style.display = 'block';
        
        this.startNewQuestion();
    }
    
    showGameComplete() {
        console.log('Game complete! All phrases have been shown.');
        
        // Hide quiz content
        document.getElementById('quiz-content').style.display = 'none';
        
        // Calculate final statistics
        const accuracy = this.totalQuestions > 0 ? 
            Math.round((this.correctAnswers / this.totalQuestions) * 100) : 0;
        
        // Create or update game complete screen
        let gameCompleteDiv = document.getElementById('game-complete');
        if (!gameCompleteDiv) {
            gameCompleteDiv = document.createElement('div');
            gameCompleteDiv.id = 'game-complete';
            gameCompleteDiv.className = 'game-complete';
            
            // Insert after quiz-content
            const quizContent = document.getElementById('quiz-content');
            quizContent.parentNode.insertBefore(gameCompleteDiv, quizContent.nextSibling);
        }
        
        // Determine performance level
        let performanceEmoji = '👍';
        let performanceText = 'Хорошая работа!';
        let performanceClass = 'good';
        
        if (accuracy >= 90) {
            performanceEmoji = '🏆';
            performanceText = 'Отличный результат!';
            performanceClass = 'excellent';
        } else if (accuracy >= 75) {
            performanceEmoji = '🎉';
            performanceText = 'Очень хорошо!';
            performanceClass = 'very-good';
        } else if (accuracy >= 60) {
            performanceEmoji = '👍';
            performanceText = 'Хорошая работа!';
            performanceClass = 'good';
        } else if (accuracy >= 40) {
            performanceEmoji = '📚';
            performanceText = 'Есть что изучать!';
            performanceClass = 'needs-improvement';
        } else {
            performanceEmoji = '💪';
            performanceText = 'Не сдавайтесь, продолжайте изучать!';
            performanceClass = 'keep-trying';
        }
        
        gameCompleteDiv.innerHTML = `
            <div class="game-complete-content ${performanceClass}">
                <div class="completion-header">
                    <div class="completion-emoji">${performanceEmoji}</div>
                    <h2>Игра завершена!</h2>
                    <p class="completion-subtitle">${performanceText}</p>
                </div>
                
                <div class="final-stats">
                    <div class="final-stats-grid">
                        <div class="final-stat">
                            <div class="final-stat-value">${this.correctAnswers}</div>
                            <div class="final-stat-label">Правильных ответов</div>
                        </div>
                        <div class="final-stat">
                            <div class="final-stat-value">${this.totalQuestions}</div>
                            <div class="final-stat-label">Всего вопросов</div>
                        </div>
                        <div class="final-stat">
                            <div class="final-stat-value">${accuracy}%</div>
                            <div class="final-stat-label">Точность</div>
                        </div>
                        <div class="final-stat">
                            <div class="final-stat-value">${this.phrases.length}</div>
                            <div class="final-stat-label">Изучено фразеологизмов</div>
                        </div>
                    </div>
                </div>
                
                <div class="completion-message">
                    <p>🎓 Вы изучили все фразеологизмы из категории <strong>"${window.CATEGORY_NAME || 'Все категории'}"</strong>!</p>
                    ${accuracy >= 75 ? 
                        '<p>✨ Отличное знание фразеологии поможет вам на экзаменах по русскому языку!</p>' : 
                        '<p>📖 Рекомендуем повторить материал для лучшего запоминания.</p>'
                    }
                </div>
                
                <div class="completion-actions">
                    <button id="play-again-button" class="primary-button">🔄 Начать заново</button>
                    <button id="choose-category-button" class="secondary-button">📚 Выбрать другую категорию</button>
                </div>
            </div>
        `;
        
        // Show the game complete screen
        gameCompleteDiv.style.display = 'block';
        
        // Add event listeners for buttons
        document.getElementById('play-again-button').addEventListener('click', () => {
            this.restart();
        });
        
        document.getElementById('choose-category-button').addEventListener('click', () => {
            // Navigate to categories page to choose another category
            window.location.href = 'categories.html';
        });
        
        // Scroll to top to show the completion screen
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    showError(error) {
        console.error('Showing error to user:', error);
        
        document.getElementById('loading').style.display = 'none';
        document.getElementById('quiz-content').style.display = 'none';
        
        const errorMessageDiv = document.getElementById('error-message');
        const isFileProtocol = window.location.protocol === 'file:';
        
        // Update error message based on the specific error and browser
        let errorContent = `
            <h3>❌ Ошибка загрузки</h3>
            <p>Не удалось загрузить базу фразеологизмов.</p>
        `;
        
        // Add specific troubleshooting for file:// protocol issues
        if (isFileProtocol) {
            errorContent += `
                <div style="background: #fef3c7; border: 1px solid #f59e0b; padding: 15px; border-radius: 8px; margin: 15px 0; text-align: left;">
                    <h4 style="color: #92400e; margin-top: 0;">📝 Рекомендации для Google Chrome:</h4>
                    <p style="color: #92400e; margin-bottom: 8px;">Для корректной работы в Chrome рекомендуется:</p>
                    <ul style="color: #92400e; text-align: left; padding-left: 20px;">
                        <li>Использовать локальный веб-сервер</li>
                        <li>Или открыть сайт в Microsoft Edge</li>
                        <li>Или запустить Chrome с параметром --allow-file-access-from-files</li>
                    </ul>
                </div>
            `;
        }
        
        // Add error details if available
        if (error && error.message) {
            errorContent += `
                <details style="margin-top: 15px; text-align: left;">
                    <summary style="cursor: pointer; color: #991b1b;">Подробности ошибки</summary>
                    <p style="background: #fef2f2; padding: 10px; border-radius: 4px; margin-top: 8px; font-family: monospace; font-size: 0.9em; color: #7f1d1d;">
                        ${error.message}
                    </p>
                </details>
            `;
        }
        
        errorContent += `
            <button onclick="location.reload()" class="retry-button">Попробовать снова</button>
        `;
        
        errorMessageDiv.innerHTML = errorContent;
        errorMessageDiv.style.display = 'block';
    }
}

// Initialize the trainer when components are loaded
function initializeTrainer() {
    console.log('Components loaded, initializing trainer...');
    window.trainer = new PhraseologyTrainer();
}

// Wait for components to load first, then initialize trainer
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, waiting for components...');
    
    // Check if components are already loaded
    if (window.ComponentLoader && document.getElementById('quiz-content')) {
        // Components already loaded, initialize immediately
        initializeTrainer();
    } else {
        // Wait for components to load
        window.addEventListener('componentsLoaded', initializeTrainer);
    }
});

// Add some visual feedback for button interactions
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('answer-button') || 
        e.target.classList.contains('next-button') ||
        e.target.classList.contains('control-button')) {
        
        // Add click animation
        e.target.style.transform = 'scale(0.95)';
        setTimeout(() => {
            e.target.style.transform = '';
        }, 150);
    }
});

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key >= '1' && e.key <= '3') {
        const buttons = document.querySelectorAll('.answer-button:not(.disabled)');
        const index = parseInt(e.key) - 1;
        if (buttons[index]) {
            buttons[index].click();
        }
    } else if (e.key === 'Enter' || e.key === ' ') {
        const nextButton = document.getElementById('next-button');
        if (nextButton.offsetParent !== null) { // Check if visible
            nextButton.click();
        }
    }
});