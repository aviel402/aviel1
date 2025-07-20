<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>מריו זז וקופץ</title>
<style>
  body { margin: 0; overflow: hidden; background: skyblue; }
  #game {
    position: relative;
    width: 800px; height: 400px;
    margin: 20px auto;
    background: linear-gradient(to top, #5c94fc 0%, #9df88a 100%);
    border: 2px solid #333;
  }
  #mario {
    position: absolute;
    bottom: 0;
    left: 50px;
    width: 50px;
    height: 70px;
    background: url('https://i.imgur.com/KVQTXJX.png') no-repeat center/contain;
  }
</style>
</head>
<body>

<div id="game">
  <div id="mario"></div>
</div>

<script>
  const mario = document.getElementById('mario');
  const game = document.getElementById('game');

  let posX = 50;
  let posY = 0; // 0 = על הקרקע
  let velocityY = 0;
  let isJumping = false;

  const gravity = 0.8;
  const jumpPower = 15;
  const groundHeight = 0;

  // תנועות
  document.addEventListener('keydown', e => {
    if(e.key === 'ArrowLeft') {
      posX -= 10;
      if(posX < 0) posX = 0;
    } else if(e.key === 'ArrowRight') {
      posX += 10;
      if(posX > game.clientWidth - mario.clientWidth) posX = game.clientWidth - mario.clientWidth;
    } else if(e.key === 'ArrowUp') {
      if(!isJumping) {
        velocityY = -jumpPower;
        isJumping = true;
      }
    }
    updatePosition();
  });

  function updatePosition() {
    mario.style.left = posX + 'px';
  }

  function gameLoop() {
    if(isJumping) {
      velocityY += gravity;
      posY += velocityY;

      if(posY >= groundHeight) {
        posY = groundHeight;
        velocityY = 0;
        isJumping = false;
      }
      mario.style.bottom = posY + 'px';
    }
    requestAnimationFrame(gameLoop);
  }

  updatePosition();
  gameLoop();
</script>

</body>
</html>
