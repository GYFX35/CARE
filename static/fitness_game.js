document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const exerciseNameElement = document.getElementById('exercise-name');
    const exerciseImageElement = document.getElementById('exercise-image');
    const exerciseDescriptionElement = document.getElementById('exercise-description');
    const repsElement = document.getElementById('reps');
    const setsElement = document.getElementById('sets');
    const startWorkoutBtn = document.getElementById('start-workout-btn');
    const nextExerciseBtn = document.getElementById('next-exercise-btn');
    const exercisesCompletedElement = document.getElementById('exercises-completed');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Game Data
    const exercises = [
        {
            name: 'Jumping Jacks',
            description: 'Why do this? Jumping jacks are a great cardio exercise that warms up your entire body and improves circulation.',
            image: 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWdzM2I2dDI3cWw2b3JtY3k3aGZtY284b3I4c2s3bDI2cTJqYjVncyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7btgdsxb2e3o6n8Q/giphy.gif',
            reps: 30,
            sets: 3
        },
        {
            name: 'Squats',
            description: 'Why do this? Squats are fantastic for building leg strength (quads, hamstrings, and glutes) and improving core stability.',
            image: 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDBnMHQ0ajB6cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w4cWJtY2w/glove/giphy.gif',
            reps: 15,
            sets: 3
        }
    ];

    // Game State
    let currentExerciseIndex = 0;
    let exercisesCompleted = 0;

    // Functions
    function startWorkout() {
        currentExerciseIndex = 0;
        exercisesCompleted = 0;
        updateExerciseUI();
        startWorkoutBtn.style.display = 'none';
        nextExerciseBtn.style.display = 'inline-block';
    }

    function nextExercise() {
        exercisesCompleted++;
        exercisesCompletedElement.textContent = exercisesCompleted;
        currentExerciseIndex++;
        if (currentExerciseIndex >= exercises.length) {
            finishWorkout();
        } else {
            updateExerciseUI();
        }
    }

    function updateExerciseUI() {
        const exercise = exercises[currentExerciseIndex];
        exerciseNameElement.textContent = exercise.name;
        exerciseImageElement.src = exercise.image;
        exerciseDescriptionElement.textContent = exercise.description;
        repsElement.textContent = exercise.reps;
        setsElement.textContent = exercise.sets;
    }

    function finishWorkout() {
        exerciseNameElement.textContent = "Workout Complete!";
        exerciseImageElement.src = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWloY3Q1aXk1cGJzY3k1eGJ6c3Z2b3k1cGJzY3k1eGJ6c3Z2b3k1eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7abGQa0aRzkvZJmw/giphy.gif';
        exerciseDescriptionElement.textContent = "Great job! You've completed the fitness challenge. Remember to rest and hydrate.";
        repsElement.textContent = '--';
        setsElement.textContent = '--';
        nextExerciseBtn.style.display = 'none';
        startWorkoutBtn.style.display = 'inline-block';
        startWorkoutBtn.textContent = 'Start Again';
    }

    async function handleSend() {
        const message = userInput.value.trim();
        if (message) {
            // Display user message
            const userMessageElement = document.createElement('div');
            userMessageElement.classList.add('message', 'user-message');
            userMessageElement.innerHTML = `<p>${message}</p>`;
            chatBox.appendChild(userMessageElement);
            chatBox.scrollTop = chatBox.scrollHeight;

            // Clear input
            userInput.value = '';

            try {
                const response = await fetch('/fitness_coach', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `message=${encodeURIComponent(message)}`
                });

                const data = await response.json();
                const coachResponse = data.response;

                const coachMessageElement = document.createElement('div');
                coachMessageElement.classList.add('message', 'coach-message');
                coachMessageElement.innerHTML = `<p>${coachResponse}</p>`;
                chatBox.appendChild(coachMessageElement);
                chatBox.scrollTop = chatBox.scrollHeight;

            } catch (error) {
                console.error('Error fetching AI response:', error);
                const coachMessageElement = document.createElement('div');
                coachMessageElement.classList.add('message', 'coach-message');
                coachMessageElement.innerHTML = `<p>Sorry, I'm having a little trouble connecting right now. Please try again later.</p>`;
                chatBox.appendChild(coachMessageElement);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }
    }

    // Event Listeners
    startWorkoutBtn.addEventListener('click', startWorkout);
    nextExerciseBtn.addEventListener('click', nextExercise);
    sendBtn.addEventListener('click', handleSend);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    });
});
