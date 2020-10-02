const mobileNav = document.querySelector('.mobile-nav');
const hamburger = document.getElementById('hamburger');
const close = document.getElementById('close');
const navBtns = document.querySelectorAll('.mobile-link');
const loginPop = document.querySelector('.login-outer');
const closeLogin = document.getElementById('close-login');
const loginBtns = document.querySelectorAll('.login');

hamburger.addEventListener('click', ()=> {
  mobileNav.style.display = 'block';
});

close.addEventListener('click', () => {
  mobileNav.style.display = 'none';
})

closeLogin.addEventListener('click', ()=>{
  loginPop.style.display = 'none';
})

navBtns.forEach( (btn)=> {
  btn.addEventListener('click', ()=>{
    mobileNav.style.display = 'none';
    if(btn.getAttribute('class', 'login')) {
      loginPop.style.display = 'block';
    }
    // loginPop.style.display = 'none';
  })
});

loginBtns.forEach((btn)=> {
  btn.addEventListener('click', () => {
    if(loginPop.style.display === 'none' || loginPop.style.display === ''){
      loginPop.style.display = 'block';
    } else if (loginPop.style.display === 'block') {
      loginPop.style.display = 'none';
    }
  })
})