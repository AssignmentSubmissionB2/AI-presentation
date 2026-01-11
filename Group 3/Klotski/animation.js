const CELL_SIZE = 85;
const CELL_GAP = 5;
let ANIMATION_SPEED = 600;

let currentSolution = null;
let currentStateIndex = 0;
let isAnimating = false;
let autoplayInterval = null;
let blockElements = {};
let currentAlgorithm = null;

function updateSpeed(value) {
    ANIMATION_SPEED = parseInt(value);
}

function initializeBoard(blocks) {
    const boardDiv = document.getElementById('board');
    boardDiv.innerHTML = '';
    blockElements = {};
    
    blocks.forEach(block => {
        if (block.id === 0) return;
        
        const div = document.createElement('div');
        div.classList.add('tile', `color-${block.id}`);
        div.textContent = block.id;
        
        const width = block.width * CELL_SIZE - CELL_GAP;
        const height = block.height * CELL_SIZE - CELL_GAP;
        const left = block.col * CELL_SIZE + CELL_GAP;
        const top = block.row * CELL_SIZE + CELL_GAP;
        
        div.style.width = `${width}px`;
        div.style.height = `${height}px`;
        div.style.left = `${left}px`;
        div.style.top = `${top}px`;
        
        boardDiv.appendChild(div);
        blockElements[block.id] = div;
    });
}

function animateToState(stateIndex, instant = false) {
    if (!currentSolution || stateIndex < 0 || stateIndex >= currentSolution.states.length) {
        return;
    }
    
    isAnimating = true;
    currentStateIndex = stateIndex;
    const state = currentSolution.states[stateIndex];
    
    const animations = [];
    state.forEach(block => {
        if (block.id === 0 || !blockElements[block.id]) return;
        
        const div = blockElements[block.id];
        const width = block.width * CELL_SIZE - CELL_GAP;
        const height = block.height * CELL_SIZE - CELL_GAP;
        const left = block.col * CELL_SIZE + CELL_GAP;
        const top = block.row * CELL_SIZE + CELL_GAP;
        
        animations.push(
            anime({
                targets: div,
                left: left,
                top: top,
                width: width,
                height: height,
                duration: instant ? 0 : ANIMATION_SPEED,
                easing: 'easeInOutCubic',
                complete: () => {
                    isAnimating = false;
                }
            })
        );
    });
    
    updateUI();
    return Promise.all(animations);
}

async function runAlgorithm(algorithm) {
    if (isAnimating) return;
    
    stopAutoplay();
    
    // Update active button
    document.querySelectorAll('.algo-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`${algorithm}Btn`).classList.add('active');
    
    currentAlgorithm = algorithm;
    
    try {
        const filename = `${algorithm}_solution.json`;
        const response = await fetch(filename);
        
        if (!response.ok) {
            throw new Error(`Could not load ${filename}. Make sure you ran main.py first!`);
        }
        
        const solution = await response.json();
        currentSolution = solution;
        currentStateIndex = 0;
        
        initializeBoard(solution.states[0]);
        updateUI();
        enableControls();
        
        const algoNames = {
            'bfs': 'BFS (Breadth-First Search)',
            'dfs': 'DFS (Depth-First Search)',
            'astar': 'A* (A-Star Search)'
        };
        
        document.getElementById('moveDisplay').textContent = `${algoNames[algorithm]} loaded! ${solution.num_moves} moves`;
        document.getElementById('moveDisplay').classList.remove('error');
    } catch (error) {
        const msg = document.getElementById('moveDisplay');
        msg.textContent = 'ERROR: Run "python main.py" first to generate JSON files, then start a web server';
        msg.classList.add('error');
        console.error(error);
    }
}

function nextMove() {
    if (!currentSolution || isAnimating) return;
    if (currentStateIndex < currentSolution.states.length - 1) {
        animateToState(currentStateIndex + 1);
    }
}

function previousMove() {
    if (!currentSolution || isAnimating) return;
    if (currentStateIndex > 0) {
        animateToState(currentStateIndex - 1);
    }
}

function resetAnimation() {
    if (!currentSolution || isAnimating) return;
    stopAutoplay();
    animateToState(0, true);
}

function toggleAutoplay() {
    if (!currentSolution) return;
    
    if (autoplayInterval) {
        stopAutoplay();
    } else {
        startAutoplay();
    }
}

function startAutoplay() {
    const btn = document.getElementById('autoplayBtn');
    btn.textContent = '⏸ PAUSE';
    
    autoplayInterval = setInterval(() => {
        if (currentStateIndex < currentSolution.states.length - 1) {
            nextMove();
        } else {
            stopAutoplay();
        }
    }, ANIMATION_SPEED + 100);
}

function stopAutoplay() {
    if (autoplayInterval) {
        clearInterval(autoplayInterval);
        autoplayInterval = null;
        const btn = document.getElementById('autoplayBtn');
        btn.textContent = '▶ AUTOPLAY';
    }
}

function updateUI() {
    if (!currentSolution) return;
    
    document.getElementById('algorithm').textContent = currentSolution.algorithm;
    document.getElementById('moves').textContent = currentSolution.num_moves;
    document.getElementById('currentMove').textContent = `${currentStateIndex}/${currentSolution.num_moves}`;
    document.getElementById('states').textContent = currentSolution.states_explored.toLocaleString();
    document.getElementById('maxSpace').textContent = currentSolution.max_space_used.toLocaleString();
    document.getElementById('branching').textContent = currentSolution.branching_factor?.toFixed(2) || '0.00';
    document.getElementById('runtime').textContent = `${currentSolution.runtime.toFixed(3)}s`;
    document.getElementById('timeComplex').textContent = currentSolution.time_complexity;
    document.getElementById('spaceComplex').textContent = currentSolution.space_complexity;
    
    if (currentStateIndex > 0 && currentStateIndex <= currentSolution.moves.length) {
        const move = currentSolution.moves[currentStateIndex - 1];
        document.getElementById('moveDisplay').textContent = `Move ${currentStateIndex}: ${move}`;
    } else if (currentStateIndex === 0) {
        document.getElementById('moveDisplay').textContent = 'Initial State';
    } else {
        document.getElementById('moveDisplay').textContent = '✓ PUZZLE SOLVED!';
    }
    
    document.getElementById('prevBtn').disabled = currentStateIndex === 0;
    document.getElementById('nextBtn').disabled = currentStateIndex === currentSolution.states.length - 1;
}

function enableControls() {
    document.getElementById('autoplayBtn').disabled = false;
    document.getElementById('resetBtn').disabled = false;
    document.getElementById('prevBtn').disabled = false;
    document.getElementById('nextBtn').disabled = false;
    updateUI();
}

document.addEventListener('keydown', (e) => {
    if (!currentSolution) return;
    
    switch(e.key) {
        case 'ArrowLeft':
            previousMove();
            break;
        case 'ArrowRight':
            nextMove();
            break;
        case ' ':
            e.preventDefault();
            toggleAutoplay();
            break;
        case 'r':
        case 'R':
            resetAnimation();
            break;
        case '1':
            runAlgorithm('bfs');
            break;
        case '2':
            runAlgorithm('dfs');
            break;
        case '3':
            runAlgorithm('astar');
            break;
    }
});