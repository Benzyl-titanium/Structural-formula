// 创建“回到顶部”按钮
const backToTopButton = document.createElement('a');
backToTopButton.className = 'back-to-top';
backToTopButton.innerHTML = '回到顶部';
backToTopButton.href = '#'; // 防止页面刷新
document.body.appendChild(backToTopButton);

let lastScrollY = window.scrollY;
let isScrollingUp = false;

// 监听滚动事件
window.addEventListener('scroll', () => {
  const currentScrollY = window.scrollY;

  // 判断是否向上滑动
  isScrollingUp = currentScrollY < lastScrollY && currentScrollY > 300;

  // 更新按钮显示状态
  if (isScrollingUp) {
    backToTopButton.classList.add('visible');
  } else {
    backToTopButton.classList.remove('visible');
  }

  lastScrollY = currentScrollY;
});

// 点击平滑滚动到顶部
backToTopButton.addEventListener('click', (e) => {
  e.preventDefault();
  window.scrollTo({ top: 0, behavior: 'smooth' });
});