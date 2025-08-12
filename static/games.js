document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    const scoreElement = document.getElementById('score');
    const restartBtn = document.getElementById('restart-btn');
    let score = 0;
    let flippedCards = [];
    let matchedCards = [];

    const cards = [
        'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D',
        'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H'
    ];

    function shuffle(array) {
        array.sort(() => Math.random() - 0.5);
    }

    function createBoard() {
        shuffle(cards);
        for (let i = 0; i < cards.length; i++) {
            const card = document.createElement('div');
            card.classList.add('card');
            card.dataset.value = cards[i];
            card.addEventListener('click', flipCard);
            gameBoard.appendChild(card);
        }
    }

    function flipCard() {
        if (flippedCards.length < 2 && !this.classList.contains('flipped')) {
            this.classList.add('flipped');
            this.textContent = this.dataset.value;
            flippedCards.push(this);

            if (flippedCards.length === 2) {
                setTimeout(checkForMatch, 1000);
            }
        }
    }

    function checkForMatch() {
        const [card1, card2] = flippedCards;
        if (card1.dataset.value === card2.dataset.value) {
            matchedCards.push(card1, card2);
            score++;
            scoreElement.textContent = score;
            if (matchedCards.length === cards.length) {
                alert('Congratulations! You won!');
            }
        } else {
            card1.classList.remove('flipped');
            card1.textContent = '';
            card2.classList.remove('flipped');
            card2.textContent = '';
        }
        flippedCards = [];
    }

    function restartGame() {
        gameBoard.innerHTML = '';
        flippedCards = [];
        matchedCards = [];
        score = 0;
        scoreElement.textContent = score;
        createBoard();
    }

    restartBtn.addEventListener('click', restartGame);

    createBoard();
});
