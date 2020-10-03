// pop up form || nav
const navPop = document.querySelector('.mobile-nav');
const loginPop = document.querySelector('.login-outer');
const registerPop = document.querySelector('.register-outer');
// close btns
const closeNav = document.getElementById('close');
const closeLogin = document.getElementById('close-login');
const closeRegister = document.getElementById('close-register');
// open btns
const hamburger = document.getElementById('hamburger');
const navBtns = document.querySelectorAll('.mobile-link');
const loginBtns = document.querySelectorAll('.login');
const registerBtns = document.querySelectorAll('.register');

const closeBtns = [closeNav, closeLogin, closeRegister];


const toggler = (btns) => {
  btns.forEach((btn)=> {
    btn.addEventListener('click', ()=> {

      // register form
      if(btn.classList.contains('register')) {
        if(registerPop.style.display === 'none' || registerPop.style.display === '') {
          registerPop.style.display = 'block';
          loginPop.style.display = 'none';
        } else if (registerPop.style.display === 'block') {
          registerPop.style.display = 'none';
        }

      //login form
      } else if (btn.classList.contains('login')){
          if(loginPop.style.display === 'none' || loginPop.style.display === ''){
            loginPop.style.display = 'block';
            registerPop.style.display = 'none';
          } else if (loginPop.style.display === 'block') {
            loginPop.style.display = 'none';
          }

      //mobile nav
      } else if (btn.getAttribute('id') === 'hamburger'){
          navPop.style.display = 'block';
          registerPop.style.display = 'none';
          loginPop.style.display = 'none';
      }
      
    });
  });
}


const closePopUp = (btns) => {
  btns.forEach((btn) => {
    btn.addEventListener('click', ()=> {

      // close nav
      if(btn.getAttribute('id') === 'close'){
        navPop.style.display = 'none';

      // close login
      } else if (btn.getAttribute('id') === 'close-login') {
        loginPop.style.display = 'none';

      //close register
      } else if (btn.getAttribute('id') === 'close-register') {
        registerPop.style.display = 'none';

      //close nav if you click a link
      } else if (btn.classList.contains('mobile-link')){
        navPop.style.display = 'none';

        // if link is login, open login form
        if(btn.classList.contains('login-btn')) {
          loginPop.style.display = 'block';
        }
      }

    });
  });
}

toggler(registerBtns);
toggler(loginBtns);
toggler([hamburger]);
closePopUp(closeBtns);
closePopUp(navBtns);
