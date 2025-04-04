// Slot machine animation
// Animates a slot machine display going from $9999 to $0

// Canvas settings
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;

// Animation settings
const START_VALUE = 9999;
const END_VALUE = 0;
const ANIMATION_DURATION = 5000; // 5 seconds total
let startTime;
let currentValue = START_VALUE;
let animationStarted = false;
let animationComplete = false;

// Colors
const BG_COLOR = [20, 20, 30];
const MACHINE_COLOR = [40, 40, 50];
const DISPLAY_COLOR = [30, 30, 40];
const GOLD_COLOR = [255, 215, 0];
const TEXT_COLOR = [255, 255, 255];
const RED_COLOR = [220, 30, 30];

function setup() {
  createCanvas(CANVAS_WIDTH, CANVAS_HEIGHT);
  textFont('monospace');
  textAlign(CENTER, CENTER);
  
  // Start animation after a short delay
  setTimeout(() => {
    animationStarted = true;
    startTime = millis();
  }, 500);
}

function draw() {
  background(BG_COLOR);
  
  // Draw slot machine
  drawSlotMachine();
  
  // Update animation
  if (animationStarted && !animationComplete) {
    updateAnimation();
  }
  
  // Draw instructions
  fill(150);
  textSize(14);
  text("Press 'S' to save image | Press 'R' to restart animation", width/2, height - 20);
}

function drawSlotMachine() {
  // Machine body
  push();
  fill(MACHINE_COLOR);
  stroke(GOLD_COLOR);
  strokeWeight(3);
  rect(width/2 - 200, height/2 - 200, 400, 400, 20);
  pop();
  
  // Display screen
  push();
  fill(DISPLAY_COLOR);
  stroke(GOLD_COLOR);
  strokeWeight(4);
  rect(width/2 - 150, height/2 - 60, 300, 120, 10);
  pop();
  
  // Dollar amount
  push();
  fill(TEXT_COLOR);
  textSize(80);
  text("$" + Math.floor(currentValue).toLocaleString('en-US'), width/2, height/2);
  pop();
  
  // Lever
  push();
  stroke(100);
  strokeWeight(2);
  fill(150);
  rect(width/2 + 220, height/2 - 100, 20, 200, 5);
  fill(RED_COLOR);
  noStroke();
  ellipse(width/2 + 230, height/2 - 100, 40, 40);
  pop();
  
  // Decorative lights
  drawLights();
}

function drawLights() {
  // Top lights
  for (let i = 0; i < 8; i++) {
    const x = width/2 - 160 + i * 45;
    const y = height/2 - 180;
    
    push();
    noStroke();
    
    // Randomly light up some bulbs during animation
    if (!animationComplete && frameCount % 10 < 5 && random() > 0.7) {
      fill(GOLD_COLOR);
    } else if (animationComplete) {
      // All lights on when animation completes
      fill(GOLD_COLOR);
    } else {
      // Dim lights otherwise
      fill(100, 100, 50);
    }
    
    ellipse(x, y, 15, 15);
    pop();
  }
  
  // Bottom lights
  for (let i = 0; i < 8; i++) {
    const x = width/2 - 160 + i * 45;
    const y = height/2 + 180;
    
    push();
    noStroke();
    
    // Randomly light up some bulbs during animation
    if (!animationComplete && frameCount % 15 < 8 && random() > 0.6) {
      fill(GOLD_COLOR);
    } else if (animationComplete) {
      // All lights on when animation completes
      fill(GOLD_COLOR);
    } else {
      // Dim lights otherwise
      fill(100, 100, 50);
    }
    
    ellipse(x, y, 15, 15);
    pop();
  }
}

function updateAnimation() {
  const currentTime = millis();
  const elapsedTime = currentTime - startTime;
  const progress = constrain(elapsedTime / ANIMATION_DURATION, 0, 1);
  
  // Custom easing function for the animation
  let easedProgress;
  
  if (progress < 0.2) {
    // Slow start (first 20% of time)
    const phaseProgress = progress / 0.2;
    easedProgress = 0.03 * phaseProgress; // Only move 3% of the way during slow start
  } 
  else if (progress < 0.8) {
    // Acceleration phase (next 60% of time)
    const phaseProgress = (progress - 0.2) / 0.6;
    easedProgress = 0.03 + 0.87 * (phaseProgress * phaseProgress); // Move from 3% to 90%
  } 
  else {
    // Easing phase (final 20% of time)
    const phaseProgress = (progress - 0.8) / 0.2;
    easedProgress = 0.9 + 0.1 * easeOutQuad(phaseProgress); // Move from 90% to 100%
  }
  
  // Calculate current value based on eased progress
  currentValue = START_VALUE - easedProgress * (START_VALUE - END_VALUE);
  
  // Add some random jitter to simulate slot machine movement
  if (!animationComplete) {
    currentValue += random(-5, 5);
  }
  
  // Ensure we don't go below the end value
  currentValue = max(currentValue, END_VALUE);
  
  // Check if animation is complete
  if (progress >= 1) {
    currentValue = END_VALUE;
    animationComplete = true;
  }
}

// Quadratic ease out function
function easeOutQuad(t) {
  return t * (2 - t);
}

// Save the canvas as an image when 's' key is pressed
function keyPressed() {
  if (key === 's' || key === 'S') {
    saveCanvas('slot-machine', 'png');
  }
  // Reset animation when 'r' key is pressed
  if (key === 'r' || key === 'R') {
    currentValue = START_VALUE;
    animationStarted = false;
    animationComplete = false;
    setTimeout(() => {
      animationStarted = true;
      startTime = millis();
    }, 500);
  }
}