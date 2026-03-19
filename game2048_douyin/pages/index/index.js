// pages/index/index.js - 数字合成2048游戏逻辑
const SIZE = 4;

Page({
  data: {
    grid: [],
    score: 0,
    best: 0,
    gameOver: false,
    isWin: false,
  },

  onLoad() {
    let best = tt.getStorageSync('best2048') || 0;
    this.setData({ best });
    this.init();
  },

  init() {
    let grid = Array.from({ length: SIZE }, () => Array(SIZE).fill(0));
    this.grid = grid;
    this.score = 0;
    this.addRandomTile();
    this.addRandomTile();
    this.render();
    this.setData({ gameOver: false, isWin: false, score: 0 });
  },

  addRandomTile() {
    let empty = [];
    for (let r = 0; r < SIZE; r++)
      for (let c = 0; c < SIZE; c++)
        if (this.grid[r][c] === 0) empty.push([r, c]);
    if (!empty.length) return;
    let [r, c] = empty[Math.floor(Math.random() * empty.length)];
    this.grid[r][c] = Math.random() < 0.9 ? 2 : 4;
  },

  render() {
    this.setData({ grid: JSON.parse(JSON.stringify(this.grid)) });
  },

  // 触摸相关
  touchStart(e) {
    this.startX = e.touches[0].clientX;
    this.startY = e.touches[0].clientY;
  },

  touchEnd(e) {
    if (!this.startX || !this.startY) return;
    let dx = e.changedTouches[0].clientX - this.startX;
    let dy = e.changedTouches[0].clientY - this.startY;
    this.startX = null;
    this.startY = null;
    if (Math.abs(dx) < 30 && Math.abs(dy) < 30) return;
    if (Math.abs(dx) > Math.abs(dy)) {
      this.slide(dx > 0 ? 'right' : 'left');
    } else {
      this.slide(dy > 0 ? 'down' : 'up');
    }
  },

  slide(dir) {
    const vectors = { up: [-1, 0], down: [1, 0], left: [0, -1], right: [0, 1] };
    let [dr, dc] = vectors[dir];
    let moved = false;
    let rowOrder = dir === 'down' ? [3, 2, 1, 0] : [0, 1, 2, 3];
    let colOrder = dir === 'right' ? [3, 2, 1, 0] : [0, 1, 2, 3];

    for (let row of rowOrder) {
      for (let col of colOrder) {
        if (this.grid[row][col] === 0) continue;
        let v = this.grid[row][col];
        let nr = row, nc = col;
        while (true) {
          let tr = nr + dr, tc = nc + dc;
          if (tr < 0 || tr >= SIZE || tc < 0 || tc >= SIZE) break;
          if (this.grid[tr][tc] === 0) { nr = tr; nc = tc; }
          else if (this.grid[tr][tc] === v) { nr = tr; nc = tc; break; }
          else break;
        }
        if (nr !== row || nc !== col) {
          if (this.grid[nr][nc] === v) {
            this.grid[nr][nc] = v * 2;
            this.score += v * 2;
            this.grid[row][col] = 0;
            if (v * 2 === 2048) {
              setTimeout(() => this.showOverlay(true), 200);
            }
          } else {
            this.grid[nr][nc] = v;
            this.grid[row][col] = 0;
          }
          moved = true;
        }
      }
    }

    if (moved) {
      this.addRandomTile();
      this.render();
      this.setData({ score: this.score });
      if (this.score > this.data.best) {
        this.setData({ best: this.score });
        tt.setStorageSync('best2048', this.score);
      }
      setTimeout(() => this.checkGameOver(), 200);
    }
  },

  checkGameOver() {
    for (let r = 0; r < SIZE; r++)
      for (let c = 0; c < SIZE; c++)
        if (this.grid[r][c] === 0) return;
    for (let r = 0; r < SIZE; r++)
      for (let c = 0; c < SIZE; c++) {
        if (r < SIZE - 1 && this.grid[r][c] === this.grid[r + 1][c]) return;
        if (c < SIZE - 1 && this.grid[r][c] === this.grid[r][c + 1]) return;
      }
    this.showOverlay(false);
  },

  showOverlay(isWin) {
    this.setData({ gameOver: true, isWin });
  },

  restart() {
    this.init();
  },

  onShareAppMessage() {
    return {
      title: `我在2048得到了 ${this.score} 分，一起来挑战！🎮`,
      desc: '经典数字合成游戏，挑战你的反应和策略！',
    };
  },
});
